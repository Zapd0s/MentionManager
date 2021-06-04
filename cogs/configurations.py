import discord
import os
from discord.ext import commands
import asqlite
import sqlite3
from cogs import mentions

class Configurations(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="start", brief="Start logging mentions for your account")
  async def start(self, ctx):
    """
    Creates a database for your Discord where all data is stored
    """
    if os.path.isfile(f'data/{ctx.author.id}.sqlite'):
      await ctx.send("You already have an account!")
      return
    conn = await asqlite.connect(f'data/{ctx.author.id}.sqlite')
    await conn.execute("CREATE TABLE IF NOT EXISTS mentions (guild_id INT, ch_id INT, msg_id INT, pinger INT, content TEXT, created INT)")
    await conn.commit()
    await conn.close()
    await ctx.send("Alright, I will now start storing your mentions!")


  @commands.group(invoke_without_command=True)
  @commands.check(mentions.Mentions.check_for_account)
  async def config(self, ctx):
    embed=discord.Embed(title="Configurations", description="These are the current configurations for your account", color=self.bot.color)
    conn = await asqlite.connect(f'data/{ctx.author.id}.sqlite')
    try:
      res =await conn.fetchone("SELECT * FROM ignore")
      ignore = res[0]
    except sqlite3.OperationalError:
      ignore = "Not setup yet\nDo -config ignore <status> to set it up"
    await conn.commit()
    await conn.close()
    embed.add_field(name="Ignore pings when in particular status", value=ignore)
    await ctx.send(embed=embed)

  @config.command()
  @commands.check(mentions.Mentions.check_for_account)
  async def ignore(self, ctx, status):
    valid = ["dnd", "idle", "online", "offline"]
    if status not in valid:
      await ctx.send(f"The status must be in the following:\n{' or '.join(val for val in valid)}")
      return
    conn = await asqlite.connect(f'data/{ctx.author.id}.sqlite')
    try:
      await conn.execute("SELECT * FROM ignore")
      await conn.execute("UPDATE ignore SET status = (?)", (status,))
    except sqlite3.OperationalError:
      await conn.execute("CREATE TABLE IF NOT EXISTS ignore (status)")
      await conn.execute("INSERT INTO ignore (status) VALUES (?)", (status,))
    await conn.commit()
    await conn.close()
    await ctx.send(f"Okay, whenever you are in {status} status, pings will be ignored")





  
def setup(bot):
  bot.add_cog(Configurations(bot))

  
