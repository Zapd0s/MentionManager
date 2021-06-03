from discord.ext import commands


class HelpCog(commands.Cog):
  def __init__(self, bot):
    self._original_help_command = bot.help_command
    bot.help_command = None

  def cog_unload(self):
    self.bot.help_command = self._original_help_command


  @commands.command()
  async def help(self, ctx):
    pass


def setup(bot):
  bot.add_cog(HelpCog(bot))