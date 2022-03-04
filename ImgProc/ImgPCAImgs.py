from PIL import Image, ImageDraw
from pylab import *
from numpy import *
import ImgTools
import pickle
from scipy.cluster.vq import *

ImgList=ImgTools.GetImgList('../ActiveTest/selectedfontimages/a_selected_thumbs/');
ImgNum=len(ImgList);

with open('../ActiveTest/selectedfontimages/a_pca_modes.pkl','rb') as f:
    ImgMean=pickle.load(f);
    V=pickle.load(f);

ImgMatrix=array([array(Image.open(Img)).flatten() for Img in ImgList],'f');

ImgMean=ImgMean.flatten();
Projected=array([dot(V[[0,1]],ImgMatrix[i]-ImgMean) for i in range(ImgNum)]);
Projected=whiten(Projected);

h,w=1200,1200;
Img=Image.new('RGB',(w,h),(255,255,255));
Draw=ImageDraw.Draw(Img);

Draw.line((0,h/2,w,h/2),fill=(255,0,0));
Draw.line((w/2,0,w/2,h),fill=(255,0,0));

Scale=abs(Projected).max(0);
Scaled=floor(array([(P/Scale)*(w/2-20,h/2-20)+(w/2,h/2) for P in Projected])).astype(int);

for i in range(ImgNum):
    NodeImg=Image.open(ImgList[i]);
    NodeImg.thumbnail((25,25));
    NSize=NodeImg.size;
    Img.paste(NodeImg,(Scaled[i][0]-NSize[0]//2,Scaled[i][1]-NSize[1]//2,
                Scaled[i][0]+NSize[0]//2+1,Scaled[i][1]+NSize[1]//2+1));

figure(); imshow(Img); show();
Img.save('../ActiveTest/selectedfontimages/PCAFont.jpg');
