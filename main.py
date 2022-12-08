# Dependancies
import nextcord
import os
from nextcord.ext import commands
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='.', intents=nextcord.Intents.all())

# Load all cogs
for fn in os.listdir('./cogs'):
    if fn.endswith('.py'):
        bot.load_extension(f'cogs.{fn[:-3]}')

@bot.event
async def on_ready():
    activity = nextcord.Activity(name='.gg/loop', type=nextcord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    print(f"Bot is online || Logged in as {bot.user} ID: {bot.user.id}")

@bot.command()
async def load(ctx, extension):
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

bot.run(TOKEN)