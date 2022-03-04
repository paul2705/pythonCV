from PIL import Image
from numpy import *
from pylab import *
import pickle
import KNN, ImgTools

with open('points_normal.pkl','rb') as f:
    Class1=pickle.load(f);
    Class2=pickle.load(f);
    Labels=pickle.load(f);

Model=KNN.KNNClassifier(Labels,vstack((Class1,Class2)));

def Classify(X,Y,Model=Model):
    return array([Model.Classify([x,y]) for (x,y) in zip(X,Y)]);

with open('points_normal_test.pkl','rb') as f:
    Class1=pickle.load(f);
    Class2=pickle.load(f);
    Labels=pickle.load(f);

ImgTools.Plot2DBoundary([-6,6,-6,6],[Class1,Class2],Classify,[1,-1]);
show();

