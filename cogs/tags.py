import discord
from discord.ext import commands
import sqlite3
import spacy
nlp = spacy.load('en_core_web_lg')

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tag(self, ctx, *, tag):

        conn = sqlite3.connect('./data/db/database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tags")
        results = c.fetchall()
        max_similarity = 0
        max_tag = ""
        for result in results:
            similarity = nlp(tag).similarity(nlp(result[0]))
            if similarity > max_similarity:
                max_similarity = similarity
                max_tag = result

        #send embed with title being max_tag[0] and description being max_tag[1], and a related image from the internet
        embed = discord.Embed(title=max_tag[0].title(), description=max_tag[1], color=0x57F287)
        await ctx.send(embed=embed)
    

    @commands.command(alias=['tags'])
    async def printall(self, ctx):
        conn = sqlite3.connect('./data/db/database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tags")
        result = c.fetchall()
        for row in result:
            await ctx.send(row[0] + " : " + row[1])
        conn.close()

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

    @commands.command()
    async def removetag(self, ctx, *, tag):
        conn = sqlite3.connect('./data/db/database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tags WHERE Tag = ?", (tag,))
        result = c.fetchone()
        if result is None:
            await ctx.send('Tag does not exist')
        else:
            c.execute("DELETE FROM tags WHERE Tag = ?", (tag,))
            conn.commit()
            await ctx.send('Tag removed')
        conn.close()

    @commands.command()
    async def edit(self, ctx, *, tag):
        conn = sqlite3.connect('./data/db/database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tags WHERE Tag = ?", (tag,))
        result = c.fetchone()
        if result is None:
            await ctx.send('Tag does not exist')
        else:
            await ctx.send('What would you like the content to be?')
            def check(m):
                return m.author == ctx.author
            msg = await self.bot.wait_for('message', check=check)
            c.execute("UPDATE tags SET Ref = ? WHERE Tag = ?", (msg.content, tag))
            conn.commit()
            await ctx.send('Tag updated')
        conn.close()

def setup(bot):
    bot.add_cog(Tags(bot))