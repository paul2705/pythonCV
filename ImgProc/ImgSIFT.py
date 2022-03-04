import sift
from PIL import Image
from numpy import *
from pylab import *

ImgName='../ActiveTest/Active.jpg';
Img1=array(Image.open(ImgName).convert('L'));
sift.ProcessImage(ImgName,'../ActiveTest/Active.sift');
l1,d1=sift.ReadFeaturesFromFile('../ActiveTest/Active.sift');

ImgName='../ActiveTest/ActivePair.jpg';
Img2=array(Image.open(ImgName).convert('L'));
sift.ProcessImage(ImgName,'../ActiveTest/ActivePair.sift');
l2,d2=sift.ReadFeaturesFromFile('../ActiveTest/ActivePair.sift');

print('Starting Matching...');
Matches=sift.MatchTwoSided(d1,d2);

figure(); gray();
sift.PlotMatches(Img1,Img2,l1,l2,Matches);
show();

