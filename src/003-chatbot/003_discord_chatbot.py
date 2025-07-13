# Discord imports
import discord
from discord.ext import commands

# Open AI and langchain imports
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

# Langchain setup
model = ChatOpenAI(model="gpt-4o-mini")
def call_model(state: MessagesState):
    """
    The state being passed in has a list of messages which is then passed down in the invocation of the model
    :param state: The Langgraph message state
    :return: response of the invocation
    """
    response = model.invoke(state["messages"])
    return {"messages": response}

graph = StateGraph(state_schema=MessagesState)
# define the starting node in the graph
graph.add_edge(START, "model")
graph.add_node("model", call_model)

# Give your app some memory. This is what enables the app to recall info from your prior conversations
memory = MemorySaver()
app = graph.compile(checkpointer=memory)
config = {
    "configurable": {
        "thread_id": "botv1"
    }
}

# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    await bot.tree.sync()

@bot.tree.command(name="blah", description="Say blah to the human!")
async def blah(interaction: discord.Interaction):
    await interaction.response.send_message(f"Blah! Hello, {interaction.user}")

@bot.tree.command(name="name", description="Say hi to the human!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user}! I'm your first bot ever!")

@bot.tree.command(name="repeat", description="I repeat anything you say")
async def repeat(interaction:discord.Interaction, input: str):
    await interaction.response.send_message(f"Here's what you said: {input}")

@bot.tree.command(name="chat", description="I can chat with you backed by open AI")
async def chat(interaction:discord.Interaction, input: str):
    try:
        result = app.invoke(
            {
                "messages": [
                    HumanMessage(input)
                ]
            },
            config
        )
        await interaction.response.send_message(result["messages"][-1].content)
    except Exception as e:
        print(e)
        await interaction.response.send_message(f'Oops! something went wrong! Please try again later')
# Run the bot
from aws_mgmt import parameters
bot.run(parameters.get_parameter("DISCORD_BOT_V1_TOKEN"))