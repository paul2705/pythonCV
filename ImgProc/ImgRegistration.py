from xml.dom import minidom
from scipy import linalg
from scipy import ndimage
#from scipy.misc import imsave
import os
from numpy import *
from pylab import *
from PIL import Image

def ReadPointsFromXML(XMLFileName):
    XMLDoc=minidom.parse(XMLFileName);
    FaceList=XMLDoc.getElementsByTagName('face');
    Faces={};
    for XMLFace in FaceList:
        FileName=XMLFace.attributes['file'].value;
        xf=int(XMLFace.attributes['xf'].value);
        yf=int(XMLFace.attributes['yf'].value);
        xs=int(XMLFace.attributes['xs'].value);
        ys=int(XMLFace.attributes['ys'].value);
        xm=int(XMLFace.attributes['xm'].value);
        ym=int(XMLFace.attributes['ym'].value);
        Faces[FileName]=array([xf,yf,xs,ys,xm,ym]);
    return Faces;

def ComputeRigidTransform(RefPoints,Points):
    '''计算用于将点对齐到参考点的旋转、尺度和平移量'''
    A=array([[Points[0],-Points[1],1,0],
             [Points[1],Points[0],0,1],
             [Points[2],-Points[3],1,0],
             [Points[3],Points[2],0,1],
             [Points[4],-Points[5],1,0],
             [Points[5],Points[4],0,1]]);
    y=array([RefPoints[0],RefPoints[1],RefPoints[2],
             RefPoints[3],RefPoints[4],RefPoints[5]]);

    a,b,tx,ty=linalg.lstsq(A,y)[0];
    R=array([[a,-b],[b,a]]);

    return R,tx,ty;

def RigidAlignment(Faces,Path,PlotFlag=False):
    '''严格对齐图像，并将其保存为新的图像，Path为文件保存路径'''

    RefPoints=list(Faces.values())[0];

    for Face in Faces:
        Points=Faces[Face];
        R,tx,ty=ComputeRigidTransform(RefPoints,Points);
        T=array([[R[1][1],R[1][0]],[R[0][1],R[0][0]]]);
    
        Img=array(Image.open(os.path.join(Path,Face)));
        NewImg=zeros(Img.shape,'uint8');

        for i in range(len(Img.shape)):
            NewImg[:,:,i]=ndimage.affine_transform(Img[:,:,i],linalg.inv(T),offset=[-ty,-tx]);

        if PlotFlag:
            imshow(NewImg); show();

        h,w=NewImg.shape[:2];
        border=(w+h)//20;

        imsave(os.path.join(Path, 'aligned/'+Face),NewImg[border:h-border,border:w-border,:]);



