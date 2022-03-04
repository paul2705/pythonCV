from PIL import Image
from numpy import *
from pylab import *
import os, sift, KNN

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

K=1;
KNNClassifier=KNN.KNNClassifier(Labels,Features);
Res=array([KNNClassifier.Classify(TestFeatures[i],K) for i in range(len(TestLabels))]);

Acc=sum(1.0*(Res==TestLabels))/len(TestLabels);
print('Accuracy:',Acc);

PrintConfusion(Res,Labels,ClassNames);
