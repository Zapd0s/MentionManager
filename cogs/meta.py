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

  @commands.command(name="invite", brief="Gives the bot's invite link")
  async def invite(self, ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=836215664502636554&permissions=354304&scope=bot")
    embed = discord.Embed(title="Invite Link", url="https://discord.com/api/oauth2/authorize?client_id=836215664502636554&permissions=354304&scope=bot", description="Hey, to invite me to your servers, [click here!](https://discord.com/api/oauth2/authorize?client_id=836215664502636554&permissions=354304&scope=bot)", color=self.bot.color)
    await ctx.send(embed=embed)




def setup(bot):
  bot.add_cog(Meta(bot))