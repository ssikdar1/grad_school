abstract sig Node { }

abstract sig Edge{ connects: set Node } { #connects = 2 }
abstract sig DirEdge{ start, end: Node }

one sig A extends Node { }
one sig B extends Node { }
one sig C extends Node { }
one sig D extends Node { }

one sig Edge1 extends Edge {} { connects = A + B }
one sig Edge2 extends Edge {} { connects = C + D }
one sig Edge3 extends Edge {} { connects = B + D }

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

pred connected {
	some p: Path | all n: Node | n in p.step.*nextStep.via.connects
}
// Show that it is not only connected but also connected with a Eulerian path.
run connected for 3 but exactly 1 Path

