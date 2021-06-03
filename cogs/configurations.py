import discord
import os
from discord.ext import commands
import asqlite

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

  
def setup(bot):
  bot.add_cog(Configurations(bot))

  
