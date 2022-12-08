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

    @commands.command(aliases=['about'])
    async def info(self, ctx):
        em = nextcord.Embed(title="Info", description="This bot was made by domain#0001. This bot is opened sourced and still in development if you want the link to the repository on github her you go: https://github.com/Potatopy/loop-bot. Enjoy ;)", color=nextcord.Color.purple())
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Util(bot))