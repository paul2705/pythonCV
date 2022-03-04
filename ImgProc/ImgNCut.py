from PIL import Image
from numpy import *
from pylab import *
import NCut

Img=array(Image.open('../ActiveTest/gesture/train/C-uniform03.ppm'));
m,n=Img.shape[:2];

Wid=50;
RImg=array(Image.fromarray(Img).resize((Wid,Wid),Image.BILINEAR));
RImg=array(RImg,'f');

A=NCut.NCutGraphMatrix(RImg,SigmaD=1,SigmaG=1e-2);

Code,V=NCut.Cluster(A,K=3,NDim=3);

CodeImg=array(Image.fromarray(Code.reshape((Wid,Wid))).resize((m,n),Image.NEAREST));

figure(); gray(); 
subplot(2,4,1); imshow(CodeImg);

for i in range(4):
	subplot(2,4,i+2); 
	imshow(array(Image.fromarray(V[i].reshape((Wid,Wid))).resize((m,n),Image.BILINEAR)));

show();
