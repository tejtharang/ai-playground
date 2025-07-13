from typing import Literal
import random

from langgraph.graph import StateGraph, START, END

def action_1(state: dict) -> dict:
    state['value'] = state['value'] + 1
    return state

def action_2(state: dict) -> dict:
    state['value'] = state['value'] * 2
    return state

def action_3(state: dict) -> dict:
    state['value'] = state['value'] * 3
    return state

def decide(state: dict) -> Literal["node_2", "node_3"]:
    if random.random() < 0.5:
        return "node_2"
    return "node_3"

# build your graph
builder = StateGraph(dict)
builder.add_node("node_1", action_1)
builder.add_node("node_2", action_2)
builder.add_node("node_3", action_3)

builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()
result = graph.invoke({ 'value' : 0 })
print(result)



