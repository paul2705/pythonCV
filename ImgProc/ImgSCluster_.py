from PIL import Image, ImageDraw
from pylab import *
from numpy import *
import ImgTools
import pickle
import sift
from scipy.cluster.vq import *

Path='../ActiveTest/panoimages/';
ImgList=ImgTools.GetImgList(Path);
ImgNum=min(len(ImgList),40);
S=zeros((ImgNum,ImgNum));
'''
L={}; D={};
for i in range(ImgNum):
	sift.ProcessImage(ImgList[i],'tmp.sift');
	L[i],D[i]=sift.ReadFeaturesFromFile('tmp.sift');

for i in range(ImgNum):
	for j in range(ImgNum):
		S[i,j]=1/(sum(sift.MatchTwoSided(D[i],D[j])>0)+1e-9);

with open("../ActiveTest/panoimages/Matches.pkl","wb") as f:
	pickle.dump(S,f);
'''
with open("../ActiveTest/panoimages/Matches.pkl","rb") as f:
	S=pickle.load(f);

N=ImgNum;
RowSum=sum(S,axis=0);
D=diag(1/sqrt(RowSum));
I=identity(N);
L=I-dot(D,dot(S,D));

U,Sigma,V=linalg.svd(L);

k=15;
Features=array(V[:k]).T;

Features=whiten(Features);
Centroids,Distortion=kmeans(Features,k,iter=500);
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

