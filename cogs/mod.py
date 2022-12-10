import nextcord
from nextcord.ext import commands

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Mod commands are online!')
    
    @commands.command(description='Clears a certain amount of messages')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amt:int):
        await ctx.channel.purge(limit=amt)
        await ctx.send(f"Deleted {amt} messages!", delete_after=5)

    @commands.command(description='Kicks a member')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:nextcord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"get out {member.mention}, Reason: {reason}")

    @commands.command(description='Bans a member')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:nextcord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"smokin that {member.mention} pack 🚬, Reason: {reason}")

    @commands.command(description='Unbans a member')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = ctx.guild.bans()

        async for ban_entry in banned_users:
            user = ban_entry.user
                
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')

    @commands.command(description='Locks a channel/server')
    @commands.has_permissions(manage_guild=True)
    async def lock(self, ctx, channel:nextcord.TextChannel=None, setting=None):
        if setting == '--server':
            for channel in ctx.guild.channels:
                await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.send('Server locked!')
        
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"Locked {channel.mention}")
    
    @commands.command(description='Locks a channel/server')
    @commands.has_permissions(manage_guild=True)
    async def unlock(self, ctx, channel:nextcord.TextChannel=None, setting=None):
        if setting == '--server':
            for channel in ctx.guild.channels:
                await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await ctx.send('Server unlocked!')
        
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"Unlocked {channel.mention}")

def setup(bot):
    bot.add_cog(Mod(bot))