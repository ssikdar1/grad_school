abstract sig Node { }

abstract sig Edge{ connects: set Node } { #connects = 2 }
abstract sig DirEdge{ start, end: Node }

one sig N extends Node { }
one sig E extends Node { }
one sig S extends Node { }
one sig W extends Node { }

one sig Edge1 extends Edge {} { connects = N + W }
one sig Edge2 extends Edge {} { connects = N + W }
one sig Edge3 extends Edge {} { connects = N + E }
one sig Edge4 extends Edge {} { connects = E + W }
one sig Edge5 extends Edge {} { connects = E + S }
one sig Edge6 extends Edge {} { connects = S + W }
one sig Edge7 extends Edge {} { connects = S + W }

one sig Edge8 extends Edge {} { connects = E + W }

sig Path { step: Step}
sig Step {
     from, to: Node,
     via: Edge,
     nextStep: lone Step
} { via.connects = from + to }

fact {
     all curr:Step, next:curr.nextStep | next.from = curr.to
}

fun steps ( p: Path ): set Step {
	p.step.*nextStep
}

// Eulerian path
pred path() {
	some p:Path | steps[p].via = Edge
}

/* There exists a path for all nodes such that all nodes are in the path
	If there was no path that contains all the nodes then the there must be somthing making it disconnected.
		And no instance was found.
	Test 1: Seven Bridges as is passes
	Test 2: One isolated node: fails
	Test 3: 2 dijoint connected components: fail
	Test 4: connect the two disjoint componenets: passes
*/
pred connected {
	some p: Path | all n: Node | n in p.step.*nextStep.via.connects
}

// running the path for 8 because running the path for more than 8 means you can go over a bridge twice
run {path and connected} for 8 but exactly 1 Path

