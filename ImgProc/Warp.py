from PIL import Image
from numpy import *
from pylab import *
from scipy import ndimage
import Homography
from scipy.spatial import Delaunay

def ImgInImg(Img1,Img2,tp):
    '''使用仿射变换将Img1放置在Img2上，使Img1图像的角和tp尽可能的靠近
       tp是齐次表示的，并且是按照从左上角逆时针计算的'''

    m,n=Img1.shape[:2];
    fp=array([[0,m,m,0],[0,0,n,n],[1,1,1,1]]);

    H=Homography.HaffineFromPoints(tp,fp);
    Img1Trans=ndimage.affine_transform(Img1,H[:2,:2],(H[0,2],H[1,2]),Img2.shape[:2]);
    Alpha=(Img1Trans>0);

    return (1-Alpha)*Img2+Alpha*Img1Trans;

def AlphaForTriangle(Points,m,n):
    '''对于带有由Points定义角点的三角形，创建大小为(m,n)的alpha图（在归一化的齐次坐标意义下）'''
    
    Alpha=zeros((m,n));
    for i in range(min(Points[0]),max(Points[0])):
        for j in range(min(Points[1]),max(Points[1])):
            x=linalg.solve(Points,[i,j,1]);
            if min(x)>0:
                Alpha[i,j]=1;

    return Alpha;

def TriangulatePoints(x,y):
    '''二维点的Delaunay三角剖分'''
    Tri=Delaunay(c_[x,y]).simplices;
    return Tri;

def PWAffine(FromImg,ToImg,fp,tp,Tri):
    '''从一幅图像中扭曲矩形图像块'''
    Img=ToImg.copy();
    IsColor=len(FromImg.shape)==3;
    ImgTrans=zeros(Img.shape,'uint8');

    for t in Tri:
        H=Homography.HaffineFromPoints(tp[:,t],fp[:,t]);
        if IsColor:
            for col in range(FromImg.shape[2]):
                ImgTrans[:,:,col]=ndimage.affine_transform(FromImg[:,:,col],H[:2,:2],(H[0,2],H[1,2]),Img.shape[:2]);
        else:
            ImgTrans=ndimage.affine_transform(FromImg,H[:2,:2],(H[0,2],H[1,2]),Img.shape[:2]);
    
        Alpha=AlphaForTriangle(tp[:,t],Img.shape[0],Img.shape[1]);
        Img[Alpha>0]=ImgTrans[Alpha>0];

    return Img;

def PlotMesh(x,y,Tri):
    for t in Tri:
        TExtend=[t[0],t[1],t[2],t[0]];
        plot(x[TExtend],y[TExtend],'r');

def Panorama(H,FromImg,ToImg,Padding=2400,Delta=2400):
    '''使用单应性矩阵H（使用RANSAC稳健性估计得出），协调两幅图像，创建水平全景图像。结果为一幅和ToImg具有相同高度的图像'''

    IsColor=len(FromImg.shape)==3;

    def Trans(p):
        p2=dot(H,[p[0],p[1],1]);
        return (p2[0]/p2[2],p2[1]/p2[2]);

    if H[1,2]<0:
        print('Warp Right');
        if IsColor:
            ToImgT=hstack((ToImg,zeros((ToImg.shape[0],Padding,3))));
            FromImgT=zeros((ToImg.shape[0],ToImg.shape[1]+Padding,ToImg.shape[2]));
            for col in range(3):
                FromImgT[:,:,col]=ndimage.geometric_transform(FromImg[:,:,col],Trans,(ToImg.shape[0],ToImg.shape[1]+Padding));
        
        else:
            ToImgT=hstack((ToImg,zeros((ToImg.shape[0],Padding))));
            FromImgT=ndimage.geometric_transform(FromImg,Trans,(ToImg.shape[0],ToImg.shape[1]+Padding));

    else:
        print('Warp Left');
        HDelta=array([[1,0,0],[0,1,-Delta],[0,0,1]]);
        H=dot(H,HDelta);
        if IsColor:
            ToImgT=hstack((zeros((ToImg.shape[0],Padding,3)),ToImg));
            FromImgT=zeros((ToImg.shape[0],ToImg.shape[1]+Padding,ToImg.shape[2]));
            for col in range(3):
                FromImgT[:,:,col]=ndimage.geometric_transform(FromImg[:,:,col],Trans,(ToImg.shape[0],ToImg.shape[1]+Padding));
        
        else:
            ToImgT=hstack((zeros((ToImg.shape[0],Padding)),ToImg));
            FromImgT=ndimage.geometric_transform(FromImg,Trans,(ToImg.shape[0],ToImg.shape[1]+Padding));
            
    if IsColor:
        Alpha=((FromImgT[:,:,0]*FromImgT[:,:,1]*FromImgT[:,:,2])>0);
        for col in range(3):
            ToImgT[:,:,col]=FromImgT[:,:,col]*Alpha+ToImgT[:,:,col]*(1-Alpha);
    else:
        Alpha=(FromImgT>0);
        ToImgT=FromImgT*Alpha+ToImgT*(1-Alpha);

    return ToImgT;

