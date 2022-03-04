from PIL import Image
from numpy import *
from pylab import *
from pygraph.classes.digraph import digraph
from pygraph.algorithms.minmax import maximum_flow
import Bayes

def BuildBayesGraph(Img,Labels,Sigma=1e2,Kappa=2):
    '''从像素四邻域建立一个图，前景和背景（前景用1标记，背景用-1标记，其他的用0标记）由Labels决定，并用朴素贝叶斯分类器建模'''
    m,n=Img.shape[:2];
    Vim=array(Img.reshape((-1,3)));

    Foreground=Img[Labels==1].reshape((-1,3));
    Background=Img[Labels==-1].reshape((-1,3));
    TrainData=[Foreground,Background];

    BC=Bayes.BayesClassifier();
    BC.Train(TrainData);

    BCLabels,Prob=BC.Classify(Vim);
    ProbFg=Prob[0];
    ProbBg=Prob[1];

    G=digraph();
    G.add_nodes(range(m*n+2));
    Source=m*n;
    Sink=m*n+1;

    for i in range(Vim.shape[0]):
        Vim[i]=Vim[i]/linalg.norm(Vim[i]);
        
    for i in range(m*n):
        G.add_edge((Source,i),wt=(ProbFg[i]/(ProbFg[i]+ProbBg[i])));
        G.add_edge((i,Sink),wt=(ProbBg[i]/(ProbFg[i]+ProbBg[i])));

        if i%n!=0:
            W=Kappa*exp(-1.0*sum((Vim[i]-Vim[i-1])**2)/Sigma);
            G.add_edge((i,i-1),wt=W);
        if (i+1)%n!=0:
            W=Kappa*exp(-1.0*sum((Vim[i]-Vim[i+1])**2)/Sigma);
            G.add_edge((i,i+1),wt=W);
        if i//n!=0:
            W=Kappa*exp(-1.0*sum((Vim[i]-Vim[i-n])**2)/Sigma);
            G.add_edge((i,i-n),wt=W);
        if i//n!=m-1:
            W=Kappa*exp(-1.0*sum((Vim[i]-Vim[i+n])**2)/Sigma);
            G.add_edge((i,i+n),wt=W);

    return G;

def ShowLabeling(Img,Labels):
    '''显示图像的前景和背景区域。前景Labels=1，背景Labels=-1，其他labels=0'''
    imshow(Img);
    contour(Labels,[-0.5,0.5]);
    contour(Labels,[-1,-0.5],colors='b',alpha=0.25);
    contour(Labels,[0.5,1],colors='r',alpha=0.25);
    axis('off');

def CutGraph(G,ImgSize):
    '''用最大流对图G进行分割，并返回分割结果的二值标记'''
    m,n=ImgSize;
    Source=m*n;
    Sink=m*n+1;

    Flows,Cuts=maximum_flow(G,Source,Sink);

    Res=zeros(m*n);
    for Pos,Label in list(Cuts.items())[:-2]:
        Res[Pos]=Label;

    return Res.reshape((m,n));
