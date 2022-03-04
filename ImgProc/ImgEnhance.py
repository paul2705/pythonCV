import ImgTools
import os
from PIL import Image
from pylab import *
Img=array(Image.open("../ActiveTest/ImgGausDerive_Magnitude.jpg").convert('L'));
NewImg,cdf=ImgTools.HistEq(Img);
figure(); imshow(NewImg); title('NewImg');
figure(); imshow(Img); title('Img');
show();

imsave("../ActiveTest/ImgGausDerive_Magnitude_Enhanced.jpg",NewImg);

