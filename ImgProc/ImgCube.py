from PIL import Image
from pylab import *
import Homography
import Camera
import sift
import pickle

def CubePoints(C,Wid):
    '''创建用于绘制立方体的一个点列表'''
    P=[];
    P.append([C[0]-Wid,C[1]-Wid,C[2]-Wid]);
    P.append([C[0]-Wid,C[1]+Wid,C[2]-Wid]);
    P.append([C[0]+Wid,C[1]+Wid,C[2]-Wid]);
    P.append([C[0]+Wid,C[1]-Wid,C[2]-Wid]);
    P.append([C[0]-Wid,C[1]-Wid,C[2]-Wid]);

    P.append([C[0]-Wid,C[1]-Wid,C[2]+Wid]);
    P.append([C[0]-Wid,C[1]+Wid,C[2]+Wid]);
    P.append([C[0]+Wid,C[1]+Wid,C[2]+Wid]);
    P.append([C[0]+Wid,C[1]-Wid,C[2]+Wid]);
    P.append([C[0]-Wid,C[1]-Wid,C[2]+Wid]);

    P.append([C[0]-Wid,C[1]-Wid,C[2]+Wid]);
    P.append([C[0]-Wid,C[1]+Wid,C[2]+Wid]);
    P.append([C[0]-Wid,C[1]+Wid,C[2]-Wid]);
    P.append([C[0]+Wid,C[1]+Wid,C[2]-Wid]);
    P.append([C[0]+Wid,C[1]+Wid,C[2]+Wid]);
    P.append([C[0]+Wid,C[1]-Wid,C[2]+Wid]);
    P.append([C[0]+Wid,C[1]-Wid,C[2]-Wid]);

    return array(P).T;

def MyCalibration(Size):
    Row,Col=Size;
    Fx=2555*Col/2592;
    Fy=2586*Row/1936;
    K=diag([Fx,Fy,1]);
    K[0,2]=0.5*Col;
    K[1,2]=0.5*Row;
    return K;

sift.ProcessImage('../ActiveTest/book_frontal.JPG','../ActiveTest/book_frontal.sift');
L0,D0=sift.ReadFeaturesFromFile('../ActiveTest/book_frontal.sift');

sift.ProcessImage('../ActiveTest/book_perspective.JPG','../ActiveTest/book_perspective.sift');
L1,D1=sift.ReadFeaturesFromFile('../ActiveTest/book_perspective.sift');

Matches=sift.MatchTwoSided(D0,D1);
Index=Matches.nonzero()[0];
fp=Homography.MakeHomoG(L0[Index,:2].T);
Index2=[int(Matches[i]) for i in Index];
tp=Homography.MakeHomoG(L1[Index2,:2].T);

Model=Homography.RansacModel();
H,inliers=Homography.HFromRansac(fp,tp,Model);

K=MyCalibration((747,1000));
Box=CubePoints([0,0,0.1],0.1);
Cam1=Camera.Camera(hstack((K,dot(K,array([[0],[0],[-1]])))));
BoxCam1=Cam1.Project(Homography.MakeHomoG(Box[:,:5]));
BoxTrans=Homography.Normalize(dot(H,BoxCam1));

Cam2=Camera.Camera(dot(H,Cam1.P));
A=dot(linalg.inv(K),Cam2.P[:,:3]);
A=array([A[:,0],A[:,1],cross(A[:,0],A[:,1])]).T;
Cam2.P[:,:3]=dot(K,A);
BoxCam2=Cam2.Project(Homography.MakeHomoG(Box));

Img0=array(Image.open('../ActiveTest/book_frontal.JPG'));
Img1=array(Image.open('../ActiveTest/book_perspective.JPG'));

figure(); imshow(Img0);
plot(BoxCam1[0,:],BoxCam1[1,:],linewidth=3);

figure(); imshow(Img1);
plot(BoxTrans[0,:],BoxTrans[1,:],linewidth=3);

figure(); imshow(Img1);
plot(BoxCam2[0,:],BoxCam2[1,:],linewidth=3);
show();

with open('ar_camera.pkl','wb') as f:
    pickle.dump(K,f);
    pickle.dump(dot(linalg.inv(K),Cam2.P),f);
