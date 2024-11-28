"""
Set environment variables
"""
from utils import set_env_keys
set_env_keys()
""" 
Chat model langchain directly writes to langsmith for tracing
"""
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o-mini")
from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage("Translate the following from English to Italian"),
    HumanMessage("Charles Leclerc is the Formula 1 world champion!")
]

returned_message = model.invoke(messages)
print(returned_message)

