# selfVideo.py

# default modules
import os
import platform

# idk auto install stuff
os.system('python -m pip install -r requirements.txt')

from dotenv import load_dotenv

# Import Third-party software party software like discord.py
import discord  # Import the original discord.py module
from discord.ext import commands
import asyncio

# .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = int(os.getenv('DISCORD_GUILD'))
CHANNEL = int(os.getenv('CHANNEL'))
AFKCHANNEL = int(os.getenv('AFKCHANNEL'))

# bot intents
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

# command_prefix not in use
client = commands.Bot(command_prefix=".", intents=discord.Intents.all())

# check if all members have video on
async def check_voice_channel_task(channel, afk_channel):
    print(f'Checking voice channel... Name: {channel.name}')
    while True:
        for member in channel.members:
            print(
                f"Checking: {member.name}"
                f" ID: {member.id}"
                f" Video: {member.voice.self_video}"
                )
            if not member.voice.self_video:
                print(f'Move member {member.name} to AFK channel')
                embed = discord.Embed(
                    title="Hey! Ich will dein gesicht sehen!", 
                    description="Bitte aktiviere deine Kamera um nicht rausgeworfen zu werden",
                    color=0x207d96
                    )
                await member.send(embed=embed)
                #await member.edit(voice_channel=None)
                await member.move_to(afk_channel)

        await asyncio.sleep(60)
        
@client.slash_command(
    name='nomotion', 
    description="Zum Beispiel, wenn ein Mitglied nur Schwarzbild auf der Videokamera hat.",
    guild_ids=[GUILD]
    )
@commands.has_permissions(move_members=True)
async def nomotion(context: commands.context, member: discord.Member):
    print(f'Forced to move member {member.name} to AFK channel')
    
    guild = client.get_guild(GUILD)
    channel = guild.get_channel(CHANNEL)
    afk_channel = guild.get_channel(AFKCHANNEL)

    if member.voice.channel == channel:
        embed = discord.Embed(
            title="Hey! Bist du noch da?", 
            description="Bitte zeige dich mal um nicht rausgeworfen zu werden",
            color=0x207d96
        )
        await member.send(embed=embed)
        await member.move_to(afk_channel)
        await context.respond(f'Der {member.name} wurde gewaltsam entfernt!')
    else:
        await context.respond(f'Was wurde mit dem {member.name} versucht?')

# status for fun
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game(name='How to disconnect member FAST'))
        await asyncio.sleep(120)
        await client.change_presence(activity=discord.Streaming(name="member without video", url="https://www.youtube.com/watch?v=oHg5SJYRHA0"))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="disconnect member song"))
        await asyncio.sleep(120)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='to member without video'))
        await asyncio.sleep(120)

# ready info
@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")

    guild = client.get_guild(GUILD)
    channel = guild.get_channel(CHANNEL)
    afk_channel = guild.get_channel(AFKCHANNEL)

    client.loop.create_task(check_voice_channel_task(channel, afk_channel))
    client.loop.create_task(status_task())

if __name__ == "__main__":
    client.run(TOKEN)