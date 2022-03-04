from PIL import Image
from numpy import *
from pylab import *
from scipy import ndimage
import Homography

ImgName='../ActiveTest/sudoku_images/sudokus/sudoku2.JPG';
Img=array(Image.open(ImgName).convert('L'));

figure(); gray(); imshow(Img);
X=ginput(4);
print(X);
fp=array([array([P[1],P[0],1]) for P in X]).T;
tp=array([[0,0,1],[0,1000,1],[1000,1000,1],[1000,0,1]]).T;

H=Homography.HFromPoints(tp,fp);

def WrapFcn(X):
    X=array([X[0],X[1],1]);
    XT=dot(H,X);
    XT/=XT[2];
    return XT[0],XT[1];

Img=ndimage.geometric_transform(Img,WrapFcn,(1000,1000));
imsave('../ActiveTest/sudoku_images/sudokus/sudoku_Con.JPG',Img);
figure(); imshow(Img); show();
