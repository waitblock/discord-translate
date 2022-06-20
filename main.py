import discord
from discord.ext import commands
import requests
import json

# Import configuration variables
try:
    with open("config.json", "r") as config_json_file:
        config_json_dict = json.load(config_json_file)
        TRANSLATE_LANGUAGE_CODE = config_json_dict["TRANSLATE_LANGUAGE_CODE"]
        BOT_ID = config_json_dict["BOT_ID"]
        OWNER_ID = config_json_dict["OWNER_ID"]
        PINGS_FOR_API_ERRORS = config_json_dict["PINGS_FOR_API_ERRORS"]
        SEND_API_ERRORS = config_json_dict["SEND_API_ERRORS"]
        TRANSLATE_CHANNELS = config_json_dict["TRANSLATE_CHANNELS"]
except FileNotFoundError:
    print("Please create a file called 'config.json', and add the necessary configuration variables. See https://github.com/waitblock/discord-translate/blob/main/config.json for an example 'config.json' file.")
    exit()

# Print bot information
print("Discord Translate v0.0.1")
print("(c) 2022 Ethan (waitblock) under the MIT License")
print("This bot is NOT in affiliation with Discord Inc.")
print("=" * 60)

# Parallel arrays containing the ISO 639-1 two letter language codes, and the language of the two letter language codes in English
language_codes = []
language_names = []

# Read in language codes
with open("supported_languages.csv", "r") as language_codes_file:
    language_codes_csv = language_codes_file.read().split("\n")
    for language_code_csv in language_codes_csv:
        language_codes.append(language_code_csv.split(",")[0])
        language_names.append(language_code_csv.split(",")[1])

# Print out the channels that will be translated
print("Channel(s) that will be translated (The channel ID(s) are shown):")
for channel in TRANSLATE_CHANNELS:
    print(channel)
print("=" * 60)

if TRANSLATE_LANGUAGE_CODE not in language_codes:  # Check if language code is valid
    print(
        "The given language (by the language code) in the configuration variable 'TRANSLATE_LANGUAGE' is not a language supported by the LibreTranslate API, or is not be a valid ISO 639-1 two-letter language code.")
    print("Please enter a supported language code / a valid ISO 639-1 two-letter language code and try again.")
    print("See https://github.com/waitblock/discord-translate#supported-languages for a list of supported languages.")
    exit()

TRANSLATE_LANGUAGE_NAME = language_names[
    language_codes.index(TRANSLATE_LANGUAGE_CODE)]  # Name of language being translated to
print(f"Configured to translate from English to {TRANSLATE_LANGUAGE_NAME}.")

API_POST_HEADERS = {
    "accept": "application/json"
}
API_TRANSLATE_URL = "https://translate.argosopentech.com/translate"

with open("help.txt", "r") as help_file:  # Put the help text into a variable, so it doesn't have to be read again
    HELP_TEXT = help_file.read()

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
    await ctx.send(TRANSLATE_CHANNELS)


@bot.event
async def on_message(ctx):
    if ctx.author.id == BOT_ID:  # Ignore the bot's own messages
        return
    if ctx.channel.id in TRANSLATE_CHANNELS:
        original_message = ctx.content
        if original_message[0:3] == "tr!" or original_message[0:10] == "translate!":
            await bot.process_commands(ctx)
            return
        request_data = {
            "q": original_message,
            "source": "en",
            "target": TRANSLATE_LANGUAGE_CODE
        }
        response = requests.post(API_TRANSLATE_URL, headers=API_POST_HEADERS, data=request_data)
        if response.status_code == 200:
            translated_message = response.json()["translatedText"]
            output = f"{original_message} (English) -> ({TRANSLATE_LANGUAGE_NAME}) {translated_message}"
            await ctx.reply(output, mention_author=False)
            print(output)
        else:
            error_message = response.json()["error"]
            output = f"API returned with response code {response.status_code}, and with error message '{error_message}'."
            print(output)
            if SEND_API_ERRORS is True:
                if PINGS_FOR_API_ERRORS is True:
                    output += f" ||<@{OWNER_ID}>||"
                await ctx.reply(output, mention_author=False)


@bot.event
async def on_connect():
    print("Bot connected to Discord API")
    print("=" * 60)
    await bot.change_presence(activity=discord.Game(name="For help type translate!help"))


with open("TOKEN", "r") as token:
    bot.run(token.read())
