import discord
from discord.ext import commands
import os
import asqlite
import humanize
import asyncio
import datetime
from paginator import MentionPages
from discord.ext import menus


class EmbedField:
  def __init__(self, name, value):
    self.name = name
    self.value = value





class Mentions(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def check_for_account(ctx):
    return os.path.isfile(f'data/{ctx.author.id}.sqlite')

  @commands.command(name="mentions", brief="Shows your recent mentions", aliases=["pings"])
  @commands.check(check_for_account)
  async def mentions(self, ctx):
    """
    Gets your most recent mentions, including information like:
    - Time
    - Author 
    - Message link
    - Ghost (deleted) pings
    """

    conn = await asqlite.connect(f'data/{ctx.author.id}.sqlite')
    if ctx.guild:
      len_res = len(await conn.fetchall("SELECT * FROM mentions WHERE guild_id = ?", (ctx.guild.id,)))
      res = await conn.fetchall("SELECT * FROM mentions WHERE guild_id = ?", (ctx.guild.id,))
    else:
      len_res = len(await conn.fetchall("SELECT * FROM mentions"))
      res = await conn.fetchall("SELECT * FROM mentions")
    
    await conn.execute("DELETE FROM mentions WHERE guild_id = ?", (ctx.guild.id,))
    await conn.commit()
    await conn.close()
    if len_res == 0:
      embed = discord.Embed(title="Recent Mentions", color=self.bot.color)
      embed.description = "You have no mentions"
      await ctx.send(embed=embed)
      return
    
    fields_list = []

    for row in res:
      ghost = False
      channel = ctx.guild.get_channel(row[1])
      mentioner = ctx.guild.get_member(int(row[3]))
      try:
        msg = await channel.fetch_message(row[2])
      except Exception:
        ghost = True
      if ghost == False:
        name = f"Pinged by {msg.author}"
      elif ghost == True:
        someone = "someone that left the server"
        if mentioner is None:
          name = f"Ghost pinged by {someone} :shrug:"
        name = f"Ghost pinged by {mentioner}"

      try:
        link = f"[Jump!]({msg.jump_url})"
      except UnboundLocalError:
        link = f"[Jump!](https://discord.com/channels/{row[0]}/{row[1]}/{row[2]})"
      created_time = datetime.datetime.fromtimestamp(row[5])
      field = EmbedField(name = name, value = f"**Content:** {row[4]}\n**Channel:** <#{row[1]}>\n**Time:** {humanize.precisedelta(datetime.datetime.now() - created_time)} ago\n {link}")
      fields_list.append(field)
    menu = menus.MenuPages(MentionPages(fields_list, ctx, per_page=3))
    await menu.start(ctx)

    

      
    
  # @mentions.error
  async def mentions_error(self, ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
      msg = await ctx.send("You don't seem to have an account! Do you want to create one?")
      tick_emoji = ["<:greenTick:849901292515098635>", "<:redTick:849901323473518603>"]
      for emoji in tick_emoji:
        await msg.add_reaction(emoji)
      def check(reaction, user):
        return reaction.message.id == msg.id and str(reaction.emoji) in tick_emoji and user == ctx.author
      reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)
      if str(reaction.emoji) == tick_emoji[0]:
        start = self.bot.get_command('start')
        await start(ctx=ctx)
      elif str(reaction.emoji) == tick_emoji[1]:
        await ctx.send(f"Okay, you can just do `{ctx.prefix}start` whenever you want")


def setup(bot):
  bot.add_cog(Mentions(bot))