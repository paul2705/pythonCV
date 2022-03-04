from PIL import Image
from pylab import *
from numpy import *
from scipy.ndimage import filters

Img=array(Image.open("../ActiveTest/Active.jpg"));
sigma=5;

Imgx=zeros(Img.shape);
for i in range(3):
    filters.gaussian_filter(Img[:,:,i],(sigma,sigma),(0,1),Imgx[:,:,i]);

Imgy=zeros(Img.shape);
for i in range(3):
    filters.gaussian_filter(Img[:,:,i],(sigma,sigma),(1,0),Imgy[:,:,i]);

Magnitude=sqrt(Imgx**2+Imgy**2);

figure();
subplot(2,4,1); imshow(Img); title("Img");
subplot(2,4,3); imshow(Imgx); title("GaussianImgx");
subplot(2,4,5); imshow(Imgy); title("GaussianImgy");
subplot(2,4,7); imshow(Magnitude); title("Magnitude");
show();

imsave("../ActiveTest/ImgGausDerive_Imgx.jpg",Imgx.astype(uint8));
imsave("../ActiveTest/ImgGausDerive_Imgy.jpg",Imgy.astype(uint8));
imsave("../ActiveTest/ImgGausDerive_Magnitude.jpg",Magnitude.astype(uint8));
