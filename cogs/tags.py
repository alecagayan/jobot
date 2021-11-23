import discord
from discord.ext import commands
import sqlite3

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tag(self, ctx, *, tag):

        db = sqlite3.connect("./data/db/database.db", check_same_thread=False)
        cur = db.cursor()

        if tag is not None:
            cur.execute(f"SELECT Ref FROM Tags WHERE Tag = ?", (tag,)) 
            result = cur.fetchone()

        cur.close()
        db.close()
        await ctx.send(result)

    @commands.command()
    async def addtag(self, ctx, *, tag):

        db = sqlite3.connect("./data/db/database.db", check_same_thread=False)
        cur = db.cursor()

        if tag is not None:
            print(tag)
            cur.execute(f"SELECT Tag FROM Tags WHERE Tag = ?", (tag,))
            result = cur.fetchone()
            if result is None:

                def check(m):
                    return m.author == ctx.author

                await ctx.send('What would you like the content of `' + tag + '` to be?')
                ref = await self.bot.wait_for('message', check=check)
                cur.execute("INSERT INTO Tags(Tag, Ref) VALUES(?,?)", (tag, ref))

                db.commit()
                cur.close()
                db.close()
            else:
                await ctx.send("That tag already exists!")
    

        
        

def setup(bot):
    bot.add_cog(Tags(bot))