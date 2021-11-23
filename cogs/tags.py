import discord
from discord.ext import commands
import sqlite3

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #command that takes in a tag and searches for the tag in the Tag column of the sqlite3 database
    #once the tag is found, the text in the corresponding Ref column is sent to the channel
    @commands.command()
    async def tag(self, ctx, *, tag):
        conn = sqlite3.connect('./data/db/database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tags WHERE Tag = ?", (tag,))
        result = c.fetchone()
        if result is None:
            await ctx.send('Tag not found')
        else:
            await ctx.send(result[1])
        conn.close()

    #command that takes in a tag and a text and adds the tag to the Tag column of the sqlite3 database
    #the text is added to the Ref column of the sqlite3 database
    @commands.command()
    async def addtag(self, ctx, *, tag):
        conn = sqlite3.connect('./data/db/database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tags WHERE Tag = ?", (tag,))
        result = c.fetchone()
        if result is None:
            #add a new row with the tag and ask the user what they want the content to be
            await ctx.send('What would you like the content to be?')
            def check(m):
                return m.author == ctx.author
            msg = await self.bot.wait_for('message', check=check)
            c.execute("INSERT INTO tags VALUES (?, ?)", (tag, msg.content))
            conn.commit()

            await ctx.send('Tag added')
        else:
            await ctx.send('Tag already exists')
        conn.close()





def setup(bot):
    bot.add_cog(Tags(bot))