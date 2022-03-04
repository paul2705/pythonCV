from PIL import Image
from numpy import *
from pylab import *
import Camera
from ImgSfmLoadData import *

X=vstack((Points3D,ones(Points3D.shape[1])));
x=P[0].Project(X);

figure(); imshow(Img1); 
plot(Points2D[0][0],Points2D[0][1],'*');
axis('off');

figure(); imshow(Img1);
plot(x[0],x[1],'r.');
axis('off');

show();

from mpl_toolkits.mplot3d import axes3d

fig=figure();
ax=fig.gca(projection='3d');
X,Y,Z=axes3d.get_test_data(0.25);
ax.plot(X.flatten(),Y.flatten(),Z.flatten(),'o');
show();

fig=figure();
ax=fig.gca(projection='3d');
ax.plot(Points3D[0],Points3D[1],Points3D[2],'k.');
show();
