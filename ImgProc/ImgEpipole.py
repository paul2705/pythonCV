from PIL import Image
from numpy import *
from pylab import *
import Sfm
import Homography
from ImgSfmLoadData import *

Index=(Corr[:,0]>=0)&(Corr[:,1]>=0);

X1=Homography.MakeHomoG(Points2D[0][:,Corr[Index,0]]);
X2=Homography.MakeHomoG(Points2D[1][:,Corr[Index,1]]);

F=Sfm.ComputeFundamental(X1,X2);
E=Sfm.ComputeEpipole(F);

figure(); imshow(Img1);
for i in range(5):
    Sfm.PlotEpipolarLine(Img1,F,X2[:,i],E,True);
axis('off');

figure(); imshow(Img2);
for i in range(5):
    plot(X2[0,i],X2[1,i],'o');
axis('off');

show();
