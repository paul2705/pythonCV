from PIL import Image
from numpy import *
from pylab import *
from mpl_toolkits.mplot3d import axes3d
import Homography, Sfm, sift, Camera

K=array([[2394,0,932],[0,2398,628],[0,0,1]]);

print('Step1...',end=' ');
Img1=array(Image.open('../ActiveTest/MertonCollegeI001.jpg'));
sift.ProcessImage('../ActiveTest/MertonCollegeI001.jpg','../ActiveTest/MertonCollegeI001.sift');
L1,D1=sift.ReadFeaturesFromFile('../ActiveTest/MertonCollegeI001.sift');

Img2=array(Image.open('../ActiveTest/MertonCollegeI002.jpg'));
sift.ProcessImage('../ActiveTest/MertonCollegeI002.jpg','../ActiveTest/MertonCollegeI002.sift');
L2,D2=sift.ReadFeaturesFromFile('../ActiveTest/MertonCollegeI002.sift');

print('Finished!');
print('Step2...',end=' ');
Matches=sift.MatchTwoSided(D1,D2);
print(Matches);
Index=Matches.nonzero()[0];
X1=Homography.MakeHomoG(L1[Index,:2].T);
Index2=[int(Matches[i]) for i in Index];
X2=Homography.MakeHomoG(L2[Index2,:2].T);

X1Normal=dot(inv(K),X1);
X2Normal=dot(inv(K),X2);

print('Finished!');
print('Step3...',end=' ');
Model=Sfm.RansacModel();
E,inliers=Sfm.FFromRansac(X1Normal,X2Normal,Model);
print(inliers);
print(inliers.shape);

print('Finished!');
print('Step4...',end=' ');
P1=array([[1,0,0,0],[0,1,0,0],[0,0,1,0]]);
P2=Sfm.ComputePFromEssential(E);

Pos=0; MaxRes=0;
for i in range(4):
    X=Sfm.Triangulate(X1Normal[:,inliers],X2Normal[:,inliers],P1,P2[i]);
    D1=dot(P1,X)[2];
    D2=dot(P2[i],X)[2];
    if sum(D1>0)+sum(D2>0)>MaxRes:
        MaxRes=sum(D1>0)+sum(D2>0);
        Pos=i;
        InFront=(D1>0)&(D2>0);

X=Sfm.Triangulate(X1Normal[:,inliers],X2Normal[:,inliers],P1,P2[Pos]);
X=X[:,InFront];

print('Finished!');
print('Step5...',end=' ');
fig=figure();
ax=fig.gca(projection='3d');
ax.plot(-X[0],X[1],X[2],'k.');
axis('off');

Cam1=Camera.Camera(P1);
Cam2=Camera.Camera(P2[Pos]);
X1Points=Cam1.Project(X);
X2Points=Cam2.Project(X);

X1PNormal=dot(K,X1Points);
X2PNormal=dot(K,X2Points);

figure(); imshow(Img1); gray();
plot(X1PNormal[0],X1PNormal[1],'o');
plot(X1[0],X1[1],'r.');
axis('off');

figure(); imshow(Img2); gray();
plot(X2PNormal[0],X2PNormal[1],'o');
plot(X2[0],X2[1],'r.');
axis('off');

show();

print('Finished!');
print('Completed!');