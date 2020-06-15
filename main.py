import discord
from discord.ext import commands

try:
    version = "0.1"
    config = {}
    with open("static/SecretStuff.txt", "r") as f:
        for line in f:
            config[line.split("::")[0]] = (line.split("::")[1]).replace("\n", "")

    description = "The Gang's discord bot"
    client = commands.Bot(command_prefix="!", description=description, owner_ids=config["OWNER"].split(","))


    async def error(cause, err, item=None):
        if item:
            cause = cause + ": " + item
        msg = f"Failed to {cause}\n*{err}*"
        await output_to_test(msg)


    async def output_to_test(msg):
        channel = client.get_channel(721062998759964682)
        await channel.send(msg)


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
        await output_to_test("Bot restarted and ready")
        await client.change_presence(activity=discord.Game("all these hoes"), status=discord.Status.online)
        initial_ext = ["cogs.train", "cogs.music_finder", "cogs.imbd", "cogs.translate", "cogs.owner", "cogs.meme"]
        for ext in initial_ext:
            try:
                client.load_extension(ext)
            except commands.ExtensionFailed as e:
                await error("load extension", e, ext)
            except Exception as e:
                await error("do something, unexpected error", e, ext)


    client.run("NzE5NjQ4MTAyNTY2MzMwNDE4.Xt6g8w.x2RrYO1bH-I4GIzpB1kp1JkKVus")
except Exception as e:
    print(str(e))
