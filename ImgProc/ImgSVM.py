from PIL import Image
from numpy import *
from pylab import *
import os, sift, PCA
from libsvm.svmutil import *

def ReadGestureFeaturesLabels(Path):
    FeatList=[os.path.join(Path,f) for f in os.listdir(Path) if f.endswith('.dsift')];
    Features=[];
    for FeatFile in FeatList:
        L,D=sift.ReadFeaturesFromFile(FeatFile);
        Features.append(D.flatten());
    Features=array(Features);

    Labels=[FeatFile.split('/')[-1][0] for FeatFile in FeatList];
    return Features,array(Labels);

def PrintConfusion(Res,Labels,ClassNames):
	N=len(ClassNames);
	ClassIndex=dict([(ClassNames[i],i) for i in range(N)]);
	Confuse=zeros((N,N));
	for i in range(len(TestLabels)):
		Confuse[ClassIndex[Res[i]],ClassIndex[TestLabels[i]]]+=1;

	print('Confusion Matrix For');
	print(ClassNames);
	print(Confuse);

def ConvertLabels(Labels,Trans):
    ConvertLabels=zeros((len(Labels)));
    for i in range(len(Labels)):
        ConvertLabels[i]=int(Trans[Labels[i]]);
    return ConvertLabels;

def ConvertRes(Res,Trans):
    ConvertRes=[];
    for i in range(len(Res)):
        ConvertRes.append(str(Trans[Res[i]]));
    return ConvertRes;

Features,Labels=ReadGestureFeaturesLabels('../ActiveTest/gesture/train');
TestFeatures,TestLabels=ReadGestureFeaturesLabels('../ActiveTest/gesture/test/');

ClassNames=unique(Labels);

V,S,M=PCA.PCA(Features);
V=V[:50];
Features=array([dot(V,F-M) for F in Features]);
TestFeatures=array([dot(V,F-M) for F in TestFeatures]);

Features=list(Features);
TestFeatures=list(TestFeatures);

Trans={};
for i,c in enumerate(ClassNames):
    Trans[c],Trans[i]=i,c;

Prob=svm_problem(ConvertLabels(Labels,Trans),Features);
Param=svm_parameter('-t 0');

Model=svm_train(Prob,Param);
Res=svm_predict(ConvertLabels(TestLabels,Trans),TestFeatures,Model)[0];
Res=ConvertRes(Res,Trans);

Acc=sum(1.0*(Res==TestLabels))/len(TestLabels);
print('Accuracy:',Acc);

PrintConfusion(Res,TestLabels,ClassNames);

