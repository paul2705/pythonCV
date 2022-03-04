import os
from PIL import Image
from pylab import *
im=array(Image.open("../ActiveTest/Active.jpg"));
imshow(im);
print("Please Click 3 Points...");
x=ginput(3);
print("You Clicked: ",x);
show();
