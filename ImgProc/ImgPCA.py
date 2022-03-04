from PIL import Image
from numpy import *
from pylab import *
from ImgTools import *
import PCA
import pickle

ImgList=GetImgList('../ActiveTest/fontimages/a_thumbs/');
Img=array(Image.open(ImgList[0]));
m,n=Img.shape[0:2];
ImgNum=len(ImgList);
print(ImgList);
ImgMatrix=array([array(Image.open(Img).convert('L')).flatten() for Img in ImgList],'f');
print(ImgMatrix.shape);

V,S,ImgMean=PCA.PCA(ImgMatrix);

figure();
gray();
subplot(2,4,1);
imshow(ImgMean.reshape(m,n));
#imsave("../PCVBook/PCVBookData/jkfaces/ImgPCA_Mean.jpg",ImgMean.reshape(m,n));
for i in range(4):
    subplot(2,4,i+2);
    imshow(V[i].reshape(m,n));
#    imsave("../PCVBook/PCVBookData/jkfaces/ImgPCA_Pattern{}.jpg".format(i),V[i].reshape(m,n));

show();

# use pickle to save data
with open('../ActiveTest/selectedfontimages/a_pca_modes.pkl','wb') as f:
    pickle.dump(ImgMean,f);
    pickle.dump(V,f);
'''
# use pickle to load data
with open('font_pca_modes.pkl','rb') as f:
    ImgMean=pickle.load(f);
    V=pickle.load(f);
'''