from ImgTools import *
import sift
from PIL import Image
from numpy import *
from pylab import *

Wid=5;
ImgList=GetImgList("../GroupImg/");
NumImg=len(ImgList);
MatchScores=zeros((NumImg,NumImg));
for i in range(NumImg):
    ImgName=ImgList[i];
    ResultName=ImgName[:-3]+'sift';
    sift.ProcessImage(ImgName,ResultName);

for i in range(NumImg):
    for j in range(i,NumImg):
        print("Comparing ",ImgList[i],ImgList[j]);

        l1,d1=sift.ReadFeaturesFromFile(ImgList[i][:-3]+'sift');
        l2,d2=sift.ReadFeaturesFromFile(ImgList[j][:-3]+'sift');

        Matches=sift.MatchTwoSided(d1,d2);

        NumMatches=sum(Matches>0);
        print('Number of matches = ',NumMatches);
        MatchScores[i,j]=NumMatches;

for i in range(NumImg):
    for j in range(i+1,NumImg):
        MatchScores[j,i]=MatchScores[i,j];

