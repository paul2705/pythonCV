from PIL import Image
from numpy import *
from pylab import *
import os
import HCluster
import ImgTools

Path='../ActiveTest/sunsets/flickr-sunsets-small/';
ImgList=ImgTools.GetImgList(Path);

Features=zeros([len(ImgList),512]);
for i,FileName in enumerate(ImgList):
    Img=array(Image.open(FileName));
    H,Edges=histogramdd(Img.reshape(-1,3),8,normed=True,range=[(0,255),(0,255),(0,255)]);
    Features[i]=H.flatten();

Tree=HCluster.HCluster(Features);
HCluster.DrawDendrogram(Tree,ImgList,FileName='../ActiveTest/sunsets/sunset.pdf');

Clusters=Tree.ExtractClusters(0.23*Tree.Distance);

for c in Clusters:
	Elements=c.GetClusterElements();
	NumElements=len(Elements);
	if NumElements>3:
		figure();
		for p in range(min(NumElements,20)):
			subplot(4,5,p+1);
			Img=array(Image.open(ImgList[Elements[p]]));
			imshow(Img);
			axis('off');
show();

