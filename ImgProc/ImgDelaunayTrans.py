from PIL import Image
from numpy import *
from pylab import *
import Homography
import Warp

FromImg=array(Image.open("../ActiveTest/Active.jpg"));
x,y=meshgrid(range(5),range(6));
x=(FromImg.shape[1]/4)*x.flatten();
y=(FromImg.shape[0]/5)*y.flatten();

Tri=Warp.TriangulatePoints(x,y);

Img=array(Image.open("../ActiveTest/ActivePair.jpg"));
figure(); imshow(Img); print("Please Click 30 Points...");
Tmp=array(ginput(30));
Points=array([Tmp[:,1],Tmp[:,0]]).astype('uint64');
with open("ImgDelaunayTransPoints.txt","w") as f:
	f.write(str(Points));

tp=Homography.MakeHomoG(Points).astype('uint64');
fp=Homography.MakeHomoG(array([y,x])).astype('uint64');

NewImg=Warp.PWAffine(FromImg,Img,fp,tp,Tri);

figure(); imshow(NewImg); #Warp.PlotMesh(tp[1],tp[0],Tri);
axis('off');
show();

imsave("../ActiveTest/ImgDelaunayTrans.jpg",NewImg);
