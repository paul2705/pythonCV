from PIL import Image
from numpy import *
from pylab import *
from scipy.cluster.vq import *
import sift, pickle

class Vocabulary(object):
    def __init__(self,Name):
        self.Name=Name;
        self.Voc=[];
        self.Idf=[];
        self.TrainingData=[];
        self.NumWords=0;

    def Train(self,FeatureFiles,K=100,SubSampling=6):
        '''用含有k个单词的K-means列出在featurefiles中的特征选练出一个词汇。对训练数据下采样可以加快训练速度'''
        ImgNum=100;
        with open("../ActiveTest/first400/ukbench.pkl","rb") as f:
            D=pickle.load(f);
        Desc=[];
        Desc.append(D[0]);
        Descriptors=Desc[0];
        for i in range(1,ImgNum):
            Desc.append(D[i]);
            Descriptors=vstack((Descriptors,Desc[i]));

        self.Voc,Distortion=kmeans(Descriptors[::SubSampling,:],K,1);
        self.NumWords=self.Voc.shape[0];

        ImgWords=zeros((ImgNum,self.NumWords));
        for i in range(ImgNum):
            ImgWords[i]=self.Project(Desc[i]);

        NumOccurences=sum((ImgWords>0)*1,axis=0);
        self.Idf=log((1.0*ImgNum)/(1.0*NumOccurences+1));
        self.TrainingData=FeatureFiles;

    def Project(self,Descriptors):
        '''将描述子投影到词汇上，以创建单词直方图'''
        
        ImgHist=zeros((self.NumWords));
        Words,Distance=vq(Descriptors,self.Voc);
        for w in Words:
            ImgHist[w]+=1;

        return ImgHist;
