from PIL import Image
from numpy import *
from pylab import *

class BayesClassifier(object):
    def __init__(self):
        '''使用训练数据初始化分类器'''
        self.Labels=[];#类标签
        self.Mean=[];#类均值
        self.Var=[];#类方差
        self.N=0;#类别数

    def Train(self,Data,Labels=None):
        '''在数据Data上训练，标记Labels是可选的，默认为0...n-1'''
#        if (Labels==None).any():
        if Labels==None:
           Labels=range(len(Data));
        self.Labels=Labels;
        self.N=len(Labels);

        for c in Data:
            self.Mean.append(mean(c,axis=0));
            self.Var.append(var(c,axis=0));

    def Classify(self,Points):
        '''通过计算得出的每一类的概率对数据点进行分类，并返回最可能的标记'''
        EstProb=array([Gauss(M,V,Points) for M,V in zip(self.Mean,self.Var)]);
        Index=EstProb.argmax(axis=0);
        EstLabels=array([self.Labels[i] for i in Index]);
        return EstLabels,EstProb;

def Gauss(M,V,X):
    '''用独立均值M和方差V评估D维高斯分布'''
    if len(X.shape)==1:
        N,D=1,X.shape[0];
    else:
        N,D=X.shape;

    S=diag(1/V);
    X=X-M;
    Y=exp(-0.5*diag(dot(X,dot(S,X.T))));

    return Y*(2*pi)**(-D/2.0)/(sqrt(prod(V))+1e-9);

