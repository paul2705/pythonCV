from PIL import Image
from numpy import *
from pylab import *
import HCluster

Class1=1.5*randn(100,2);
Class2=randn(100,2)+array([5,5]);
Features=vstack((Class1,Class2));
figure();
plot(Class1[:,0],Class1[:,1],'r.');
plot(Class2[:,0],Class2[:,1],'b.');
show();

Tree=HCluster.HCluster(Features);
Clusters=Tree.ExtractClusters(5);

print('Number of Clusters',len(Clusters));
for c in Clusters:
    print(c.GetClusterElements());


