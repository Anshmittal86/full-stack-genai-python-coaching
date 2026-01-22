from IPython.display import Image, display
import operator
from typing import Annotated, List, Literal, TypedDict
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

class State(TypedDict):
    nlist : Annotated[list[str], operator.add]  

def node_a(state: State) -> Command[Literal["b", "c", END]]:
    print(f"node a is receiving {state['nlist']}")
    select = state["nlist"][-1]
    if select == "b":
        next_node = "b"
    elif select == "c":
        next_node = "c"
    elif select == "q":
        next_node = END
    else:
        next_node = END

    return Command(
        update = State(nlist = [select]),
        goto = [next_node]
    )  

def node_b(state: State) -> State:
    print(f"node b is receiving {state['nlist']}")
    note = "B"
    return(State(nlist = [note]))

def node_c(state: State) -> State:
    print(f"node c is receiving {state['nlist']}")
    note = "C"
    return(State(nlist = [note]))

# def conditional_edge(state: State) -> Literal["b", "c", END]:
#     select = state["nlist"][-1]
#     if select == "b":
#         return "b"
#     elif select == "c":
#         return "c"
#     elif select == "q":
#         return END
#     else:
#         return END
    
builder = StateGraph(State)

# Add nodes
builder.add_node("a", node_a)
builder.add_node("b", node_b)
builder.add_node("c", node_c)

# Add edges
builder.add_edge(START, "a")
# builder.add_conditional_edges("a", conditional_edge)
builder.add_edge("b", END)
builder.add_edge("c", END)

graph = builder.compile()
print(graph.get_graph().draw_mermaid())

while True:
    user = input('b, c, or q to quit: ')
    print(user)
    input_state = State(nlist = [user])
    result = graph.invoke(input_state)
    print( result )
    if result['nlist'][-1] == "q":
        print("quit")
        break