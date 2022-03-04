from PIL import Image
from numpy import *
from pylab import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame,pygame.image
from pygame.locals import *
import pickle

def SetProjectionFromCamera(K):
    '''从照相机标定矩阵中获得视图'''
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    
    fx=K[0,0]; fy=K[1,1];
    fovy=2*arctan(0.5*height/fy)*180/pi;
    aspect=(width*fy)/(height*fx);

    near=0.1; far=100.0;

    gluPerspective(fovy,aspect,near,far);
    glViewport(0,0,width,height);

def SetModelViewFromCamera(Rt):
	'''从照相机姿态中获得模拟试图矩阵'''
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();

	Rx=array([[1,0,0],[0,0,-1],[0,1,0]]);

	R=Rt[:,:3];
	U,S,V=linalg.svd(R);
	R=dot(U,V);
	R[0,:]=-R[0,:];

	t=Rt[:,3];
	M=eye(4);
	M[:3,:3]=dot(R,Rx);
	M[:3,3]=t;

	M=M.T;
	m=M.flatten();
	glLoadMatrixf(m);

def DrawBackground(ImgName):
	bg_image=pygame.image.load(ImgName).convert();
	bg_data=pygame.image.tostring(bg_image,"RGBX",1);

	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	glEnable(GL_TEXTURE_2D);
	glBindTexture(GL_TEXTURE_2D,glGenTextures(1));
	glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,bg_data);
	glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);
	glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);

	glBegin(GL_QUADS);
	glTexCoord2f(0.0,0.0); glVertex3f(-1.0,-1.0,-1.0);
	glTexCoord2f(1.0,0.0); glVertex3f( 1.0,-1.0,-1.0);
	glTexCoord2f(1.0,1.0); glVertex3f( 1.0, 1.0,-1.0);
	glTexCoord2f(0.0,1.0); glVertex3f(-1.0, 1.0,-1.0);
	glEnd();

	glDeleteTextures(1);

def DrawTeapot(Size):
	glEnable(GL_LIGHTING);
	glEnable(GL_LIGHT0);
	glEnable(GL_DEPTH_TEST);
	glClear(GL_DEPTH_BUFFER_BIT);

	glMaterialfv(GL_FRONT,GL_AMBIENT,[0,0,0,0]);
	glMaterialfv(GL_FRONT,GL_DIFFUSE,[0.5,0.0,0.0,0.0]);
	glMaterialfv(GL_FRONT,GL_SPECULAR,[0.7,0.6,0.6,0.0]);
	glMaterialf(GL_FRONT,GL_SHININESS,0.25*128.0);
	glutSolidTeapot(Size);

width,height=1000,747;

def Setup():
	pygame.init();
	pygame.display.set_mode((width,height),OPENGL | DOUBLEBUF);
	pygame.display.set_caption('OpenGL AR demo');

with open('ar_camera.pkl','rb') as f:
	K=pickle.load(f);
	Rt=pickle.load(f);

Setup();
DrawBackground('../ActiveTest/book_perspective.bmp');
SetProjectionFromCamera(K);
SetModelViewFromCamera(Rt);
DrawTeapot(0.05);

while True:
	event=pygame.event.poll();
	if event.type in (QUIT,KEYDOWN):
		break;
	pygame.display.flip();

