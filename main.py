import discord
from discord.ext import commands
from translate import Translator

# Configuration variable(s):
TRANSLATE_LANGUAGE_CODE = "zh"  # This is the ISO 639-1 two letter language code that the bot will translate to
BOT_ID = 969008594097930331  # This is the user ID of your bot
OWNER_ID = 785591018342580254  # This is the user ID of the owner of the bot

# Print bot information
print("Discord Translate v0.0.1")
print("(c) 2022 Ethan (waitblock) under the MIT License")
print("This bot is NOT in affiliation with Discord Inc.")
print("=" * 60)

# Parallel arrays containing the ISO 639-1 two letter language codes, and the language of the two letter language codes in English
language_codes = []
language_names = []

# Read in language codes
with open("language_codes.csv", "r") as language_codes_file:
    language_codes_csv = language_codes_file.read().split("\n")
    for language_code_csv in language_codes_csv:
        language_codes.append(language_code_csv.split(",")[0])
        language_names.append(language_code_csv.split(",")[1])

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
except ValueError:  # channels.txt contains a channel ID that is not an integer
    print("Please remove any channel IDs in 'channels.txt' that are not valid channel IDs / integers.")
    exit()

# Print out the channels that will be translated
print("Channel(s) that will be translated (The channel ID(s) are shown):")
for channel in translate_channels:
    print(channel)

if TRANSLATE_LANGUAGE_CODE not in language_codes:  # Check if language code is valid
    print(
        "The given language code in the configuration variable 'TRANSLATE_LANGUAGE' is an invalid ISO 639-1 two-letter language code.")
    print("Please enter a valid ISO 639-1 two-letter language code and try again.")
    exit()

TRANSLATE_LANGUAGE_NAME = language_names[
    language_codes.index(TRANSLATE_LANGUAGE_CODE)]  # Name of language being translated to
print(f"Configured to translate from English to {TRANSLATE_LANGUAGE_NAME}.")

with open("help.txt", "r") as help_file:  # Put the help text into a variable so it doesn't have to be read again
    HELP_TEXT = help_file.read()

translator = Translator(to_lang=TRANSLATE_LANGUAGE_CODE)

# Enable the 'messages' intent
intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(("translate!", "tr!"), case_insensitive=True, help_command=None, intents=intents)


@bot.command(name="help")
async def print_help(ctx):
    await ctx.send(HELP_TEXT)


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f":ping_pong: Pong! {round(bot.latency * 100, 2)}ms")


@bot.command(name="shutdown")
async def shutdown(ctx):
    if ctx.author.id != OWNER_ID:
        return
    await ctx.send("Confirm shutdown? (Y/N)")

    def verify_author(message):
        return message.author == ctx.author and message.channel == ctx.channel

    confirm = await bot.wait_for("message", check=verify_author)
    confirm_message = confirm.content.lower()
    if confirm_message == "yes" or confirm_message == "y":
        await ctx.send("Shutting down...")
        exit(0)
    else:
        await ctx.send("Shutdown cancelled.")


@bot.command(name="translatechannels")
async def display_translate_channels(ctx):
    await ctx.send(translate_channels)


@bot.event
async def on_message(ctx):
    if ctx.author.id == BOT_ID:  # Ignore the bot's own messages
        return
    if ctx.channel.id in translate_channels:
        original_message = ctx.content
        if original_message[0:3] == "tr!" or original_message[0:10] == "translate!":
            await bot.process_commands(ctx)
            return
        translated_message = translator.translate(original_message)
        output = f"{original_message} (English) -> ({TRANSLATE_LANGUAGE_NAME}) {translated_message}"
        await ctx.reply(output, mention_author=False)
        print(output)


@bot.event
async def on_connect():
    print("Bot connected to Discord API")
    print("=" * 60)
    await bot.change_presence(activity=discord.Game(name="For help type translate!help"))


with open("TOKEN", "r") as token:
    bot.run(token.read())
