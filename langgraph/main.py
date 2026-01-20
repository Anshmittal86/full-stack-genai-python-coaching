from typing_extensions import TypedDict
from langgraph.graph import START, StateGraph
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

class State(TypedDict):
    text: str
    
user_query = "Hello How are you?"
    
def llM_call(state: State) -> dict:
    """ Call a LLM to response the user query """
    
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
            { "role": "system", "content": "You are a helpful assistant." },
            { "role": "user", "content": user_query }
        ]
    )
    return {"text": state["text"] + response.choices[0].message.content}

graph_builder = StateGraph(State)

# Add node to a graph
graph_builder.add_node("node_a", llM_call)

# Add START edge to node
graph_builder.add_edge(START, "node_a")

print(graph_builder.compile().invoke({"text": ""}))