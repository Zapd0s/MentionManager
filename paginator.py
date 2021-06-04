from discord.ext import menus
import discord

class MentionPages(menus.ListPageSource):
  
  def __init__(self, data, ctx, per_page):
    super().__init__(data, per_page=per_page)
    self.ctx = ctx
  
  async def format_page(self, menu, item):
    embed = discord.Embed(title = "Recent Mentions", color=discord.Color.from_rgb(255,0,0))
    embed.set_author(name=self.ctx.author, icon_url=self.ctx.author.avatar_url)
    for field in item:
      embed.add_field(name=field.name, value=field.value)
    return embed

  
    
