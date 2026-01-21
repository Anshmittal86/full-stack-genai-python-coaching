from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model="gpt-4o-mini",
    model_provider="openai"
)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    print("\n\n\nInside chatbot node: ", state)
    response = llm.invoke(state.get("messages", []))
    return { "messages": [response] }

def samplenode(state: State):
    print("\n\n\nInside samplenode node: ", state)
    return { "messages": ["Hi, This is a message from SampleNode"] }

# Create a state graph
graph_builder = StateGraph(State)

# Define nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)

# Define edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

# Compile the graph
graph = graph_builder.compile()

# Execute the graph with an initial state
updated_state = graph.invoke(State({"messages": ["Hi , My name is Ansh Mittal"]}))
print("\n\n\nUpdated State: ", updated_state)


# (START) -> chatbot -> samplenode -> (END)

# state = { messages: ["Hey there"] }
# node chatbot(state: ["Hey There"]) -> { messages: ["Hi, This is a message from ChatBot Node"] }
# state = { messages: ["Hey there", "Hi, This is a message from ChatBot Node"] }