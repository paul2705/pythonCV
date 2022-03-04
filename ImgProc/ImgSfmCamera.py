from PIL import *
from numpy import *
from pylab import *
from ImgSfmLoadData import *
import Homography, Sfm, Camera

Corr=Corr[:,0];
Index3D=where(Corr>=0)[0];
Index2D=Corr[Index3D];

x=Homography.MakeHomoG(Points2D[0][:,Index2D]);
X=Homography.MakeHomoG(Points3D[:,Index3D]);

PEst=Camera.Camera(Sfm.ComputeP(x,X));

print(PEst.P/PEst.P[2,3]);
print(P[0].P/P[0].P[2,3]);

XEst=PEst.Project(X);

figure(); imshow(Img1);
plot(x[0],x[1],'bo');
plot(XEst[0],XEst[1],'r.');
axis('off');
show();
