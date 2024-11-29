from utils import env_vars
env_vars.set_vars()

"""
In my own words:

The input to the LLM has to come from somewhere - usually this is system generated or user input.
Prompt Templates help with proper conversion of these to a list of messages to be passed to the LLM
"""

from langchain_core.prompts import ChatPromptTemplate
system_template = "Translate the following from English to {language}"
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system",system_template),
        ("user", "{text}")
    ]
)

prompt = prompt_template.invoke({"language": "Italian", "text": "I love Italy!"})
print(prompt)
print("-------------------------------\n")
print(prompt.to_messages())
print("-------------------------------\n")

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model = "gpt-4o-mini")
response = model.invoke(prompt)
print(response.content)