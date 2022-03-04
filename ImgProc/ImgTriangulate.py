from PIL import Image
from numpy import *
from pylab import *
from ImgSfmLoadData import *
import Sfm
import Homography
from mpl_toolkits.mplot3d import axes3d

Index=(Corr[:,0]>=0)&(Corr[:,1]>=0);

X1=Homography.MakeHomoG(Points2D[0][:,Corr[Index,0]]);
X2=Homography.MakeHomoG(Points2D[1][:,Corr[Index,1]]);

XTrue=Homography.MakeHomoG(Points3D[:,Index]);

XEst=Sfm.Triangulate(X1,X2,P[0].P,P[1].P);
print(XEst[:,:3]);
print(XTrue[:,:3]);

fig=figure();
ax=fig.gca(projection='3d');
ax.plot(XEst[0],XEst[1],XEst[2],'ko');
ax.plot(XTrue[0],XTrue[1],XTrue[2],'r.');
#axis('equal');
show();
