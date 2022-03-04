from PIL import Image
from numpy import *
from pylab import *
from scipy.ndimage import measurements,morphology

Img=array(Image.open("../ActiveTest/Active.jpg").convert('L'));
ImgOpen=morphology.binary_opening(Img,ones((9,5)),iterations=2);

Labels,NumObjects=measurements.label(ImgOpen);

figure(); imshow(ImgOpen); title(f"Number of objects: {NumObjects}");
show();

imsave("../ActiveTest/ImgMorphology.jpg",ImgOpen);

