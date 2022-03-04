from PIL import Image
from numpy import *
from pylab import *
from numpy.random import randn
import pickle

N=200;

Class1=0.6*randn(N,2);
Class2=1.2*randn(N,2)+array([5,1]);
Labels=hstack((ones(N),-ones(N)));
'''
figure();
plot(Class1[:,0],Class1[:,1],'r*');
plot(Class2[:,0],Class2[:,1],'bo');

figure();
plot(Labels[:,0],Labels[:,1],'r.');
'''

with open('points_normal_test.pkl','wb') as f:
    pickle.dump(Class1,f);
    pickle.dump(Class2,f);
    pickle.dump(Labels,f);

Class1=0.6*randn(N,2);
R=0.8*randn(N,1)+5;
Angle=2*pi*randn(N,1);
Class2=hstack((R*cos(Angle),R*sin(Angle)));
Labels=hstack((ones(N),-ones(N)));
with open('points_ring.pkl','wb') as f:
    pickle.dump(Class1,f);
    pickle.dump(Class2,f);
    pickle.dump(Labels,f);


