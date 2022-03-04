import os
from PIL import Image
from pylab import *
im=array(Image.open("../ActiveTest/Active.jpg"));
imshow(im);
x=[0,0,50,50];
y=[0,0,50,50];
plot(x,y,"r*");
plot(x[:2],y[:2]);
title("Plot");
show();
