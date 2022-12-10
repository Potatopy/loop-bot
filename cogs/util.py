import nextcord
import aiohttp
import time
from nextcord.ext import commands
from PIL import Image
from io import BytesIO
import base64

class Dropdown(nextcord.ui.Select):
    def __init__(self, message, images, user):
        self.message = message
        self.images = images
        self.user = user

        options = [
            nextcord.SelectOption(label="1"),
            nextcord.SelectOption(label="2"),
            nextcord.SelectOption(label="3"),
            nextcord.SelectOption(label="4"),
            nextcord.SelectOption(label="5"),
            nextcord.SelectOption(label="6"),
            nextcord.SelectOption(label="7"),
            nextcord.SelectOption(label="8"),
            nextcord.SelectOption(label="9"),
        ]

        super().__init__(
            placeholder="Choose one of the 9 images you want to see!",
            min_values=1, 
            max_values=1, 
            options=options
            )

    async def callback(self, interaction: nextcord.Interaction):
        if not int(self.user) == int(interaction.user.id):
            await interaction.response.send.message("You did not request this image!", ephemeral=True)
        selection = int(self.values[0])-1
        image = BytesIO(base64.decodebytes(self.images[selection].encode("utf-8")))
        return await self.message.edit(content="Content Generated by **craiyon.com** check out the site to try it out yourself!", file=nextcord.File(image, "genImage.png"), view=DropdownView(self.message, self.images, self.user))

class DropdownView(nextcord.ui.View):
    def __init__(self, message, images, user):
        super().__init__()
        self.message = message
        self.images = images
        self.user = user
        self.add_item(Dropdown(self.message, self.images, self.user))

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

    @commands.command()
    async def avatar(self, ctx, member: nextcord.Member = None):
        if member is None:
            member = ctx.author
        em = nextcord.Embed(title=f"{member.name}'s avatar", color=nextcord.Color.purple())
        em.set_image(url=member.display_avatar)
        await ctx.send(embed=em)

    @commands.command()
    async def generate(self, ctx, *, prompt):
        ETA = int(time.time() + 60)
        msg = await ctx.send(f"Generating your image... ETA: <t:{ETA}:R>")
        async with aiohttp.request("POST", "https://backend.craiyon.com/generate", json={"prompt": prompt}) as resp:
            r = await resp.json()
            images = r['images']
            image = BytesIO(base64.b64decode(images[0].encode("utf-8")))
            return await msg.edit(content="Here is your image!", file=nextcord.File(image, "generatedImage.png"), view=DropdownView(msg, images, ctx.author.id))

def setup(bot):
    bot.add_cog(Util(bot))