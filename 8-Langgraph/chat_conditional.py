from typing_extensions import TypedDict
from typing import Literal, Optional
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_community.chat_models import init_chat_model

llm = init_chat_model(
    model="gpt-3.5-turbo",
    model_Provider="openai",
)

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good : Optional[bool]

def chatbot(state: State):
    response = llm.invoke(state["user_query"])
    state["llm_output"] = response.content
    return state

def evaluation_node(state: State) -> Literal["samplenode", "endnode"]:
    if True:
        return END
    
    return "samplenode"

def samplenode(state: State) -> State:
    response = llm.invoke("Please provide a better response to the user query: " + state["user_query"])
    state["llm_output"] = response.content
    return state

def endnode(state: State):
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluation_node)
graph_builder.add_edge("samplenode", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State(user_query="Hi, this is the initial message!"))
print("\n\nUpdated state after graph execution:", updated_state)
