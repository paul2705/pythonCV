from PIL import Image
from numpy import *
from pylab import *
from libsvm.svmutil import *
import os, ImgTools
from scipy.ndimage import measurements

def ComputeFeature(Img):
    '''对一个ocr图像块返回一个特征向量'''

    NormImg=ImgTools.ImgResize(Img,(30,30));
    NormImg=NormImg[3:-3,3:-3];

    return NormImg.flatten();

def LoadOCRData(Path):
    '''返回路径中所有图像的标记及OCR特征'''
    ImgList=ImgTools.GetImgList(Path);
    Labels=[int(ImgFile.split('/')[-1][0]) for ImgFile in ImgList];

    Features=[];
    for ImgName in ImgList:
        Img=array(Image.open(ImgName).convert('L'));
        Features.append(ComputeFeature(Img));

    return array(Features),Labels;

def FindSudokuEdges(Img,axis=0):
    '''对一幅对齐后的数独图像查找单元格的边界'''
    Trim=1*(Img<128);
    S=Trim.sum(axis=axis);

    SLabels,SNum=measurements.label(S>(0.5*max(S)));
    M=measurements.center_of_mass(S,SLabels,range(1,SNum+1));
    X=[int(X[0]) for X in M];

    if len(X)==4:
        Dx=diff(X);
        X=[X[0],X[0]+Dx[0]//3,X[0]+2*Dx[0]//3,
            X[1],X[1]+Dx[1]//3,X[1]+2*Dx[1]//3,
            X[2],X[2]+Dx[2]//3,X[2]+2*Dx[2]//3,X[3]];

    if len(X)==10:
        return X;
    else:
        return RuntimeError('Edges Not Detected!');


Features,Labels=LoadOCRData('../ActiveTest/sudoku_images/ocr_data/training/');
TestFeatures,TestLabels=LoadOCRData('../ActiveTest/sudoku_images/ocr_data/testing/');

Features=list(Features);
TestFeatures=list(TestFeatures);

Prob=svm_problem(Labels,Features);
Param=svm_parameter('-t 0');

Model=svm_train(Prob,Param);
Res=svm_predict(Labels,Features,Model);

Res=svm_predict(TestLabels,TestFeatures,Model);

ImgName='../ActiveTest/sudoku_images/sudokus/sudoku18.JPG';
VerName='../ActiveTest/sudoku_images/sudokus/sudoku18.sud';
Img=array(Image.open(ImgName).convert('L'));

X=FindSudokuEdges(Img,axis=0);
Y=FindSudokuEdges(Img,axis=1);

Crops=[];
for Col in range(9):
    for Row in range(9):
        Crop=Img[Y[Col]:Y[Col+1],X[Row]:X[Row+1]];
        Crops.append(ComputeFeature(Crop));

Res=svm_predict(loadtxt(VerName),list(Crops),Model)[0];
ResImg=array(Res).reshape(9,9);

print('Result:');
print(ResImg);
