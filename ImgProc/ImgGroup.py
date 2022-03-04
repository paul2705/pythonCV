import pydot
from PIL import Image
from numpy import *
from pylab import *
from ImgMatch import *

threshold=2;

Path="/Users/duanlingbo/Desktop/WORK/2021春季PRP02-06/TEST/";
G=pydot.Dot(graph_type="graph");
for i in range(NumImg):
    for j in range(i+1,NumImg):
        if MatchScores[i,j]>threshold:
            Img=Image.open(ImgList[i]);
            Img.thumbnail((100,100));
            FileName="../GroupImg/"+str(i)+'.png';
            Img.save(FileName);
            print(Path+FileName[3:]);
            G.add_node(pydot.Node(str(i),fontcolor='transparent',shape='rectangle',image=Path+FileName[3:]));

            Img=Image.open(ImgList[j]);
            Img.thumbnail((100,100));
            FileName="../GroupImg/"+str(j)+'.png';
            Img.save(FileName);
            print(Path+FileName[3:]);
            G.add_node(pydot.Node(str(j),fontcolor='transparent',shape='rectangle',image=Path+FileName[3:]));

            G.add_edge(pydot.Edge(str(i),str(j)));

G.write_png('../GroupImg/Group.png');


