from PIL import Image
from numpy import *
from pylab import *
from Harris import *

Wid=5;
Img1=array(Image.open("../ActiveTest/Active.jpg").convert('L'));
HarrisImg=ComputeHarrisResponse(Img1);
FilteredCoords1=GetHarrisPoints(HarrisImg,10);
d1=GetDescriptors(Img1,FilteredCoords1,Wid);

Img2=array(Image.open("../ActiveTest/ActivePair.jpg").convert('L'));
HarrisImg=ComputeHarrisResponse(Img2);
FilteredCoords2=GetHarrisPoints(HarrisImg,10);
d2=GetDescriptors(Img2,FilteredCoords2,Wid);

print('Starting Matching...');
Matches=MatchTwoSided(d1,d2);

figure(); gray();
PlotMatches(Img1,Img2,FilteredCoords1,FilteredCoords2,Matches);
show();

