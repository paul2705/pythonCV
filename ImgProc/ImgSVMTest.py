from PIL import Image
from numpy import *
from pylab import *
import pickle
from libsvm.svmutil import *
import ImgTools

with open('points_ring.pkl','rb') as f:
    Class1=pickle.load(f);
    Class2=pickle.load(f);
    Labels=pickle.load(f);

Class1=list(Class1);
Class2=list(Class2);
Labels=list(Labels);
Samples=Class1+Class2;

Prob=svm_problem(Labels,Samples);
Param=svm_parameter('-t 2');
Model=svm_train(Prob,Param);

Res=svm_predict(Labels,Samples,Model);

with open('points_ring_test.pkl','rb') as f:
    Class1=pickle.load(f);
    Class2=pickle.load(f);
    Labels=pickle.load(f);

Class1=list(Class1);
Class2=list(Class2);

def Predict(X,Y,Model=Model):
    Points=[];
    for i in range(len(X)):
        Points.append(array([X[i],Y[i]]));
    return array(svm_predict([0]*len(X),list(Points),Model)[0]);

ImgTools.Plot2DBoundary([-6,6,-6,6],[array(Class1),array(Class2)],Predict,[1,-1]);
show();

