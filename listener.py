import discord
from discord.ext import commands
import asqlite
import datetime
import os

class Manager(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  
  @commands.Cog.listener('on_message')
  async def log_pings(self, message:discord.Message):
    if not message.mentions:
      return
    if not message.guild:
      return
    for member in message.mentions:
      if not os.path.isfile(f'data/{member.id}.sqlite'):
        continue
      try:
        conn = await asqlite.connect(f'data/{member.id}.sqlite')
      except Exception:
        return # (guild_id INT, ch_id INT, msg_id INT, pinger INT, content TEXT, created INT)
      else:
        timestamp = datetime.datetime.timestamp(message.created_at)
        await conn.execute("INSERT INTO mentions (guild_id, ch_id, msg_id, pinger, content, created) VALUES (?,?,?,?,?,?)", (message.guild.id, message.channel.id, message.id, message.author.id, message.content, timestamp))
        await conn.commit()
        await conn.close()

      
def setup(bot):
  bot.add_cog(Manager(bot))