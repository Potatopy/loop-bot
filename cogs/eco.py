import nextcord
import asyncio
import aiosqlite
import random
from nextcord.ext import commands

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy cog is ready")
        db = await aiosqlite.connect("bank.db")
        await asyncio.sleep(3)
        async with db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS bank (wallet INT, bank INT, maxbank INT, user INT)")
        await db.commit()

    async def create_balance(self, user):
        db = await aiosqlite.connect("bank.db")
        async with db.cursor() as cursor:
            await cursor.execute("INSERT INTO bank VALUES (?, ?, ?, ?)", (0, 100, 25000, user.id))
        await db.commit()
        return

    async def get_balance(self, user):
        db = await aiosqlite.connect("bank.db")
        async with db.cursor() as cursor:
            await cursor.execute("SELECT wallet, bank, maxbank FROM bank WHERE user = ?", (user.id,))
            data = await cursor.fetchone()
            if data is None:
                await self.create_balance(user)
                return 0, 100, 25000
            wallet, bank, maxbank = data[0], data[1], data[2]
            return wallet, bank, maxbank

    async def update_wallet(self, user, amt: int):
        db = await aiosqlite.connect("bank.db")
        async with db.cursor() as cursor:
            await cursor.execute("SELECT wallet FROM bank WHERE user = ?", (user.id,))
            data = await cursor.fetchone()
            if data is None:
                await self.create_balance(user)
                return 0
            await cursor.execute("UPDATE bank SET wallet = ? WHERE user = ?", (data[0] + amt, user.id))
            await db.commit()
    
    async def update_bank(self, user, amt):
        db = await aiosqlite.connect("bank.db")
        async with db.cursor() as cursor:
            await cursor.execute("SELECT wallet, bank, maxbank FROM bank WHERE user = ?", (user.id,))
            data = await cursor.fetchone()
            if data is None:
                await self.create_balance(user)
                return 0
            capacity = int(data[2] -  data[1])
            if amt > capacity:
                await self.update_wallet(self, user, amt)
                return 1
            await cursor.execute("UPDATE bank SET bank = ? WHERE user = ?", (data[1] + amt, user.id))
            await db.commit() 
    
    @commands.command(aliases=['bal', 'money', 'cash', 'coins'])
    async def balance(self, ctx, member: nextcord.Member = None):
        if not member:
            member = ctx.author
        wallet, bank, maxbank = await self.get_balance(member)
        em = nextcord.Embed(title=f"{member.name}'s balance", color=nextcord.Color.green())
        em.add_field(name="Wallet", value=f"${wallet}")
        em.add_field(name="Bank", value=f"${bank} / ${maxbank}")
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def beg(self, ctx):
        chances = random.randint(1, 4)
        if chances == 1:
            return await ctx.send("all the humiliiation and none of the reward - Stewie Griffin")
        amount = random.randint(5, 300)
        res = await self.update_wallet(ctx.author, amount)
        if res == 0:
            return await ctx.send('you are not in our database, run the command again we added you ;)')
        await ctx.send(f"you begged and got ${amount}")

    @commands.command(aliases=['wd'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def withdraw(self, ctx, amt: int):
        wallet, bank, maxbank = await self.get_balance(ctx.author)
        try:
            amount = int(amt)
        except ValueError:
            pass
        if type(amount) == str:
            if amount.lower() == "max" or amount.lower() == "all":
                amount = int(bank)
        else:
            amount = int(amount)

        bank_res = await self.update_bank(ctx.author, -amount)
        wallet_res = await self.update_wallet(ctx.author, +amount)
        if bank_res == 0 or wallet_res == 0:
            return await ctx.send("you are not in our database, run the command again we added you ;)")

        wallet, bank, maxbank = await self.get_balance(ctx.author)
        em = nextcord.Embed(title=f"${amount} has been withdrew", color=nextcord.Color.green())
        em.add_field(name="New Wallet", value=f"${wallet}")
        em.add_field(name="New Bank", value=f"${bank} / ${maxbank}")
        await ctx.send(embed=em)

    @commands.command(aliases=['dep'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deposit(self, ctx, amt: int):
        wallet, bank, maxbank = await self.get_balance(ctx.author)
        try:
            amount = int(amt)
        except ValueError:
            pass
        if type(amount) == str:
            if amount.lower() == "max" or amount.lower() == "all":
                amount = int(wallet)
        else:
            amount = int(amount)

        bank_res = await self.update_bank(ctx.author, amount)
        wallet_res = await self.update_wallet(ctx.author, -amount)
        if bank_res == 0 or wallet_res == 0:
            return await ctx.send("you are not in our database, run the command again we added you ;)")
        elif bank_res == 1:
            return await ctx.send("ur poor lol")

        wallet, bank, maxbank = await self.get_balance(ctx.author)
        em = nextcord.Embed(title=f"${amount} has been deposited", color=nextcord.Color.green())
        em.add_field(name="New Wallet", value=f"${wallet}")
        em.add_field(name="New Bank", value=f"${bank} / ${maxbank}")
        await ctx.send(embed=em)

    @commands.command(aliases=['donate'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def give(self, ctx, member: nextcord.Member, amt):
        wallet, bank, maxbank = await self.get_balance(ctx.author)
        try:
            amount = int(amt)
        except ValueError:
            pass
        if type(amount) == str:
            if amount.lower() == "max" or amount.lower() == "all":
                amount = int(wallet)
        else:
            amount = int(amount)

        wallet_res = await self.update_wallet(ctx.author, -amount)
        wallet_res2 = await self.update_wallet(member, amount)
        if wallet_res == 0 or wallet_res2 == 0:
            return await ctx.send("you are not in our database, run the command again we added you ;)")

        wallet2, bank2, maxbank2 = await self.get_balance(member)

        em = nextcord.Embed(title=f"${amount} coins given to {member.name}", color=nextcord.Color.green())
        em.add_field(name=f"{ctx.author.name}'s New Wallet", value=f"${wallet}")
        em.add_field(name=f"{member.name}'s New Wallet", value=f"${wallet2}")

        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Economy(bot))