import discord
from discord.ext import commands
import os
import traceback
import datetime


inital_extensions = (
  "cogs.configurations",
  "cogs.listener",
  "cogs.mentions",
  "cogs.meta",
  "jishaku",
  # "cogs.help" not finished yet!
)


class MentionManager(commands.Bot):
  def __init__(self):
    description = "A simple bot to handle and view your mentions"
    mentions = discord.AllowedMentions(everyone=False, replied_user=False, roles=False, users=False)
    intents = discord.Intents(
      guilds = True,
      members = True,
      messages = True,
      reactions = True
    )
    
    super().__init__(
      command_prefix = "-",
      description = description,
      allowed_mentions = mentions,
      intents = intents
    )

    self.color = discord.Color.from_rgb(255,0,0) # red color

    for file in inital_extensions:
      try:
        self.load_extension(file)
      except Exception as e:
        print(f"Failed to load {file}")
        traceback.print_exc()

  async def on_ready(self):
    self.uptime = datetime.datetime.now()
    print("Bot ready.")

  def run(self):
    token = os.environ["TOKEN"]
    super().run(token)


if __name__ == '__main__':
  bot = MentionManager()
  bot.run()





