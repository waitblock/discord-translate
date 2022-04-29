import discord
from discord.ext import commands

# Print bot information
print("Discord Translate v0.0.1")
print("(c) 2022 Ethan (waitblock) under the MIT License")
print("This bot is NOT in affiliation with Discord Inc.")
print("="*60)

translate_channels = []  # Channels IDs that will have translations enabled.
# Read & parse channels from channels.txt file
try:
    with open("channels.txt", "r") as channels_file:
        channels = channels_file.read().split("\n")
        for channel in channels:
            translate_channels.append(int(channel))
except FileNotFoundError:  # channels.txt file does not exist
    print("Please create a file with the name 'channels.txt' to configure the bot.")
    exit()

print("Channel(s) that will be translated (The channel ID(s) are shown):")
for channel in translate_channels:
    print(channel)

bot = commands.Bot(("translate!", "tr!"), case_insensitive=True, help_command=None)


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f":ping_pong: Pong! {round(bot.latency*100, 2)}ms")


@bot.event
async def on_message(message):
    if message.channel.id in translate_channels:
        print(message.content)


@bot.event
async def on_connect():
    print("Bot connected to Discord API")
    print("="*60)
    await bot.change_presence(activity=discord.Game(name="For help type translate!help"))

with open("TOKEN", "r") as token:
    bot.run(token.read())
