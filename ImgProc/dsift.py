from PIL import Image
from numpy import *
from pylab import *
import os
import sift

def ProcessImageDSift(ImgName,ResultName,Size=20,Steps=10,ForceOrientation=False,Resize=None):
    '''用密集采样的SIFT描述子处理一幅图像，并将结果保存在一个文件中。可选的输入：特征的大小Size，位置之间的步长Steps，是否强迫计算描述子的方位ForceOrientation（False表示所有的方位都是朝上的），用于调查图像大小的元组'''
    Img=Image.open(ImgName).convert('L');
    if Resize!=None:
        Img=Img.resize(Resize);
    m,n=Img.size;

    if ImgName[-3:]!='pgm':
        Img.save('../ActiveTest/tmp.pgm');
        ImgName='../ActiveTest/tmp.pgm';

    Scale=Size/3.0;
    X,Y=meshgrid(range(Steps,m,Steps),range(Steps,n,Steps));
    x,y=X.flatten(),Y.flatten();
    Frame=array([x,y,Scale*ones(x.shape[0]),zeros(x.shape[0])]);
    savetxt('../ActiveTest/tmp.frame',Frame.T,fmt='%03.3f');

    if ForceOrientation:
        Cmd=str("sift "+ImgName+" --output="+ResultName+" --read-frames=../ActiveTest/tmp.frame --orientations");
    else:
        Cmd=str("sift "+ImgName+" --output="+ResultName+" --read-frames=../ActiveTest/tmp.frame");

    os.system(Cmd);
    print('Processed',ImgName,'To',ResultName);

