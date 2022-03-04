from ImgTools import *
Img=ComputeAvgImg(GetImgList('../Collect'));
imshow(Img); show();

imsave("../ActiveTest/ImgAvg.jpg",Img);

