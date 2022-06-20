<img src=https://i.ibb.co/TPcQM44/translate-bot.png height="300" width="auto"/>

# Discord Translate

## Configuration
*At the moment, there is supposed to be one bot hosted for each server that you want the bot to be in.*
1. Create a file called 'TOKEN'
2. Add your bot's token in the 'TOKEN' file
3. Change the configuration variables in the 'config.json' file to reflect your desired configuration ([A description of each configuration variable is provided below](https://github.com/waitblock/discord-translate#configuration-variables))
4. The bot should now run and translate to the configured language in the channels specified

If the bot does not seem to be working properly, please send me an issue in the 'Issues' tab of this repository.

## Supported Languages
*Currently, the bot will only translate from English to a specified language.*
- Arabic (ar)
- Chinese (zh)
- English (en)
- French (fr)
- German (de)
- Hindi (hi)
- Indonesian (id)
- Irish (ga)
- Italian (it)
- Japanese (ja)
- Korean (ko)
- Polish (pl)
- Portuguese (pt)
- Russian (ru)
- Spanish (es)
- Turkish (tr)
- Vietnamese (vi)

## Configuration Variables
| Variable Name           | Datatype          | Description                                                                                |
|-------------------------|-------------------|--------------------------------------------------------------------------------------------|
| TRANSLATE_LANGUAGE_CODE | String            | The ISO 639-1 two letter language code that the bot will translate to.                     |
| BOT_ID                  | Integer           | The Discord user ID of your bot.                                                           |
| OWNER_ID                | Integer           | The Discord user ID of the owner of the bot.                                               |
| PINGS_FOR_API_ERRORS    | Boolean           | Whether or not the bot will ping you in the case of an API error.                          |
| SEND_API_ERRORS         | Boolean           | Whether or not the bot will send error messages in the server in the case of an API error. |
| TRANSLATE_CHANNELS      | Array of Integers | The list of Discord channel IDs that you want the bot to translate in.                     |

*Disclaimer: This bot is NOT in affiliation with Discord Inc.*
