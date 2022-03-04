import cv2

Img=cv2.imread('../ActiveTest/empire.jpg');
H,W=Img.shape[:2]
print(H,W);

cv2.imwrite('../ActiveTest/EMPIRE.png',Img);

