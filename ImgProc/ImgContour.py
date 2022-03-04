import os
from PIL import Image
from pylab import *
im=array(Image.open("../ActiveTest/Active.jpg").convert('L'));
figure();
gray();
contour(im,origin='image');
axis('equal');
#show();
figure();
hist(im.flatten(),128);
show();

