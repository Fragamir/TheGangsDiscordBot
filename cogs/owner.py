from discord.ext import commands

class OwnerCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group("admin")
    async def admin(self, context):
        print(f"{context.message.author.name} ({context.message.author.id}) Invoked a cog command")

    @admin.command("reload", pass_context=True)
    async def reload(self, cog):
        if cog[:5] != "cogs.":
            cog = "cogs." + cog
        msg = extension(self.client.reload_extension, cog)
        await context.send(msg)

    @admin.command("load", pass_context=True)
    async def load(self, cog):
        if cog[:5] != "cogs.":
            cog = "cogs." + cog
        msg = extension(self.client.load_extension, cog)
        await context.send(msg)

    @admin.command("unload", pass_context=True)
    async def unload(self, cog):
        if cog[:5] != "cogs.":
            cog = "cogs." + cog
        msg = extension(self.client.unload_extension, cog)
        await context.send(msg)

        
def extension(func, cog):
    try:
        func(cog)
    except commands.ExtensionFailed:
        return "Extension failed to execute"
    except commands.ExtensionNotLoaded:
        return "Extension not loaded"
    except commands.ExtensionNotFound:
        return f"Extension '{cog}' not found"
    except commands.NoEntryPointError:
        return "Extension got no mf setup function"
    except Exception as e:
        return "Unexpected exception:\n" + str(e)
    return "Extension loaded: "


def setup(client):
    client.add_cog(OwnerCog(client))
