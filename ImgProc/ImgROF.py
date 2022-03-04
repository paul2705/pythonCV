from PIL import Image
from pylab import *
import ROF
from numpy import *
from numpy import random

Img=array(Image.open("../ActiveTest/Active.jpg"));
U=T=zeros(Img.shape);
for i in range(3):
    U[:,:,i],T[:,:,i]=ROF.denoise(Img[:,:,i],Img[:,:,i]);

figure(); 
subplot(2,4,1); imshow(Img); title("Img");
subplot(2,4,3); imshow(U.astype(uint8)); title("ROF");

imsave('../ActiveTest/ImgROF_RGB.jpg',U.astype(uint8));

Img=zeros((500,500));
Img[100:400,100:400]=128;
Img[200:300,200:300]=255;
Img=Img+30*random.standard_normal((500,500));

U,T=ROF.denoise(Img,Img);

figure();
subplot(2,4,1); imshow(Img); title("Img");
subplot(2,4,3); imshow(U); title("ROF");
show();

imsave('../ActiveTest/ImgROF_Flat.jpg',U);
