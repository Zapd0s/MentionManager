import discord
from discord.ext import commands
import time

class Meta(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="ping", brief="Gives the bot's latency")
  async def ping(self, ctx):
    """
    Gives information about the response time and latency of the bot.
    """
    start = time.perf_counter()
    a = await ctx.send("Pinging...")
    end = time.perf_counter()
    dur = (end-start) * 1000
    embed = discord.Embed(title = "Pong!", description = f"**Response Time** \n ```{dur:.2f}ms```\n **Websocket Latency** \n ```{round(((self.bot.latency) * 1000), 2)}ms```", color = self.bot.color)
    await a.edit(embed = embed)


def setup(bot):
  bot.add_cog(Meta(bot))