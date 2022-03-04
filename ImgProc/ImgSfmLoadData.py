from PIL import Image
from numpy import *
from pylab import *
import Camera

Path='../ActiveTest/MertonCollegeI/';
Img1=array(Image.open('../ActiveTest/MertonCollegeI/001.jpg'));
Img2=array(Image.open('../ActiveTest/MertonCollegeI/002.jpg'));

Points2D=[loadtxt(Path+'2D/00'+str(i+1)+'.corners').T for i in range(3)];
Points3D=loadtxt(Path+'3D/p3d').T;
Corr=genfromtxt(Path+'2D/nview-corners',dtype='int',missing_values='*');

P=[Camera.Camera(loadtxt(Path+'2D/00'+str(i+1)+'.P')) for i in range(3)];

