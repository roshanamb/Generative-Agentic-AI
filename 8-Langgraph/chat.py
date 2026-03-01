from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_community.chat_models import init_chat_model

llm = init_chat_model(
    model="gpt-3.5-turbo",
    model_Provider="openai",
)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State) -> str:
    # print("\n\nChatbot node executed with state:", state)
    response = llm.invoke(state["messages"])
    return {"messages" : [response.content]}

def samplenode(state: State) -> str:
    print("\n\nSample node executed with state:", state)
    return {"messages" : ["Hi, this is a message from sample node!"]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode") 
graph_builder.add_edge("samplenode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State(messages=["Hi, this is the initial message!"]))
print("\n\nUpdated state after graph execution:", updated_state)
