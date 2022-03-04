from PIL import Image
from numpy import *
from pylab import *
from scipy import ndimage

Img=array(Image.open("../ActiveTest/Active.jpg").convert('L'));
H=array([[1.4,0.5,-500],[0.5,1.5,-500],[0,0,1]]);
NewImg=ndimage.affine_transform(Img,H[:2,:2],(H[0,2],H[1,2]));

figure(); gray(); imshow(NewImg);
imsave("../ActiveTest/ImgAffine.jpg",NewImg);
show();
