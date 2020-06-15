import discord
from discord.ext import commands
import os

version = os.environ["VERSION"]

description = "The Gang's discord bot"
client = commands.Bot(command_prefix="!", description=description, owner_ids=os.environ["OWNERS"].split(","))

@client.event
async def on_ready():
    print(f"\nBot started as: {client.user.name} ({client.user.id}) - Version: {version}")
    await client.change_presence(activity=discord.Game("all these hoes"), status=discord.Status.online)
    initial_ext = ["cogs."+x for x in os.environ.get("INITIAL_EXT").split(",")]
    for ext in initial_ext:
        try:
            client.load_extension(ext)
        except commands.ExtensionFailed as e:
             print("Failed to load extension", str(e), ext)
        except Exception as e:
            print("Failed to do something, unexpected error", str(e), ext)


client.run(os.environ.get("SECRET"))
