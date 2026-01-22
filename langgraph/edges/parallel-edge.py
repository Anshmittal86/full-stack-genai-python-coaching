from IPython.display import Image, display
import operator
from typing import Annotated, List, Literal, TypedDict
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict):
    nlist: Annotated[List[str], operator.add]

def node_a(state: State):
    print(f"node a is receiving {state['nlist']}")
    note = "A"
    return(State(nlist = [note]))

def node_b(state: State):
    print(f"node b is receiving {state['nlist']}")
    note = "B"
    return(State(nlist = [note]))

def node_c(state: State):
    print(f"node c is receiving {state['nlist']}")
    note = "C"
    return(State(nlist = [note]))

def node_bb(state: State):
    print(f"node bb is receiving {state['nlist']}")
    note = "BB"
    return(State(nlist = [note]))

def node_cc(state: State):
    print(f"node cc is receiving {state['nlist']}")
    note = "CC"
    return(State(nlist = [note]))

def node_d(state: State):
    print(f"node d is receiving {state['nlist']}")
    note = "D"
    return(State(nlist = [note]))
    
# Define a State
graph_builder = StateGraph(State)

# Define a Nodes
graph_builder.add_node("node_a", node_a)
graph_builder.add_node("node_b", node_b)
graph_builder.add_node("node_c", node_c)
graph_builder.add_node("node_bb", node_bb)
graph_builder.add_node("node_cc", node_cc)
graph_builder.add_node("node_d", node_d)

# Define a Edges
graph_builder.add_edge(START, "node_a")
graph_builder.add_edge("node_a", "node_c")
graph_builder.add_edge("node_a", "node_b")
graph_builder.add_edge("node_b", "node_bb")
graph_builder.add_edge("node_c", "node_cc")
graph_builder.add_edge("node_bb", "node_d")
graph_builder.add_edge("node_cc", "node_d")
graph_builder.add_edge("node_d", END)

# Compile a Graph
graph = graph_builder.compile()

# print(graph.get_graph().draw_mermaid())

inital_state = State(
    nlist=["Hey How are you"]
)
 
updated_state = graph.invoke(inital_state)
print(updated_state)