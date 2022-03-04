from PIL import Image
from numpy import *
from pylab import *
from scipy.cluster.vq import *
#from scipy.misc import imresize

Stepsx=51; Stepsy=604;
Img=array(Image.open('../ActiveTest/KMeansRGB.png'));
print(Img.shape);
Dx=Img.shape[0]//Stepsx;
Dy=Img.shape[1]//Stepsy;

Features=[];
for x in range(Stepsx):
    for y in range(Stepsy):
        R=mean(Img[x*Dx:(x+1)*Dx,y*Dy:(y+1)*Dy,0]);
        G=mean(Img[x*Dx:(x+1)*Dx,y*Dy:(y+1)*Dy,1]);
        B=mean(Img[x*Dx:(x+1)*Dx,y*Dy:(y+1)*Dy,2]);
        Features.append([R,G,B]);
Features=array(Features,'f');

Centroids,Variance=kmeans(Features,4,iter=500,thresh=1e-9);
print(Centroids);
Code,Distance=vq(Features,Centroids);
CodeImg=Code.reshape(Stepsx,Stepsy);
CodeImg=CodeImg*255.0/4.0;
h,w=Img.shape[:2];
CodeImg=array(Image.fromarray(CodeImg).resize((w,h),Image.NEAREST),'f');

figure(); imshow(CodeImg); show();

m,n=CodeImg.shape;
with open('../ActiveTest/KMeansRGB1.txt','w') as f:
	for i in range(m):
		for j in range(n):
			f.write(str(CodeImg[i,j])+' ');
		f.write('\n');
