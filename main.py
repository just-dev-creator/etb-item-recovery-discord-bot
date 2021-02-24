import os
from discord.ext import commands
from discord_slash import SlashCommand

client = commands.Bot(command_prefix='%')
token = os.environ["DISCORD_BOT_TOKEN"]
slash = SlashCommand(client, override_type=True, auto_register=True, auto_delete=True)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

client.run(token)