import os
from discord.ext import commands
from discord_slash import SlashCommand
import pymongo
from dotenv import load_dotenv

# Initialize team variable. ADD YOUR MEMBERS HERE
team_members = [460143849172631553]

# Setup .env file
load_dotenv()

# Set up the bot and slash commands
client = commands.Bot(command_prefix='%')
token = os.environ["DISCORD_BOT_TOKEN"]
slash = SlashCommand(client, override_type=True)


@client.event
async def on_ready():
    """Is called when the client logged in succesfully."""
    # Notify user when client is connected
    print('We have logged in as {0.user}'.format(client))
    # Synchronise all commands because the cog is now loaded
    await slash.sync_all_commands(delete_from_unused_guilds=False)


# MongoDB Connection
mongoClient = pymongo.MongoClient(os.environ["MONGODB_CONNECTION_STRING"])
db = mongoClient["etb-item-recovery"]
collection = db["cases"]

# Load cogs
client.load_extension("slash")
client.load_extension("dmconversation")
# Run the bot
try:
    client.run(token)
except KeyboardInterrupt:
    print("Goodbye.")
    exit(0)
