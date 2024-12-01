"""
LangGraph comes with built-in message persistence layer. Let's use that
"""
from langchain_core.messages import HumanMessage

from utils import env_vars
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
env_vars.set_vars()
model = ChatOpenAI(model="gpt-4o-mini")

def call_model(state: MessagesState):
    """
    The state being passed in has a list of messages which is then passed down in the invocation of the model
    :param state: The Langgraph message state
    :return: response of the invocation
    """
    response = model.invoke(state["messages"])
    return {"messages": response}

def main():
    # instantiate the graph
    graph = StateGraph(state_schema=MessagesState)
    # define the starting node in the graph
    graph.add_edge(START, "model")
    graph.add_node("model", call_model)

    # Give your app some memory. This is what enables the app to recall info from your prior conversations
    memory = MemorySaver()
    app = graph.compile(checkpointer=memory)

    output1 = app.invoke(
        {
            "messages": [
                HumanMessage("Hi! I am ricky!")
            ]
        },
        {
            "configurable": {
                "thread_id": "test1"
            }
        }
    )
    print(output1["messages"][-1].pretty_print())

    output2 = app.invoke(
        {
            "messages": [
                HumanMessage("What is my name?")
            ]
        },
        {
            "configurable": {
                "thread_id": "test1"
            }
        }
    )
    print(output2["messages"][-1].pretty_print())

if __name__ == "__main__":
    main()

