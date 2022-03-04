from PIL import Image
from numpy import *
from pylab import *
from scipy import ndimage
import Homography
import Warp

Img1=array(Image.open("../ActiveTest/Active.jpg").convert('L'));
Img2=array(Image.open("../ActiveTest/ActivePair.jpg").convert('L'));

m,n=Img1.shape[:2];
fp=array([[0,m,m,0],[0,0,n,n],[1,1,1,1]]);

figure(); imshow(Img2); print("Please Click 4 Points(CounterClockWise)...");
x=array(ginput(4));
Points=array([x[:,1],x[:,0]]).astype('uint64');
tp=Homography.MakeHomoG(Points).astype('uint64');

tp2=tp[:,:3];
fp2=fp[:,:3];

H=Homography.HaffineFromPoints(tp2,fp2);
Img1Trans=ndimage.affine_transform(Img1,H[:2,:2],(H[0,2],H[1,2]),Img2.shape[:2]);

Alpha=Warp.AlphaForTriangle(tp2,Img2.shape[0],Img2.shape[1]);
TmpImg=(1-Alpha)*Img2+Alpha*Img1Trans;

tp2=tp[:,[0,2,3]];
fp2=fp[:,[0,2,3]];

H=Homography.HaffineFromPoints(tp2,fp2);
Img1Trans=ndimage.affine_transform(Img1,H[:2,:2],(H[0,2],H[1,2]),Img2.shape[:2]);

Alpha=Warp.AlphaForTriangle(tp2,Img2.shape[0],Img2.shape[1]);
NewImg=(1-Alpha)*TmpImg+Alpha*Img1Trans;

figure(); gray(); imshow(NewImg);
axis('equal'); axis('off');
show();
imsave("../ActiveTest/ImgAffineTrans.jpg",NewImg);

