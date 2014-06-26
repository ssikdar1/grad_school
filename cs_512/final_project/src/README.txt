README:
Graph.als


Noah McCarn and Shan Sikdar




program 1: SevenBridges.als
The Konigsburg Bridge Problem is already set up. Just execute the script and the Alloy initializer will try to find a path that goes through all the bridges (or edges) 
and crossing each bridge (edge) only once. An Instance will not be found since there is no path that crosses all bridges only once.



program 2: EightBridges.als
Same as seven bridges with the smallest possible change being that we addded an extra bridge, that goes from the East Node to the West.
Just execute the script and the Alloy initializer will try to find a path that goes through all the bridges (or edges) 
and crossing each bridge (edge) only once. An Instance will be found since there is a path that crosses all bridges only once.

program 3: DisconnectedGraph.als
A Disconnected Graph
This program demonstrates that our conditions for conectedness works. The test case here is a disconnected graph. 
Here alloy will not be able to find an instance for the model since the graph is not connected.
e.g
	A	C
	|	|
	B	D

program 4: ConnectedGraph.als
A Connected Graph.
This program demonstrates that our conditions for conectedness works. The test case here is a connected graph. 
Here alloy will be able to find an instance for the model since the graph is connected.
e.g
	A	C
	|	|
	B-------D