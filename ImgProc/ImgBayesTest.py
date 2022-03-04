from PIL import Image
from numpy import *
from pylab import *
import pickle
import Bayes, ImgTools

with open('points_ring.pkl','rb') as f:
    Class1=pickle.load(f);
    Class2=pickle.load(f);
    Labels=pickle.load(f);

BC=Bayes.BayesClassifier();
BC.Train([Class1,Class2],[1,-1]);

with open('points_ring_test.pkl','rb') as f:
    Class1=pickle.load(f);
    Class2=pickle.load(f);
    Labels=pickle.load(f);

print(BC.Classify(Class1[:10])[0]);

def Classify(X,Y,BC=BC):
    Points=vstack((X,Y));
    return BC.Classify(Points.T)[0];

ImgTools.Plot2DBoundary([-6,6,-6,6],[Class1,Class2],Classify,[1,-1]);
show();
