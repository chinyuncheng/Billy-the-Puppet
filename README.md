# Billy-the-Puppet
The Discord bot provides Slash Commands to host game events.

## Features
- Language
- Logger
- Timezone (pytz)

## Usages
1. Create your own Discord bot application.
2. Clone this repository to any server platform that you want.
3. Add the .env file with the following key in the root folder
```
DISCORD_BOT_TOKEN=`Your_discord_bot_token`
```
4. Change the value of the key in settings.py as below
```python
ALLOW_ADD_NEW_GUILD  =  True
```
5. Add the bot to your Discord server
6. Change the value to False in step 4 if you don't want the bot being added to another server
