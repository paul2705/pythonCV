import cv2
from numpy import *

Img=cv2.imread('../ActiveTest/Active.jpg');
ImgGray=cv2.cvtColor(Img,cv2.COLOR_BGR2GRAY);
sift=cv2.xfeatures2d.SIFT_create();
keypoints=sift.detect(ImgGray,None);
ImgSIFT=copy(Img);
cv2.drawKeypoints(Img,keypoints,ImgSIFT,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS);
cv2.imshow('Input Image',Img);
cv2.imshow('SIFT features',ImgSIFT);
cv2.waitKey();
