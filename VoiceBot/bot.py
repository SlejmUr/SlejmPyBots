import discord
import os
import asyncio
from datetime import datetime
from discord.ext import commands

#voice_clients
client = discord.Client()
voice_main = 639890219885395978
roleid = 860920453005312010
guild_id = 614122584967217204
usersids = []  

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$',intents=intents)

@bot.event
async def on_ready():
    print("\n")
    print(f"{client.user} or {bot.user} logged in now!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name='my LORD'))
    while True:
        await asyncio.sleep(5)
        await auto_role()

@bot.event
async def auto_role():
    voice = bot.get_channel(voice_main)
    member_ids = voice.voice_states.keys()
    #print(usersids)
    if not member_ids:
      if not usersids:
        return
      else:
        for key in usersids:
          await removerole(key,voice,"because no-one in the voice")
    else:
      for key in member_ids:
        if key not in usersids:
          await addrole(key,voice)
          return
      for key in usersids:
        await removerole(key,voice,"because left the voice")
        
@bot.event
async def addrole(key,voice):
  takenGuild = bot.get_guild(guild_id)
  role = takenGuild.get_role(roleid)
  member = await takenGuild.fetch_member(int(key))
  now = datetime.now()
  print(f"{member} is on the {voice} Voice channel at {now}")
  if not role in member.roles:
    await member.add_roles(role)
    print(f"Role added to {member} at {now}")
    if member.id not in usersids:
      usersids.append(member.id)
      return
  else:
    if member.id not in usersids:
      usersids.append(member.id)
      return

@bot.event
async def removerole(key,voice,reason):
    takenGuild = bot.get_guild(guild_id)
    role = takenGuild.get_role(roleid)
    member = await takenGuild.fetch_member(int(key))
    if not member in voice.members:
      if role in member.roles:
        await member.remove_roles(role)
        now = datetime.now()
        print(f"Role removed from {member} {reason} at {now}")
        usersids.remove(member.id)
        return

@bot.command()
async def cleanroles(ctx):
  takenGuild = bot.get_guild(guild_id)
  role = takenGuild.get_role(roleid)
  async for member in takenGuild.fetch_members(limit=200):
    if role in member.roles:
      await member.remove_roles(role)

my_secret = os.environ['TOKEN']
bot.run(my_secret)
