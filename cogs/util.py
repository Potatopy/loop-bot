import nextcord
from nextcord.ext import commands

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Util commands are online!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def echo(self, ctx, *, arg = ""):
        if arg == "":
            await ctx.send("Please enter a message to echo")
        else:
            await ctx.send(arg)

def setup(bot):
    bot.add_cog(Util(bot))