from PIL import Image
from numpy import *
from pylab import *
from scipy.ndimage import filters

def PlaneSweepNCC(ImgL,ImgR,Start,Steps,Wid):
    '''使用归一化的互相关计算视差图像'''
    m,n=ImgL.shape;

    MeanL=zeros((m,n));
    MeanR=zeros((m,n));
    S=zeros((m,n));
    SL=zeros((m,n));
    SR=zeros((m,n));

    DMaps=zeros((m,n,Steps));

    filters.uniform_filter(ImgL,Wid,MeanL);
    filters.uniform_filter(ImgR,Wid,MeanR);

    NormL=ImgL-MeanL;
    NormR=ImgR-MeanR;

    for Disp in range(Steps):
        filters.uniform_filter(roll(NormL,-Disp-Start)*NormR,Wid,S);
        filters.uniform_filter(roll(NormL,-Disp-Start)*roll(NormL,-Disp-Start),Wid,SL);
        filters.uniform_filter(NormR**2,Wid,SR);

        DMaps[:,:,Disp]=S/sqrt(SL*SR);

    return argmax(DMaps,axis=2);

def PlaneSweepGauss(ImgL,ImgR,Start,Steps,Wid):
    '''使用带有高斯加权周边的归一化互相关计算视差图像'''
    m,n=ImgL.shape;

    MeanL=zeros((m,n));
    MeanR=zeros((m,n));
    S=zeros((m,n));
    SL=zeros((m,n));
    SR=zeros((m,n));

    DMaps=zeros((m,n,Steps));

    filters.gaussian_filter(ImgL,Wid,0,MeanL);
    filters.gaussian_filter(ImgR,Wid,0,MeanR);

    NormL=ImgL-MeanL;
    NormR=ImgR-MeanR;

    for Disp in range(Steps):
        filters.gaussian_filter(roll(NormL,-Disp-Start)*NormR,Wid,0,S);
        filters.gaussian_filter(roll(NormL,-Disp-Start)*roll(NormL,-Disp-Start),Wid,0,SL);
        filters.gaussian_filter(NormR**2,Wid,0,SR);

        DMaps[:,:,Disp]=S/sqrt(SL*SR);

    return argmax(DMaps,axis=2);



