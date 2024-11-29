"""
Set environment variables
"""
from utils import env_vars
env_vars.set_vars()

"""
Langsmith wrapper to enable tracing example
"""
import openai
from langsmith.wrappers import wrap_openai
from langsmith import traceable

# Enable tracing on open AI client
client = wrap_openai(openai.Client())

# You can add any function to the trace using traceable
@traceable
def pipeline(user_input: str):
    result = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        model="gpt-4o-mini"
    )
    return result.choices[0].message.content

print(pipeline("Hello, my name is Ria!"))

