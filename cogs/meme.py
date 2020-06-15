from discord.ext import commands

class MemeCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def lyrics(self, context, *rest):



def setup(bot):
    bot.add_cog(MemeCog(bot))
