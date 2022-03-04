from PIL import Image
from numpy import *
from scipy.ndimage import filters
from pylab import *

Img=array(Image.open("../ActiveTest/Active.jpg"));

Imgx=zeros(Img.shape);
for i in range(3):
    filters.sobel(Img[:,:,i],1,Imgx[:,:,i]);

Imgy=zeros(Img.shape);
for i in range(3):
    filters.sobel(Img[:,:,i],0,Imgy[:,:,i]);

Magnitude=zeros(Img.shape);
for i in range(3):
    Magnitude[:,:,i]=sqrt(Imgx[:,:,i]**2+Imgy[:,:,i]**2);
#Magnitue=sqrt(Imgx**2+Imgy**2);

figure(); 
subplot(2,4,1); imshow(Img);
subplot(2,4,3); imshow(Imgx);
subplot(2,4,5); imshow(Imgy);
subplot(2,4,7); imshow(Magnitude);
show();

imsave("../ActiveTest/ImgDerive_Imgx.jpg",Imgx.astype(uint8));
imsave("../ActiveTest/ImgDerive_Imgy.jpg",Imgy.astype(uint8));
imsave("../ActiveTest/ImgDerive_Magnitude.jpg",Magnitude.astype(uint8));
