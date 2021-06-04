import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener('on_command_error')
  async def handler(self, ctx, error):
    if hasattr(ctx.command, 'on_error'):
      return


    if isinstance(error, commands.errors.CheckFailure):
      await ctx.send("Uh oh! You don't seem to have an account registered! Do -start to create one")
      return
      

def setup(bot):
  bot.add_cog(ErrorHandler(bot))
