import nextcord
import os
from nextcord.ext import commands
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
mongo = os.getenv('MONGO_DB')

bot_channel = 1049886726199455794 # bot channel
talk_channels = [1049886706280714302] # channels where you can gain xp

level = ["lvl 5", "lvl 10", "lvl 25", "lvl 50 (vip perks)"] # roles to give out (CHANGE THIS TO YOUR OWN ROLES + must be in the same order as levelnum)
levelnum = [5, 10, 25, 50] # level to give out the role

cluster = MongoClient(mongo)

leveling = cluster["discord"]["leveling"]

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Leveling system is online!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in talk_channels:
            stats = leveling.find_one({"id": message.author.id})
            if not message.author.bot:
                if stats is None:
                    newuser = {"id": message.author.id, "xp": 100}
                    leveling.insert_one(newuser)
                else:
                    xp = stats["xp"] + 5
                    leveling.update_one({"id": message.author.id}, {"$set": {"xp": xp}})
                    lvl = 0
                    while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    if xp == 0:
                        await message.channel.send(f"{message.author.mention} has leveled up to **{lvl}**!")
                        for i in range(len(level)):
                            if lvl == levelnum[i]:
                                await message.author.add_roles(nextcord.utils.get(message.author.guild.roles, name=level[i]))
                                em = nextcord.Embed(description=f"{message.author.mention} now has the {level[1]} role check out <#1049892987070590996> to see what you got!")
                                em.set_thumbnail(url=message.author.display_avatar)
                                await message.channel.send(embed=em)

    @commands.command(aliases=['lvl', 'level', 'r'])
    async def rank(self, ctx):
        if ctx.channel.id == bot_channel:
            stats = leveling.find_one({"id": ctx.author.id})
            if stats is None:
                await ctx.send("You haven't sent anything. Say something to get started!")
            else:
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                    if xp < ((50*(lvl**2))+(50*lvl)):
                        break
                    lvl += 1
                xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                boxes = int((xp/(200*((1/2)*lvl)))*20)
                rankings = leveling.find().sort("xp", -1)
                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                em = nextcord.Embed(title="{}'s rank".format(ctx.author.name))
                em.add_field(name="User", value=ctx.author.mention, inline=True)
                em.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
                em.add_field(name="Rank", value=f"{rank}", inline=True)
                em.add_field(name="Progress bar [lvl]", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=True)
                em.set_thumbnail(url=ctx.author.display_avatar)
                await ctx.send(embed=em)

    @commands.command(aliases=['lb', 'leaderboard'])
    async def top(self, ctx):
        if (ctx.channel.id == bot_channel):
            rankings = leveling.find().sort("xp", -1)
            i = 1
            em = nextcord.Embed(title="Rankings:")
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    em.add_field(name=f"{i}: {temp.name}", value=f"Total XP: {tempxp}", inline=False)
                    i += 1
                except:
                    pass
                if i == 11:
                    break
            await ctx.send(embed=em)
            
def setup(bot):
    bot.add_cog(Level(bot))