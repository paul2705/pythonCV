from PIL import Image
from numpy import *
from pylab import *
from sqlite3 import dbapi2 as sqlite
import pickle

class Indexer(object):
    def __init__(self,DB,Voc):
        '''初始化数据库的名称及词汇对象'''
        self.Con=sqlite.connect(DB);
        self.Voc=Voc;

    def __del__(self):
        self.Con.close();

    def DBCommit(self):
        self.Con.commit();

    def CreateTables(self):
        '''创建数据库表单'''
        self.Con.execute('create table imlist(filename)');
        self.Con.execute('create table imwords(imid,wordid,vocname)');
        self.Con.execute('create table imhistograms(imid,histogram,vocname)');
        self.Con.execute('create index im_idx on imlist(filename)');
        self.Con.execute('create index wordid_idx on imwords(wordid)');
        self.Con.execute('create index imid_idx on imwords(imid)');
        self.Con.execute('create index imidhist_idx on imhistograms(imid)');
        self.DBCommit();

    def AddToIndex(self,ImgName,Desc):
        '''获取一幅带有特征描述子的图像，投影到词汇上并添加进数据库'''
        if self.IsIndexed(ImgName): return;
        print('Indexing',ImgName);

        ImgID=self.GetID(ImgName);
        ImgWords=self.Voc.Project(Desc);
        NumWords=ImgWords.shape[0];
        
        for i in range(NumWords):
            Word=ImgWords[i];
            self.Con.execute('insert into imwords(imid,wordid,vocname) values (?,?,?)',(ImgID,Word,self.Voc.Name));
            
        self.Con.execute('insert into imhistograms(imid,histogram,vocname) values (?,?,?)',(ImgID,pickle.dumps(ImgWords),self.Voc.Name));

    def IsIndexed(self,ImgName):
        '''如果图像名字被索引到，就返回True'''
        Img=self.Con.execute("select rowid from imlist where filename='%s'"%ImgName).fetchone()
        return Img!=None;

    def GetID(self,ImgName):
        '''获取图像ID，如果不存在，就进行添加'''
        Cur=self.Con.execute("select rowid from imlist where filename='%s'"%ImgName);
        Res=Cur.fetchone();
        if Res==None:
            Cur=self.Con.execute("insert into imlist(filename) values ('%s')"%ImgName);
            return Cur.lastrowid
        else:
            return Res[0];


class Searcher(object):
    def __init__(self,DB,Voc):
        '''初始化数据课的名称'''
        self.Con=sqlite.connect(DB);
        self.Voc=Voc;

    def __del__(self):
        self.Con.close();

    def CandidatesFromWord(self,ImgWord):
        '''G获取包含ImgWord的图像列表'''
        ImgIDs=self.Con.execute("select distinct imid from imwords where wordid=%d"%ImgWord).fetchall();
        return [i[0] for i in ImgIDs];

    def CandidatesFromHistogram(self,ImgWords):
        '''获取具有相似单词的图像列表'''
        Words=ImgWords.nonzero()[0];
        Candidates=[];
        for Word in Words:
            C=self.CandidatesFromWord(Word);
            Candidates+=C;

        Tmp=[(W,Candidates.count(W)) for W in set(Candidates)];
        Tmp.sort(key=(lambda x: x[1]));
        Tmp.reverse();

        return [W[0] for W in Tmp];

    def GetImgHistogram(self,ImgName):
        '''返回一幅图像的单词直方图'''
        ImgID=self.Con.execute("select rowid from imlist where filename='%s'"%ImgName).fetchone();
        S=self.Con.execute("select histogram from imhistograms where rowid='%d'"%ImgID).fetchone();
        
        return pickle.loads(S[0]);

    def GetFileName(self,ImgID):
        '''返回图像ID对应的文件名'''
        S=self.Con.execute("select filename from imlist where rowid='%d'"%ImgID).fetchone();
        return S[0];
        
    def Query(self,ImgName):
        '''查找所有与ImgName匹配的图像列表'''
        H=self.GetImgHistogram(ImgName);
        Candidates=self.CandidatesFromHistogram(H);

        MatchScores=[];
        for ImgID in Candidates:
            CandName=self.Con.execute("select filename from imlist where rowid=%d"%ImgID).fetchone();
            CandH=self.GetImgHistogram(CandName);
            CandDist=sqrt(sum(self.Voc.Idf*(H-CandH)**2));
            MatchScores.append((CandDist,ImgID));

        MatchScores.sort();
        return MatchScores;


def ComputeScore(Src,ImgList):
    '''对查询返回的前3个结果计算平均相似图像，并返回结果'''
    ImgNum=min(len(ImgList),100);
    Pos=zeros((ImgNum,4));
    for i in range(ImgNum):
        Qry=Src.Query(ImgList[i]);
        print(len(Qry));
        Pos[i]=[W[1]-1 for W in Qry[:4]];
        print(Pos[i]);
        
    Score=array([(Pos[i]//4)==(i//4) for i in range(ImgNum)])*1.0;
    return sum(Score)/ImgNum;

def PlotResults(Src,Res):
    '''显示在列表Res中的图像'''
    figure();
    NumResults=len(Res);
    for i in range(NumResults):
        ImgName=Src.GetFileName(Res[i]);
        subplot(1,NumResults,i+1);
        imshow(array(Image.open(ImgName)));
        axis('off');

    show();

