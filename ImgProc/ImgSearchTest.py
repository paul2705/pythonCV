from PIL import Image
from numpy import *
from pylab import *
import ImageSearch, ImgTools
import pickle

with open('../ActiveTest/first400/Vocabulary.pkl','rb') as f:
    Voc=pickle.load(f);

ImgList=ImgTools.GetImgList('../ActiveTest/first400');
ImgList.sort();

src=ImageSearch.Searcher('test.db',Voc);
print(ImageSearch.ComputeScore(src,ImgList));
NumResults=6;
Res=[W[1] for W in src.Query(ImgList[2])[:NumResults]];
ImageSearch.PlotResults(src,Res);
