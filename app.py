# selfVideo.py
import os

# idk auto install stuff
os.system('python -m pip install python-dotenv --quiet')
os.system('python -m pip install discord --quiet')
os.system('python -m pip install asyncio --quiet')

from dotenv import load_dotenv

# discord.py
import discord
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
client = discord.Client(intents=intents)

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
    guild = client.get_guild(GUILD)
    channel = guild.get_channel(CHANNEL)
    afk_channel = client.get_channel(AFKCHANNEL)

    client.loop.create_task(check_voice_channel_task(channel, afk_channel))
    client.loop.create_task(status_task())

client.run(TOKEN)
