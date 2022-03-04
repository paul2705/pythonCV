from PIL import Image
from numpy import *
from pylab import *
import Homography
import Warp

def ConvertPoints(j):
    Index=Matches[j].nonzero()[0];
    fp=Homography.MakeHomoG(L[j+1][Index,:2].T);
    Index2=[int(Matches[j][i]) for i in Index];
    tp=Homography.MakeHomoG(L[j][Index2,:2].T);
    fp=vstack([fp[1],fp[0],fp[2]]);
    tp=vstack([tp[1],tp[0],tp[2]]);
    return fp,tp;

import sift

FeatName=['../MergeImg/'+str(i)+'.sift' for i in range(5)];
ImgName=['../MergeImg/'+str(i)+'.jpg' for i in range(5)];
L={}; D={};
for i in range(5):
    sift.ProcessImage(ImgName[i],FeatName[i]);
    L[i],D[i]=sift.ReadFeaturesFromFile(FeatName[i]);

Matches={};
for i in range(4):
    Matches[i]=sift.Match(D[i+1],D[i]);
    '''
    figure(); gray();
    sift.PlotMatches(array(Image.open(ImgName[i+1]).convert('L')),array(Image.open(ImgName[i]).convert('L')),L[i+1],L[i],Matches[i]);
    show();
    '''

Model=Homography.RansacModel();

fp,tp=ConvertPoints(1);
H12=Homography.HFromRansac(fp,tp,Model)[0];
print(H12);
fp,tp=ConvertPoints(0);
H01=Homography.HFromRansac(fp,tp,Model)[0];
print(H01);
tp,fp=ConvertPoints(2);
H32=Homography.HFromRansac(fp,tp,Model)[0];
print(H32);
tp,fp=ConvertPoints(3);
H43=Homography.HFromRansac(fp,tp,Model)[0];
print(H43);

Delta=2000;

Img1=array(Image.open(ImgName[1]),'uint8');
Img2=array(Image.open(ImgName[2]),'uint8');
Img12=Warp.Panorama(H12,Img1,Img2,Delta,Delta);

Img1=array(Image.open(ImgName[0]),'f');
Img02=Warp.Panorama(dot(H12,H01),Img1,Img12,Delta,Delta);

Img1=array(Image.open(ImgName[3]),'f');
Img32=Warp.Panorama(H32,Img1,Img02,Delta,Delta);

Img1=array(Image.open(ImgName[4]),'f');
Img42=Warp.Panorama(dot(H32,H43),Img1,Img32,Delta,2*Delta);

figure(); imshow(Img42.astype('uint8'));
show();

imsave("../MergeImg/ImgRansac.jpg",Img42.astype('uint8'));
