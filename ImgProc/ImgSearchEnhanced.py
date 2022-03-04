from PIL import Image
from numpy import *
from pylab import *
import pickle
import sift, ImageSearch, Homography, ImgTools

with open('../ActiveTest/first400/Vocabulary.pkl','rb') as f:
    Voc=pickle.load(f);

ImgList=ImgTools.GetImgList('../ActiveTest/first400');
ImgList.sort();
ImgNum=min(len(ImgList),100);

Src=ImageSearch.Searcher('test.db',Voc);

QryIndex=50;
NumResults=20;

ResReg=[W[1] for W in Src.Query(ImgList[0])[:NumResults]];
print('Top Matches (Regular):',ResReg);

sift.ProcessImage(ImgList[0],'tmp.sift');
QryLocs,QryDesc=sift.ReadFeaturesFromFile('tmp.sift');
fp=Homography.MakeHomoG(QryLocs[:,:2].T);

Model=Homography.RansacModel();

Rank={};
for Index in ResReg[1:]:
    sift.ProcessImage(ImgList[Index-1],'tmp.sift');
    L,D=sift.ReadFeaturesFromFile('tmp.sift');

    Matches=sift.Match(QryDesc,D);
    Ind=Matches.nonzero()[0];
    Ind2=[int(Matches[i]) for i in Ind];
    tp=Homography.MakeHomoG(L[:,:2].T);

    try:
        H,inliers=Homography.HFromRansac(fp[:,Ind],tp[:,Ind2],Model,MatchTheshold=10);
    except:
        inliers=[];
        
    print(len(inliers));
    Rank[Index]=len(inliers);
    
SortedRank=sorted(Rank.items(),key=lambda x:x[1],reverse=True);
ResGeom=[ResReg[0]]+[S[0] for S in SortedRank];
print('Top Matches (Homography):',ResGeom);

ImageSearch.PlotResults(Src,ResReg[:8]);
ImageSearch.PlotResults(Src,ResGeom[:8]);
