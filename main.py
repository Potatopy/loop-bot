# Dependencies

import discord
import os
import asyncio
from discord.ext import commands
from discord import File
from easy_pil import Editor, load_image_async, Font
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

# Load all cogs
async def load():
    for fn in os.listdir('./cogs'):
        if fn.endswith('.py'):
            await bot.load_extension(f'cogs.{fn[:-3]}')


@bot.event
async def on_ready():
    activity = discord.Activity(name='.gg/loop', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    print(f"Bot is online || Logged in as {bot.user} ID: {bot.user.id}")


@bot.event
async def on_member_join(member):
    # Channel to send the welcome message
    channel = member.guild.system_channel

    # Background img
    background = Editor("img/pic2.jpg")
    profile_image = await load_image_async(member.display_avatar.url)

    # Fonts / customization (you can change the fonts to whatever you want)
    profile = Editor(profile_image).resize((150, 150)).circle_image()
    poppins = Font.poppins(size=50, variant="bold")
    poppins_small = Font.poppins(size=20, variant="light")

    # Background image + text
    background.paste(profile, (325, 90))
    background.ellipse((325, 90), 150, 150, outline="white", stroke_width=5)
    background.text((400, 260), f"Welcome to /loop", color="white", font=poppins, align="center")
    background.text((400, 325), f"{member.name}#{member.discriminator}", color="white", font=poppins_small,
                    align="center")
    file = File(fp=background.image_bytes, filename="pic2.jpg")

    await channel.send(f"Welcome {member.mention} to /loop", file=file)


@bot.command()
async def load_ext(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded {extension} cog')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloaded {extension} cog')


@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f'Reloaded {extension} cog')


async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())
