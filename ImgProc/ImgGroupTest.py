import pydot
G=pydot.Dot(graph_type='graph');

G.add_node(pydot.Node(str(0),fontcolor='transparent'));
for i in range(5):
    G.add_node(pydot.Node(str(i+1)));
    G.add_edge(pydot.Edge(str(0),str(i+1)));
    for j in range(5):
        G.add_node(pydot.Node(str(j+1)+'-'+str(i+1)));
        G.add_edge(pydot.Edge(str(j+1)+'-'+str(i+1),str(j+1)));
G.write_png('graph.jpg');
