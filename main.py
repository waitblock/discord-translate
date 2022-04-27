import discord
from discord.ext import commands

bot = commands.Bot(("translate!", "tr!"), case_insensitive=True, help_command=None)


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f":ping_pong: Pong! {round(bot.latency*100, 2)}ms")


@bot.event
async def on_connect():
    print("Bot connected to Discord API")
    await bot.change_presence(activity=discord.Game(name="For help type translate!help"))

with open("TOKEN", "r") as token:
    bot.run(token.read())
