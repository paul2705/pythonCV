from PIL import Image
from pylab import *

Img=array(Image.open("../ActiveTest/Active.jpg"));

imsave('../ActiveTest/ImgSave.jpg',Img);
