from scipy.spatial import Delaunay
from PIL import Image
from numpy import *
from pylab import *
from numpy import random

x,y=array(random.standard_normal((2,100)));
Tri=Delaunay(c_[x,y]).simplices;

figure();
for t in Tri:
    TExtend=[t[0],t[1],t[2],t[0]];
    plot(x[TExtend],y[TExtend],'r');

plot(x,y,'*');
axis('off');
show();
