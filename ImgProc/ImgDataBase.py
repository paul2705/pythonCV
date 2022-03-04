from PIL import Image
from numpy import *
from pylab import *
import pickle
import ImgTools, sift, ImageSearch

ImgList=ImgTools.GetImgList('../ActiveTest/first400');
ImgList.sort();
ImgNum=min(len(ImgList),100);

with open('../ActiveTest/first400/Vocabulary.pkl','rb') as f:
    Voc=pickle.load(f);

with open('../ActiveTest/first400/ukbench.pkl','rb') as f:
    D=pickle.load(f);

Index=ImageSearch.Indexer('test.db',Voc);
Index.CreateTables();

for i in range(ImgNum):
    Index.AddToIndex(ImgList[i],D[i]);

Index.DBCommit();

