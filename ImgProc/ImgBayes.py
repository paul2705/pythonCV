from PIL import Image
from numpy import *
from pylab import *
import os, sift, Bayes, PCA

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

Features,Labels=ReadGestureFeaturesLabels('../ActiveTest/gesture/train');
TestFeatures,TestLabels=ReadGestureFeaturesLabels('../ActiveTest/gesture/test/');

ClassNames=unique(Labels);

V,S,M=PCA.PCA(Features);
V=V[:50];
Features=array([dot(V,F-M) for F in Features]);
TestFeatures=array([dot(V,F-M) for F in TestFeatures]);

BC=Bayes.BayesClassifier();
BList=[Features[where(Labels==C)[0]] for C in ClassNames];
BC.Train(BList,ClassNames);
Res=BC.Classify(TestFeatures)[0];

Acc=sum(1.0*(Res==TestLabels))/len(TestLabels);
print('Accuracy:',Acc);

PrintConfusion(Res,Labels,ClassNames);
