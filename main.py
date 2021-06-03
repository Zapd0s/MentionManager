import discord
from discord.ext import commands
import asqlite
import jishaku
import os
import humanize
import time
import datetime
import asyncio
from discord.ext import tasks







mentions = discord.AllowedMentions(everyone=False, replied_user=False, roles=False, users=False)
bot = commands.Bot(command_prefix = "-", allowed_mentions=mentions, intents = discord.Intents.all())
bot.color = discord.Color.from_rgb(255,0,0)

async def check_if_acc(ctx:commands.Context):
  if os.path.isfile(f'data/{ctx.author.id}'):
    return True
  else:
    return False

@bot.event
async def on_ready():
  bot.load_extension('jishaku')
  bot.load_extension('listener')
  print("Ready")

@bot.command()
async def start(ctx):
  if os.path.isfile(f'data/{ctx.author.id}.sqlite'):
    await ctx.send("bruh")
    return
  conn = await asqlite.connect(f'data/{ctx.author.id}.sqlite')
  await conn.execute("CREATE TABLE IF NOT EXISTS mentions (guild_id INT, ch_id INT, msg_id INT, pinger INT, content TEXT, created INT)")
  await conn.commit()
  await conn.close()
  await ctx.send("Alright, I will now start storing your mentions!")


@bot.command(aliases=["pings"])
async def mentions(ctx):
  if not os.path.isfile(f'data/{ctx.author.id}.sqlite'):
    return await ctx.send("bruh")

  conn = await asqlite.connect(f'data/{ctx.author.id}.sqlite')
  if ctx.guild:
    len_res = len(await conn.fetchall("SELECT * FROM mentions WHERE guild_id = ?", (ctx.guild.id,)))
    res = await conn.fetchmany("SELECT * FROM mentions WHERE guild_id = ?", (ctx.guild.id,), size=10)
  else:
    len_res = len(await conn.fetchall("SELECT * FROM mentions"))
    res = await conn.fetchmany("SELECT * FROM mentions", size=25)
  embed = discord.Embed(title="Recent Mentions",color=bot.color)
  if len_res == 0:
    embed.description = "You have no mentions"
    await ctx.send(embed=embed)
    await conn.close()
    return
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
    no_ch = "Channel was deleted"
    embed.add_field(name = name, value = f"**Content:** {row[4]}\n**Channel:** {channel.mention if channel is not None else no_ch}\n**Time:** {humanize.precisedelta(datetime.datetime.now() - created_time)} ago\n {link}")
  await conn.close()
  embed.set_footer(text = f"Showing {len(embed.fields)} of {len_res} mentions • React here to clear the above mentions")
  message = await ctx.send(embed = embed)
  await message.add_reaction("⏹️")
  def check(reaction, user):
    if user.id == ctx.author.id:
      if reaction.message.id == message.id:
        if reaction.emoji == "⏹️":
          return True
        else:
          return False
      else:
        return False
    else:
      return False
  try:
    await bot.wait_for('reaction_add',check=check,timeout=60)
  except asyncio.TimeoutError:
    return
  else:
    conn = await asqlite.connect(f"data/{ctx.author.id}.sqlite")
    await conn.execute("DELETE FROM mentions WHERE guild_id = ? LIMIT ?", (ctx.guild.id, len(embed.fields)))
    await conn.commit()
    if ctx.guild:
      len_res = len(await conn.fetchall("SELECT * FROM mentions WHERE guild_id = ?", (ctx.guild.id,)))
    else:
      len_res = len(await conn.fetchall("SELECT * FROM mentions"))
    await ctx.reply(f"Cleared {len(embed.fields)} mentions. {len_res} remaining", delete_after = 5)
    await conn.close()

    
@bot.command()
async def ping(ctx):
  start = time.perf_counter()
  a = await ctx.send("Pinging...")
  end = time.perf_counter()
  dur = (end-start) * 1000
  embed = discord.Embed(title = "Pong!", description = f"**Response Time** \n ```{dur:.2f}ms```\n **Websocket Latency** \n ```{round(((bot.latency) * 1000), 2)}ms```", color = bot.color)
  await a.edit(embed = embed)



@tasks.loop(minutes=5)
async def clear_unwanted():
  for file in os.listdir('data/'):
    conn = await asqlite.connect(file)
    res = await conn.fetchall("SELECT * FROM mentions")
    for row in res:
      mentioned_time = datetime.datetime.fromtimestamp(row[5])
      if datetime.datetime.now() - mentioned_time > datetime.timedelta(days=2):
        await conn.execute("DELETE FROM mentions WHERE msg_id = ?", row[2])
      await conn.commit()
      await conn.close()


  




token = os.environ['TOKEN']
bot.run(token)

