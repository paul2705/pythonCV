from PIL import Image
from numpy import *
from pylab import *
import ImgTools
import dsift, sift

dsift.ProcessImageDSift('../ActiveTest/empire.jpg','../ActiveTest/empire.sift',90,40,True);
L,D=sift.ReadFeaturesFromFile('../ActiveTest/empire.sift');

Img=array(Image.open('../ActiveTest/empire.jpg'));
#Img.resize(90);
sift.PlotFeatures(Img,L,True);
show();

Path='../ActiveTest/gesture/test';
ImgList=ImgTools.GetImgList(Path);
for FileName in ImgList:
    FeatFile=FileName[:-3]+'dsift';
    dsift.ProcessImageDSift(FileName,FeatFile,10,5,Resize=(50,50));

Path='../ActiveTest/gesture/train';
ImgList=ImgTools.GetImgList(Path);
for FileName in ImgList:
    FeatFile=FileName[:-3]+'dsift';
    dsift.ProcessImageDSift(FileName,FeatFile,10,5,Resize=(50,50));

