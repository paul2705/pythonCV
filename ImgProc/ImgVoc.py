from PIL import Image
from numpy import *
from pylab import *
import pickle
import ImgTools, Vocabulary, sift

ImgList=ImgTools.GetImgList('../ActiveTest/first400');
ImgList.sort();
ImgNum=min(len(ImgList),100);
FeatFile='../ActiveTest/first400/ukbench.pkl';
'''
L={}; D={};
for i in range(ImgNum):
	sift.ProcessImage(ImgList[i],'tmp.sift');
	L[i],D[i]=sift.ReadFeaturesFromFile('tmp.sift');
with open(FeatFile,'wb') as f:
	pickle.dump(D,f);
'''
Voc=Vocabulary.Vocabulary('ukbenchTest');
Voc.Train(FeatFile,1000,10);

with open('../ActiveTest/first400/Vocabulary.pkl','wb') as f:
    pickle.dump(Voc,f);

print("Vocabulary is:",Voc.Name,Voc.NumWords);
