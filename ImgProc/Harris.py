'''harris角点检测'''
from scipy.ndimage import filters
from pylab import *
from numpy import *
from PIL import Image

def ComputeHarrisResponse(Img,Sigma=3):
    '''在一幅灰度图像中，对每个像素计算Harris角点检测器响应函数'''
    Imgx=zeros(Img.shape);
    filters.gaussian_filter(Img,(Sigma,Sigma),(0,1),Imgx);
    Imgy=zeros(Img.shape);
    filters.gaussian_filter(Img,(Sigma,Sigma),(1,0),Imgy);

    Wxx=filters.gaussian_filter(Imgx*Imgx,Sigma);
    Wxy=filters.gaussian_filter(Imgx*Imgy,Sigma);
    Wyy=filters.gaussian_filter(Imgy*Imgy,Sigma);

    Wdet=Wxx*Wyy-Wxy**2; #det(M)
    Wtr=Wxx+Wyy; #trace(M)

    return Wdet/Wtr;

def GetHarrisPoints(HarrisImg,MinDist=10,Threshold=0.1):
    '''从一幅harris响应图像中返回角点。MinDist为分割角点和图像边界的最少像素数目'''
    CornerThreshold=HarrisImg.max()*Threshold;
    HarrisImg_T=(HarrisImg>CornerThreshold)*1;

    Coords=array(HarrisImg_T.nonzero()).T;
    CandidateValues=[HarrisImg[c[0],c[1]] for c in Coords];
    Index=argsort(CandidateValues);

    AllowedLocations=zeros(HarrisImg.shape);
    AllowedLocations[MinDist:-MinDist,MinDist:-MinDist]=1;

    FilteredCoords=[];
    for i in Index:
        if AllowedLocations[Coords[i,0],Coords[i,1]]==1:
            FilteredCoords.append(Coords[i]);
            AllowedLocations[(Coords[i,0]-MinDist):(Coords[i,0]+MinDist),(Coords[i,1]-MinDist):(Coords[i,1]+MinDist)]=0;

    return FilteredCoords;

def PlotHarrisPoints(Img,FilteredCoords):
    figure(); gray(); imshow(Img);
    plot([p[1] for p in FilteredCoords],[p[0] for p in FilteredCoords],'*');
    axis('off');


    fig=plt.gcf()
    fig.set_size_inches(448/100,448/100) #dpi = 100, output = 700*700 pixels
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1,bottom=0,right=1,left=0,hspace=0,wspace=0)
    plt.margins(0,0)
    savefig("../ActiveTest/ImgHarris.jpg",transparent=True,dpi=100,pad_inches=0);

    
    show();

def GetDescriptors(Img,FilteredCoords,Wid=5):
    '''对于每个返回点，返回点周围2*wid+1个像素的值'''
    Desc=[];
    for Coords in FilteredCoords:
        Patch=Img[Coords[0]-Wid:Coords[0]+Wid+1,Coords[1]-Wid:Coords[1]+Wid+1].flatten();
        Desc.append(Patch);
    
    return Desc;

def Match(Desc1,Desc2,Threshold=0.5):
    '''对于第一幅图像中的每个角点描述子，使用归一化互相关，选取它在第二幅图像中的匹配角点'''
    n=len(Desc1[0]);
    
    d=-ones((len(Desc1),len(Desc2)));
    for i in range(len(Desc1)):
        for j in range(len(Desc2)):
            d1=(Desc1[i]-mean(Desc1[i]))/std(Desc1[i]);
            d2=(Desc2[j]-mean(Desc2[j]))/std(Desc2[j]);
            NCCValue=sum(d1*d2)/(n-1);
            if NCCValue>Threshold:
                d[i,j]=NCCValue;

    DIndex=argsort(-d);
    MatchScores=DIndex[:,0];

    return MatchScores;

def MatchTwoSided(Desc1,Desc2,Threshold=0.5):
    '''两边对称提高稳定性'''
    Matches12=Match(Desc1,Desc2,Threshold);
    Matches21=Match(Desc2,Desc1,Threshold);

    Index12=where(Matches12>=0)[0];

    for i in Index12:
        if Matches21[Matches12[i]]!=i:
            Matches12[i]=-1;

    return Matches12;

def AppendImages(Img1,Img2):
    '''返回将两幅图像并排拼成的一幅新图像'''
    Rows1=Img1.shape[0];
    Rows2=Img2.shape[0];

    if Rows1<Rows2:
        Img1=concatenate((Img1,zeros((Rows2-Rows1,Img1.shape[1]))),axis=0);
    elif Rows1>Rows2:
        Img2=concatenate((Img2,zeros((Rows1-Rows2,Img2.shape[1]))),axis=0);

    return concatenate((Img1,Img2),axis=1);

def PlotMatches(Img1,Img2,Locs1,Locs2,MatchScores,ShowBelow=True):
    Img3=AppendImages(Img1,Img2);
    if ShowBelow:
        Img3=vstack((Img3,Img3));

    imshow(Img3);

    cols1=Img1.shape[1];
    for i,m in enumerate(MatchScores):
        if m>0:
            plot([Locs1[i][1],Locs2[m][1]+cols1],[Locs1[i][0],Locs2[m][0]],'c');
    axis('off');


