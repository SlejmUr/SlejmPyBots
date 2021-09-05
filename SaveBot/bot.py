import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord import utils

client = discord.Client()
intents = discord.Intents.default()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix='$',intents=intents)

Guild_Main = 762268016972922881 #Main guild ID
Guild_Backup = 879383448568102952 #Save guild ID

@bot.event
async def on_ready():
    print("\n")
    print(f"{client.user} or {bot.user} logged in now!")
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name='my LORD'))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name='saving your ass'))
    custom_guild = bot.get_guild(Guild_Backup)
    custom_channel = discord.utils.get(custom_guild.channels, name=(f'bot-messages'))
    await custom_channel.send("BOT is Started")

@bot.event
async def on_message(message):
  #check if author not itself
  if message.author == bot.user:
    return
  #check if message send to MAIN Guild
  if Guild_Main != message.guild.id:
      return
  #set future things
  CHANNELNAME = message.channel.name
  custom_guild = bot.get_guild(Guild_Backup)
  custom_channel = discord.utils.get(custom_guild.channels, name=(f'{CHANNELNAME}'))
  #set embed
  embed=discord.Embed(title="Message sent", description=message.content, color=0x29f500)
  embed.set_thumbnail(url=message.author.avatar_url)
  embed.set_author(name=message.author.name)
  #check message attachment
  if message.attachments != []:
    attachment = message.attachments[0]
    embed.set_image(url=attachment.url)
    #check if end with mp4
    if attachment.filename.endswith("mp4"):
      embed.add_field(name="Send as MP4", value="Url: " + attachment.url, inline=False)
    if attachment.filename.endswith("mov"):
      embed.add_field(name="Send as MOV", value="Url: " + attachment.url, inline=False)
  #check if message is embed
  if message.embeds != []:
    EMBED = message.embeds[0]
    embed=discord.Embed(title=EMBED.title, url=EMBED.url, description=EMBED.description, color=EMBED.color)
    embed.set_author(name=message.author.name)
  #Finally send to Backup channel
  await custom_channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
  #check if author not itself
  if before.author == bot.user:
    return
  #check if message send to MAIN Guild
  if Guild_Main != before.guild.id:
      return
  #set future things
  CHANNELNAME = before.channel.name
  custom_guild = bot.get_guild(Guild_Backup)
  custom_channel = discord.utils.get(custom_guild.channels, name=(f'{CHANNELNAME}'))
  #set embed
  embed=discord.Embed(title="Message edited", description=(f"`{before.content}` edited to `{after.content}`"), color=0x4169e1)
  embed.set_thumbnail(url=before.author.avatar_url)
  embed.set_author(name=before.author.name)
  #Finally send to Backup channel
  await custom_channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
  #check if author not itself
  if message.author == bot.user:
    return
  #check if message send to MAIN Guild
  if Guild_Main != message.guild.id:
      return
  #set future things
  CHANNELNAME = message.channel.name
  custom_guild = bot.get_guild(Guild_Backup)
  custom_channel = discord.utils.get(custom_guild.channels, name=(f'{CHANNELNAME}'))
  #set embed
  embed=discord.Embed(title="Message deleted", description=(f"`{message.content}` deleted"), color=0xFF5733)
  embed.set_thumbnail(url=message.author.avatar_url)
  embed.set_author(name=message.author.name)
  #Finally send to Backup channel
  await custom_channel.send(embed=embed)

BOT_TOKEN = os.environ['TOKEN']
bot.run(BOT_TOKEN)
