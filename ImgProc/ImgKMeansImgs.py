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
Projected=array([dot(V[:40],ImgMatrix[i]-ImgMean) for i in range(ImgNum)]);

Projected=whiten(Projected);
Centroids,Distortion=kmeans(Projected,4);

Code,Distance=vq(Projected,Centroids);

for k in range(4):
    Index=where(Code==k)[0];
    figure(); gray();
    for i in range(minimum(len(Index),40)):
        subplot(4,10,i+1);
        imshow(ImgMatrix[Index[i]].reshape((25,25)));
        axis('off');

show();
