import discord
from discord.ext import commands
import os

version = os.environ["VERSION"]

description = "The Gang's discord bot"
client = commands.Bot(command_prefix="!", description=description, owner_ids=os.environ["OWNERS"].split(","))


async def split_send(context, string):
    out = []
    split_string = string.split("\n")
    dictionary = {}
    for count in range(0, len(split_string)-1):
        dictionary[str(count)] = [split_string[count], len(split_string[count])]
    start = 0
    while True:
        try:
            interstart = start
            count = 0
            while count < 2001:
                count += dictionary[str(interstart)][1]
            interstart -= 1
            msg = ""
            for count in range(start, interstart):
                msg += dictionary[str(count)][0]
            out.append(msg)
        except IndexError:
            break
    for message in out:
        await context.send(message)


@client.event
async def on_ready():
    print(f"\nBot started as: {client.user.name} ({client.user.id}) - Version: {version}")
    await client.change_presence(activity=discord.Game("all these hoes"), status=discord.Status.online)
    # initial_ext = ["cogs.train", "cogs.music_finder", "cogs.imbd", "cogs.translate", "cogs.owner", "cogs.meme"]
    initial_ext = ["cogs."+x for x in os.environ.get("INITIAL_EXT").split(",")]
    for ext in initial_ext:
        try:
            client.load_extension(ext)
        except commands.ExtensionFailed as e:
             print("Failed to load extension", str(e), ext)
        except Exception as e:
            print("Failed to do something, unexpected error", str(e), ext)


client.run(os.environ.get("SECRET"))
