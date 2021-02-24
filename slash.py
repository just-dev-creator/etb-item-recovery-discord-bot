import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashCommand

class Slash(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @cog_ext.cog_slash(name="test", guild_ids=[703266392295604254]. options=[{
    "name": "tosay",
    "type": 3,
    "required": True
  }])
  async def _test(self, ctx: SlashContext):
    await ctx.send("hello"
    )

def setup(bot):
  bot.add_cog(Slash(bot))