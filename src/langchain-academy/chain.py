from langchain_core.runnables.config import CONFIG_KEYS
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, AnyMessage, SystemMessage
from langgraph.graph.message import add_messages

# This is how typical interactions work
# messages = [AIMessage(content="Hi! How can I assist you today?", name="Bujji"), HumanMessage(content="Hi! My name is Ricky", name="Ricky")]
# for m in messages:
#     m.pretty_print()
#
llm = ChatOpenAI(model="gpt-4o-mini")
# result = llm.invoke(messages)
# #print(result)

# TOOLS
def multiply(a: int, b: int) -> int:
    """
    :param a: first int
    :param b: second int
    :return: a * b
    """
    return a * b

llm_with_tools = llm.bind_tools([multiply])

#tool_call = llm_with_tools.invoke([HumanMessage(content = "What is 2 multiplied by 3?", name = "Ricky")])
# So far it hasn't printed out the results so I don't know. It has only invoked the tool but hasn't used it.
#print(tool_call)

# REDUCERS
# Reducers help us incrementally roll up messages

# new_ai_message = AIMessage(content="Hi, Ricky! How can I help you today ?", name="Bujji")
# messages = add_messages(messages, new_ai_message)

# This is how add_messages works. To abstract this away, Langgraph has build a MessagesState class which will roll up the messages as we use it.
# We just have to update the messages parameter there.

def tool_calling_llm(state: MessagesState):
    return {
        "messages": [llm_with_tools.invoke(state["messages"])]
    }

builder = StateGraph(state_schema=MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_edge(START, "tool_calling_llm")
builder.add_edge( "tool_calling_llm", END)

graph = builder.compile()
graph.invoke(dict(messages = [HumanMessage(content="Hi! My name is Ricky!", name="Ricky")]))
graph.invoke(dict(messages = [HumanMessage(content="What is my name?", name="Ricky")]))
accumulated_messages = graph.invoke(dict(messages = [HumanMessage(content="What is 2 multiplied by 3 ?", name="Ricky")]))
for m in accumulated_messages["messages"]:
    m.pretty_print()

# ROUTER
# Now we've established that the tool call is being made. What we have to do is use the tool if the tool call is being made or else do something else
# from langgraph.prebuilt import ToolNode
# from langgraph.prebuilt import tools_condition
#
# builder = StateGraph(MessagesState)
# builder.add_node("tool_calling_llm", tool_calling_llm)
# builder.add_node("tools", ToolNode([multiply]))
#
# builder.add_edge(START, "tool_calling_llm")
# # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
# # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
# builder.add_conditional_edges("tool_calling_llm", tools_condition)
# builder.add_edge("tools", END)
# graph = builder.compile()
# accumulated_messages = graph.invoke(dict(messages = [HumanMessage(content="What is 2 multiplied by 3 ?", name="Ricky")]))
# for m in accumulated_messages["messages"]:
#     m.pretty_print()
#
# # AGENT
# # We basically need to let the agent decide which route it wants to take. So, after calling the tool. Let's make the agent decide what to do.
# # Introduce a couple more tools to induce some complexity
#
# def add(a: int, b: int) -> int:
#     """
#     :param a:
#     :param b:
#     :return: a + b
#     """
#     return a + b
#
# def subtract(a: int, b : int) -> int:
#     """
#     :param a:
#     :param b:
#     :return: a - b
#     """
#     return a - b
#
# llm = ChatOpenAI(model="gpt-4o-mini")
# llm_with_tools = llm.bind_tools([add, multiply, subtract])
# sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")
# def assistant(state: MessagesState):
#     return {
#         "messages" : [llm_with_tools.invoke([sys_msg] + state["messages"])]
#     }
#
# builder = StateGraph(MessagesState)
# builder.add_node("assistant", assistant)
# builder.add_node("tools", ToolNode([add, multiply, subtract]))
# builder.add_edge(START, "assistant")
# builder.add_conditional_edges("assistant", tools_condition)
# builder.add_edge("tools", "assistant")
# graph = builder.compile()
#
# graph.invoke({
#     "messages": [
#         HumanMessage(content="What is 2 multiplied by 3 plus 10 subtracted by 5 ?", name="Ricky")
#     ]
# })
# messages = graph.invoke({
#     "messages": [
#         HumanMessage(content="What was my previous query ?", name="Ricky")
#     ]
# })
# for m in messages["messages"]:
#     m.pretty_print()
#
# ## MEMORY
# # As soon as teh graph ends, there is no recollection of any questions

from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
config = {
    "configurable": {
        "thread_id": "1"
    }
}
graph.invoke(
    {
        "messages": [
            HumanMessage(content="What is 2 multiplied by 3 plus 10 subtracted by 5 ?", name="Ricky")
        ]
    },
    config
)

messages = graph.invoke(
    {
        "messages": [
            HumanMessage(content="What was the previous result ?", name="Ricky")
        ]
    },
    config
)

for m in messages["messages"]:
    m.pretty_print()
