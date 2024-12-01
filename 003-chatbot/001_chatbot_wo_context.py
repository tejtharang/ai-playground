"""
One of the most important parts of a chatbot is the ability to recall information from the conversation.
See below an example of a chat where historical conversation is not recalled. Such a chatbot is not useful.
"""
from utils import env_vars
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

def main():
    env_vars.set_vars()
    model = ChatOpenAI(model="gpt-4o-mini")
    response1 = model.invoke(
        [
            HumanMessage("Hi! I am Ricky!")
        ]
    )
    print(response1.content)
    response2 = model.invoke(
        [
            HumanMessage("What is my name?")
        ]
    )
    print(response2.content)

if __name__ == "__main__":
    main()