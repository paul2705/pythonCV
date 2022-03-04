from PIL import Image
from numpy import *
from pylab import *
import Stereo

ImgL=array(Image.open("../ActiveTest/cones/im2.ppm").convert('L'),'f');
ImgR=array(Image.open("../ActiveTest/cones/im3.ppm").convert('L'),'f');

Steps=12; Start=4; Wid=9;

Res1=Stereo.PlaneSweepGauss(ImgL,ImgR,Start,Steps,Wid);

imsave('../ActiveTest/cones/depthGauss.png',Res1.astype('float32'));

Res2=Stereo.PlaneSweepNCC(ImgL,ImgR,Start,Steps,Wid);

imsave('../ActiveTest/cones/depthNCC.png',Res2.astype('float32'));

