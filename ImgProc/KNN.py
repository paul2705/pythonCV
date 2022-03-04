from PIL import Image
from numpy import *
from pylab import *

class KNNClassifier(object):
    def __init__(self,Labels,Samples):
        '''使用训练数据初始化分类器'''
        self.Labels=Labels;
        self.Samples=Samples;

    def Classify(self,Point,K=3):
        '''在训练数据上采用K近邻分类，并返回标记'''
        Dist=array([L2Dist(Point,S) for S in self.Samples]);
        Index=Dist.argsort();
        Votes={};
        for i in range(K):
            Label=self.Labels[Index[i]];
            Votes.setdefault(Label,0);
            Votes[Label]+=1;
        return max(Votes);

def L2Dist(P1,P2):
    return sqrt(sum((P1-P2)**2));

