from PIL import Image
from numpy import *
from pylab import *
import GraphCut

Img=array(Image.open('../ActiveTest/Empire.jpg'));
m,n=Img.shape[:2];
Scale=0.05;
M,N=int(m*Scale),int(n*Scale);
NewImg=array(Image.fromarray(Img).resize((N,M),Image.BILINEAR));
Size=NewImg.shape[:2];

Labels=zeros(Size);
Labels[3:15,3:15]=-1;
Labels[-15:-3,-15:-3]=1;

G=GraphCut.BuildBayesGraph(NewImg,Labels,Kappa=1);
Res=GraphCut.CutGraph(G,Size);

figure();
GraphCut.ShowLabeling(NewImg,Labels);

figure(); gray(); imshow(Res);
axis('off');
show();
