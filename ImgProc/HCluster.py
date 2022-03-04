from PIL import Image, ImageDraw
from numpy import *
from pylab import *
from itertools import combinations

class ClusterNode(object):
    def __init__(self,Vec,Left,Right,Distance=0.0,Count=1):
        self.Left=Left; self.Right=Right; self.Vec=Vec;
        self.Distance=Distance; self.Count=Count;

    def ExtractClusters(self,Dist):
        if self.Distance<Dist:
            return [self];
        return self.Left.ExtractClusters(Dist)+self.Right.ExtractClusters(Dist);
    
    def GetClusterElements(self):
        '''在聚类子树中返回元素的id'''
        return self.Left.GetClusterElements()+self.Right.GetClusterElements();

    def GetHeight(self):
        '''返回节点的高度，高度是各分支的和'''
        return self.Left.GetHeight()+self.Right.GetHeight();

    def GetDepth(self):
        '''返回节点的深度，深度是每个子节点取最大再加上他的自身距离'''
        return max(self.Left.GetDepth(),self.Right.GetDepth())+self.Distance;

    def Draw(self,Draw,X,Y,S,ImgList,Img):
        '''用图像缩略图递归的画出叶节点'''
        H1=int(self.Left.GetHeight()*50/2);
        H2=int(self.Right.GetHeight()*50/2);
        Top=Y-(H1+H2);
        Bottom=Y+(H1+H2);

        Draw.line((X,Top+H1,X,Bottom-H2),fill=(0,0,0));
        DL=self.Distance*S;
        Draw.line((X,Top+H1,X+DL,Top+H1),fill=(0,0,0));
        Draw.line((X,Bottom-H2,X+DL,Bottom-H2),fill=(0,0,0));

        self.Left.Draw(Draw,X+DL,Top+H1,S,ImgList,Img);
        self.Right.Draw(Draw,X+DL,Bottom-H2,S,ImgList,Img);
        

class ClusterLeafNode(object):
    def __init__(self,Vec,id):
        self.Vec=Vec; self.id=id;

    def ExtractClusters(self,Dist):
        return [self];

    def GetClusterElements(self):
        return [self.id];

    def GetHeight(self):
        return 1

    def GetDepth(self):
        return 0

    def Draw(self,Draw,X,Y,S,ImgList,Img):
        NodeImg=Image.open(ImgList[self.id]);
        NodeImg.thumbnail([50,50]);
        NSize=NodeImg.size;
        Img.paste(NodeImg,[int(X),int(Y-NSize[1]//2),int(X+NSize[0]),int(Y+NSize[1]-NSize[1]//2)]);


def L2Dist(V1,V2):
    return sqrt(sum((V1-V2)**2));
    
def L1Dist(V1,V2):
    return sum(abs(V1-V2));

def HCluster(Features,DistFc=L2Dist):
    '''用层次聚类对行特征进行聚类'''
    Distances={};
    Node=[ClusterLeafNode(array(f),id=i) for i,f in enumerate(Features)];

    while len(Node)>1:
        Closest=float('inf');

        for u,v in combinations(Node,2):
            if (u,v) not in Distances:
                Distances[u,v]=DistFc(u.Vec,v.Vec);
            Tmp=Distances[u,v];
            if Tmp<Closest:
                Closest=Tmp;
                LowestPair=(u,v);
        u,v=LowestPair;

        NewVec=(u.Vec+v.Vec)/2.0;

        NewNode=ClusterNode(NewVec,Left=u,Right=v,Distance=Closest);
        Node.remove(u); Node.remove(v);
        Node.append(NewNode);

    return Node[0];

def DrawDendrogram(Node,ImgList,FileName='clusters.jpg'):
    '''绘制聚类树状图，并保存到文件中'''

    Rows=Node.GetHeight()*50;
    Cols=1200;

    S=float(Cols-150)/Node.GetDepth();

    Img=Image.new('RGB',(Cols,Rows),(255,255,255));
    Draw=ImageDraw.Draw(Img);

    Draw.line((0,Rows/2,50,Rows/2),fill=(0,0,0));

    Node.Draw(Draw,50,(Rows/2),S,ImgList,Img);
    Img.save(FileName);
    Img.show();


