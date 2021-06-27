# Import modules
import discord, datetime, time
from discord.ext.commands import Bot
from discord.ext import commands
import requests
import json
import aiohttp
import random
import os
from dotenv import load_dotenv
from discord_slash import SlashCommand, SlashContext
from discord_slash import SlashCommandOptionType
from discord_slash.utils import manage_commands
from discord_slash.utils.manage_commands import create_option




load_dotenv()
TOKEN = os.getenv("TOKEN")
prefix = "-"


# define your client
client = Bot(command_prefix=prefix, intents=discord.Intents.all(), allowed_mentions=discord.AllowedMentions(everyone=False))

client = commands.Bot(command_prefix="prefix")
slash = SlashCommand(client, override_type = True, sync_commands=True)

[client.load_extension("cogs." + x.replace(".py", "")) for x in os.listdir("cogs") if x.endswith(".py")]
# slash = SlashCommand(client, auto_register=True, auto_delete=True)
# guild_ids = [809464190577541120, 829249975966761001]





# if you want to remove the deafult HELP command
client.remove_command('help')


# Its a event which will run when the bot is ready/online.
@client.event
async def on_ready():
    activity = discord.Activity(
        type=discord.ActivityType.watching, name="Slash Commands"
    )
    await client.change_presence(status=discord.Status.dnd, activity=activity)
    print("Logged in as " + client.user.name)
    



# Run the bot with the token
client.run(TOKEN)
