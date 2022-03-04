from PIL import Image, ImageDraw
from pylab import *
from numpy import *
import ImgTools
import pickle
from scipy.cluster.vq import *

Path='../ActiveTest/selectedfontimages/a_selected_thumbs/';
ImgList=ImgTools.GetImgList(Path);
ImgNum=len(ImgList);

with open('../ActiveTest/selectedfontimages/a_pca_modes.pkl','rb') as f:
    ImgMean=pickle.load(f);
    V=pickle.load(f);

ImgMatrix=array([array(Image.open(Img)).flatten() for Img in ImgList],'f');

ImgMean=ImgMean.flatten();
Projected=array([dot(V[:40],ImgMatrix[i]-ImgMean) for i in range(ImgNum)]);

N=len(Projected);
S=array([[sqrt(sum((Projected[i]-Projected[j])**2)) for i in range(N)] for j in range(N)],'f');

RowSum=sum(S,axis=0);
D=diag(1/sqrt(RowSum));
I=identity(N);
L=I-dot(D,dot(S,D));

U,Sigma,V=linalg.svd(L);

k=5;
Features=array(V[:k]).T;

Features=whiten(Features);
Centroids,Distortion=kmeans(Features,4,iter=500);
Code,Distance=vq(Features,Centroids);

for c in range(k):
	Index=where(Code==c)[0];
	figure();
	for i in range(min(len(Index),39)):
		Img=Image.open(ImgList[Index[i]]);
		subplot(4,10,i+1);
		imshow(Img);
		axis('equal'); axis('off');
show();

