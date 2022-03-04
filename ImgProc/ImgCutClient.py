from PIL import Image
from numpy import *
from pylab import *
import GraphCut

def CreateMSRLabels(Img,Lasso=False):
    '''从用户的注释中创建用于训练的标记矩阵'''
    Labels=zeros(Img.shape[:2]);
    Labels[Img==30]=-1;
    Labels[Img==64]=-1;
    if Lasso:
        Labels[Img==215]=1;
    else:
        Labels[Img==128]=1;

    return Labels;

Img=array(Image.open('../ActiveTest/book_perspective.JPG'));
'''
NewImg=ones(Img.shape[:2]);
NewImg[:,:]=22;
NewImg[300:500,400:600]=128;
NewImg[500:700,700:1000]=0;
imsave('../ActiveTest/book_per.bmp',NewImg);
'''
ImgPer=array(Image.open('../ActiveTest/book_per.bmp').convert('L'));

Scale=0.05;
m,n=Img.shape[:2];
N,M=int(m*Scale),int(n*Scale);
Img=array(Image.fromarray(Img).resize((M,N),Image.BILINEAR));
ImgPer=array(Image.fromarray(ImgPer).resize((M,N),Image.NEAREST));

Labels=CreateMSRLabels(ImgPer,True);

G=GraphCut.BuildBayesGraph(Img,Labels,Kappa=2);
Res=GraphCut.CutGraph(G,Img.shape[:2]);

Res[m==30]=1;
Res[m==64]=1;

imsave('../ActiveTest/book_cut.jpg',Res);
figure(); gray(); imshow(Res);
xticks([]); yticks([]);
show();
