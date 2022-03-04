from PIL import Image
from numpy import *
from pylab import *
import Warp
import Homography

Img1=array(Image.open("../ActiveTest/Active.jpg").convert('L'));
Img2=array(Image.open("../ActiveTest/ActivePair.jpg").convert('L'));

figure(); imshow(Img2); print("Please Click 4 Points(CounterClockWise)...");
x=array(ginput(4));
Points=array([x[:,1],x[:,0]]);
tp=Homography.MakeHomoG(Points);

NewImg=Warp.ImgInImg(Img1,Img2,tp);

figure(); gray(); imshow(NewImg); 
imsave("../ActiveTest/ImgTransform.jpg",NewImg);
axis('equal'); axis('off');
show();
