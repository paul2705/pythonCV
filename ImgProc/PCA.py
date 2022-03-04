from PIL import Image
from numpy import *
from pylab import *

def PCA(Data):
    ''' Principal Component Analysis '''
    NumData,Dim=Data.shape;
    
    MeanData=Data.mean(axis=0);
    Data=Data-MeanData;

    if Dim>NumData:
        M=dot(Data,Data.T); # 协方差矩阵
        e,EV=linalg.eigh(M); # 特征值和特征向量
        tmp=dot(Data.T,EV).T; # 紧致技巧
        V=tmp[::-1]; 
        S=sqrt(e)[::-1];
        for i in range(V.shape[1]):
            V[:,i]/=S;
    else: # Singular Value Decomposition (SVD)
        U,S,V=linalg.svd(Data);
        V=V[:NumData];

    return V,S,MeanData;


