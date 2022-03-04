import cv2
from pylab import *

Img=cv2.imread('../ActiveTest/empire.jpg');
GrayImg=cv2.cvtColor(Img,cv2.COLOR_BGR2GRAY);

figure(); gray(); imshow(GrayImg); 
show();
