from PIL import Image
from numpy import *
from pylab import *
from scipy.cluster.vq import *

def NCutGraphMatrix(Img,SigmaD,SigmaG=1e-2):
    '''创建用于归一化割的矩阵，其中SigmaD和SigmaG是像素距离和像素相似性的权重参数'''

    m,n=Img.shape[:2];
    N=m*n;

    if len(Img.shape)==3:
        for i in range(3):
            Img[:,:,i]=Img[:,:,i]/Img[:,:,i].max();
        VImg=Img.reshape((-1,3));
    else:
        Img=Img/Img.max();
        VImg=Img.flatten();

    x,y=meshgrid(range(n),range(m));
    X,Y=x.flatten(),y.flatten();

    W=zeros((N,N),'f');
    for i in range(N):
        for j in range(i,N):
            D=(X[i]-X[j])**2+(Y[i]-Y[j])**2;
            W[i,j]=W[j,i]=exp(-1.0*sum((VImg[i]-VImg[j])**2)/SigmaG)*exp(-D/SigmaD);

    return W;

def Cluster(S,K,NDim):
    '''从相似性矩阵进行谱聚类'''

    if sum(abs(S-S.T))>1e-10:
        raise ValueError('NOT Symmetric!');

    RowSum=sum(abs(S),axis=0);
    D=diag(1/sqrt(RowSum+1e-6));
    L=dot(D,dot(S,D));

    U,Sigma,V=linalg.svd(L);
    
    Features=array(V[:NDim]).T;

    Features=whiten(Features);
    Centroids,Distortion=kmeans(Features,K);
    Code,Distance=vq(Features,Centroids);

    return Code,V;


