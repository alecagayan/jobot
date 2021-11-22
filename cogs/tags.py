import discord
from discord.ext import commands

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tag(self, ctx, *, tag):
        await ctx.send('hi')

def setup(bot):
    bot.add_cog(Tags(bot))