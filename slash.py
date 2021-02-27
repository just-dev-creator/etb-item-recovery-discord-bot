from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import main
from datetime import datetime

class Slash(commands.Cog):
  """.
  This class handles all slash commands
  """
  
  def __init__(self, bot):
    self.bot = bot
  # 703266392295604254
  @cog_ext.cog_slash(name="createticket", guild_ids=[703266392295604254, 757917063070089327], options=[{
    "name": "Betreff",
    "type": 3,
    "required": True,
    "description": "Gib dein Anliegen in einigen Wörtern an"
  }, {
    "name": "Kurzbeschreibung",
    "type": 3,
    "required": True,
    "description": "Gib dein Anliegen in ein bis zwei Sätzen an."
  }], description="Erstelle eine Schadensersatzforderung aufgrund Laggs. ")
  async def _createticket(self, ctx: SlashContext, Betreff, Kurzbeschreibung):
    """.
    Creating the refund ticker
    """
    # Respond to slash command
    await ctx.respond(eat=True)
    # Check if user already has an open case
    query = {
      "userid": ctx.author_id
    }
    if main.collection.find_one(query) is not None:
      # Informing the user about the error
      await ctx.send("Du hast bereits eine offene Anfrage!", hidden=True)
      return

    # Informing the user that his case was opened
    await ctx.send(f"Deine Forderung mit dem Betreff `{Betreff}` und der Kurzbeschreibung `{Kurzbeschreibung}` wurde erstellt. Schaue bitte in deine privaten Nachrichten.", hidden=True)
    # Creating DM-Channel with user
    author = ctx.author
    dm = await author.create_dm()
    # Creating MongoDB-Entry for User
    main.collection.insert_one({
      "userid": ctx.author_id,
      "lastcontact": datetime.now(),
      "title": Betreff,
      "desc": Kurzbeschreibung
    })
    # Informing the user about the system and asking for the time
    await dm.send("Dein persönlichr Channel wurde initialisiert. Bitte beantworte die folgenden Nachrichten hier im Chat!")
    await dm.send("Wann hat der Vorfall stattgefunden. Bitte gib die Zeit genau an, da wir sonst die aufgetretenen Lags nicht verifizieren können und deinen Antrag ablehnen müssen. ")
  @cog_ext.cog_slash(name="accept", guild_ids=[703266392295604254], options=[{
    "name": "userid",
    "type": 3,
    "required": True,
    "description": "Gib die ID des Users an"
  },{
    "name": "Informationen",
    "type": 3,
    "required": False,
    "description": "Gib dem User einige weitere Informationen"
  }], description="Akzeptiere die Anfrage eines Users")
  async def _accept(self, ctx: SlashContext, userid: str, Informationen: str = None):
    """.
    When this function the request is accepted
    """
    await ctx.respond(eat=True)
    # Convert Userid-String to int
    userid = int(userid)
    # Check for permissions
    if ctx.author_id != 460143849172631553:
      await ctx.send("Du hast hierfür keine Berechtigungen! ", hidden=True)
      return
    # Find and delete MongoDB entry
    main.collection.delete_one({
      "userid": userid
    })
    # Open DM with target
    target = await self.bot.fetch_user(userid)
    target_dm = await target.create_dm()
    # Send approval to target
    await target_dm.send("Herzlichen Glückwunsch! Dein Antrag wurde akzeptiert! Du solltest deine Items innerhalb der nächsten zwei Tage erhalten. Bitte beachte, dass kein neuer Antrag für den Vorfall gestellt werden darf! ")
    if Informationen is not None:
      await target_dm.send("Hier sind weitere Informationen von deinem Sachbearbeiter für dich: " + Informationen)
    # Send confirmation for steps to team member
    await ctx.send("Du hast den Antrag erfolgreich akzeptiert! ", hidden=True)
  @cog_ext.cog_slash(name="decline", guild_ids=[703266392295604254], options=[{
    "name": "userid",
    "type": 3,
    "required": True,
    "description": "Gib die ID des Users an"
  },{
    "name": "Informationen",
    "type": 3,
    "required": False,
    "description": "Gib dem User einige weitere Informationen"
  }], description="Akzeptiere die Anfrage eines Users")
  async def _decline(self, ctx: SlashContext, userid: str, Informationen: str = None):
    """.
    When this function is called the request gets cancelled
    """
    await ctx.respond(eat=True)
    # Convert Userid-String to int
    userid = int(userid)
    # Check for permissions
    if ctx.author_id != 460143849172631553:
      await ctx.send("Du hast hierfür keine Berechtigungen! ", hidden=True)
      return
    # Find and delete MongoDB entry
    main.collection.delete_one({
      "userid": userid
    })
    # Open DM with target
    target = await self.bot.fetch_user(userid)
    target_dm = await target.create_dm()
    # Send approval to target
    await target_dm.send("Es tut uns leid, aber dein Antrag wurde leider nicht akzeptiert. Dies könnte daran liegen, dass du zu wenig oder ungenaue Informationen angegeben hast. Bitte stelle aber erst in frühestens drei Tagen einen weiteren Antrag zu dieser Situation! ")
    if Informationen is not None:
      await target_dm.send("Hier sind weitere Informationen von deinem Sachbearbeiter für dich: " + Informationen)
    # Send confirmation for steps to team member
    await ctx.send("Du hast den Antrag erfolgreich abgelehnt! ", hidden=True)
  @cog_ext.cog_slash(name="custom", guild_ids=[703266392295604254], options=[{
    "name": "userid",
    "type": 3,
    "required": True,
    "description": "Gib die ID des Users an"
  },{
    "name": "Informationen",
    "type": 3,
    "required": True,
    "description": "Gib dem User Informationen"
  }], description="Akzeptiere die Anfrage eines Users")
  async def _custom(self, ctx: SlashContext, userid: str, Informationen: str):
    """.
    When this function is called the user gets custom information
    """
    await ctx.respond(eat=True)
    # Convert Userid-String to int
    userid = int(userid)
    # Check for permissions
    if ctx.author_id != 460143849172631553:
      await ctx.send("Du hast hierfür keine Berechtigungen! ", hidden=True)
      return
    # Open DM with target
    target = await self.bot.fetch_user(userid)
    target_dm = await target.create_dm()
    # Send approval to target
    await target_dm.send("Hier sind Informationen von deinem Sachbearbeiter: " + Informationen)
    # Send confirmation for steps to team member
    await ctx.send("Du hast die Nachricht erfolgreich übermittelt! ", hidden=True)

def setup(bot):
  """Sets up the cog"""
  bot.add_cog(Slash(bot))