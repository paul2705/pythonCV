from scipy.cluster.vq import *
from PIL import Image
from numpy import *
from pylab import *

Class1=1.5*randn(100,2);
Class2=randn(100,2)+array([5,5]);
Features=vstack((Class1,Class2));

Centroids,Variance=kmeans(Features,2);
Code,Distance=vq(Features,Centroids);

figure();
Index=where(Code==0)[0];
plot(Features[Index,0],Features[Index,1],'*');
Index=where(Code==1)[0];
plot(Features[Index,0],Features[Index,1],'r.');
plot(Centroids[:,0],Centroids[:,1],'go');
axis('off');
show();
