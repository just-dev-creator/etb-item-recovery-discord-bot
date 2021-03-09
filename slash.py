from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord import Embed
from discord import Colour
import main
import time
from datetime import datetime

class Slash(commands.Cog):
  """.
  This class handles all slash commands
  """
  
  def __init__(self, bot):
    self.bot = bot
  # EtB ID: 757917063070089327
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
  }, {
    "name": "clientside",
    "type": 5,
    "required": True,
    "description": "Ist der Fehler nach §5.2 clientseitig verschuldet?"
  }], description="Erstelle eine Schadensersatzforderung aufgrund Laggs. ")
  async def _createticket(self, ctx: SlashContext, Betreff, Kurzbeschreibung, clientside: bool):
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

    # Informing the user that his case isn't prioritisied
    if clientside:
      await ctx.send("Wir haben gesehen, dass dein Bug clientseitig enstanden ist. Dies kann zu Verzögerungen bei der Rückerstattung führen, **sie wird jedoch trotzdem behandelt.**", hidden=True)

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
      "desc": Kurzbeschreibung,
      "clientside": clientside
    })
    # Informing the user about the system and asking for the time
    embed = Embed(title="Zeitpunkt", colour=Colour(0x3d14eb), description="Wann hat der Vorfall stattgefunden? Antworte direkt im Chat!", timestamp=datetime.utcfromtimestamp(time.time()))

    embed.set_footer(text="This bot was created by justCoding!")

    embed.add_field(name=":question:", value="Wir benutzen diese Angaben, um zu verifizieren, dass der Bug tatsächlich stattgefunden hat. ")
    embed.add_field(name=":exclamation:", value="Sofern die Angaben zu ungenau sind, wird dein Antrag abgelehnt. Bei Toden reicht eine Genauigkeit auf die Stunde, bei anderweitigen Verlusten müssen deine Angaben auf die Minute stimmen.")

    await dm.send(embed=embed)
  @cog_ext.cog_slash(name="accept", guild_ids=[703266392295604254, 757917063070089327], options=[{
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
  @cog_ext.cog_slash(name="decline", guild_ids=[703266392295604254, 757917063070089327], options=[{
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
  @cog_ext.cog_slash(name="custom", guild_ids=[703266392295604254, 757917063070089327], options=[{
    "name": "userid",
    "type": 3,
    "required": True,
    "description": "Gib die ID des Users an"
  },{
    "name": "Informationen",
    "type": 3,
    "required": True,
    "description": "Gib dem User Informationen"
  }], description="Gibt dem User weitere Informationen. Der Fall wird weder akzeptiert noch abgelehnt. ")
  async def _custom(self, ctx: SlashContext, userid: str, Informationen: str):
    """.
    When this function is called the user gets custom information
    """
    # Check for permissions
    if ctx.author_id != 460143849172631553:
      await ctx.send("Du hast hierfür keine Berechtigungen! ", hidden=True)
      return
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

  @cog_ext.cog_slash(name="suggest", guild_ids=[703266392295604254, 757917063070089327], description="Zeigt die älteste Konversation an.")
  async def _suggest(self, ctx: SlashContext):
    """
    Shows the user a case that he can work on
    """
    await ctx.respond(eat=True)
    # Check for permissions
    if ctx.author_id != 460143849172631553:
      await ctx.send("Du hast hierfür keine Berechtigungen! ", hidden=True)
      return
    
    found = main.collection.find_one({
      "confirmed": True
      ,"clientside": False
    })
    if found == None:
      found = main.collection.find_one({
        "confirmed": True
      })
      if found == None:
        await ctx.send(":sunglasses: Alles geschafft, es gibt keine zu bearbeitenden Anfragen!", hidden=True)
      else:
        target = await self.bot.fetch_user(found['userid'])
        embed = Embed(title=f"Anfrage von `{target.name}#{target.discriminator}`", colour=Colour(0x56ff), description="Wir konnten einen Eintrag finden. Bitte überprüfe die folgenden Daten und antworte dem User auf einem Server, der die Staff-Commands besitzt, mit */accept* oder */decline* oder */custom*.")
        embed.set_footer(text="This bot was created by justCoding!")
        embed.add_field(name=":globe_with_meridians:", value=f"Betreff: `{found['title']}`")
        embed.add_field(name=":book:", value=f"Kurzbeschreibung: `{found['desc']}`")
        embed.add_field(name=":mens:", value=f"Clientseitig: `{found['clientside']}`")
        embed.add_field(name=":clock1:", value=f"Zeitpunkt: `{found['time']}`")
        embed.add_field(name=":map:", value=f"Szenario: `{found['scenario']}`")
        embed.add_field(name=":card_box:", value=f"Verlorene Items: `{found['items']}`")
        embed.add_field(name=":man:", value=f"UserID: `{found['userid']}`")
        await ctx.send(content="Wir haben dir einen Vorschlag per DM zukommen lassen!", hidden=True, delete_after=7.5)
        message_history = ""
      for i in found['conversation']:
        author = await self.bot.fetch_user(i['userid'])
        message_history += author.name + "#" + author.discriminator + ": *" + i['message'] + "*\n"
      
      message_history += ""
      embed.add_field(name=":books:", value=message_history)
      dm = await ctx.author.create_dm()
      await dm.send(embed=embed)
    else:
      target = await self.bot.fetch_user(found['userid'])
      embed = Embed(title=f"Anfrage von `{target.name}#{target.discriminator}`", colour=Colour(0x56ff), description="Wir konnten einen Eintrag finden. Bitte überprüfe die folgenden Daten und antworte dem User auf einem Server, der die Staff-Commands besitzt, mit */accept* oder */decline* oder */custom*.")
      embed.set_footer(text="This bot was created by justCoding!")
      embed.add_field(name=":globe_with_meridians:", value=f"Betreff: `{found['title']}`")
      embed.add_field(name=":book:", value=f"Kurzbeschreibung: `{found['desc']}`")
      embed.add_field(name=":mens:", value=f"Clientseitig: `{found['clientside']}`")
      embed.add_field(name=":clock1:", value=f"Zeitpunkt: `{found['time']}`")
      embed.add_field(name=":map:", value=f"Szenario: `{found['scenario']}`")
      embed.add_field(name=":card_box:", value=f"Verlorene Items: `{found['items']}`")
      embed.add_field(name=":man:", value=f"UserID: `{found['userid']}`")
      message_history = ""
      for i in found['conversation']:
        author = await self.bot.fetch_user(i['userid'])
        message_history += author.name + "#" + author.discriminator + ": *" + i['message'] + "*\n"
      
      message_history += ""
      embed.add_field(name=":books:", value=message_history)
      await ctx.send(content="Wir haben dir einen Vorschlag per DM zukommen lassen!", hidden=True, delete_after=7.5)
      dm = await ctx.author.create_dm()
      await dm.send(embed=embed)


  @cog_ext.cog_slash(name="answer", options=[{
    "name": "userid",
    "description": "Die ID des Users auf die du antworten möchtest.",
    "required": True,
    "type": 3
  },{
    "name": "answer",
    "description": "Gib deine Antwort an.",
    "required": True,
    "type": 3
  }], description="Fügt eine Antwort der Konversation hinzu. ", guild_ids=[703266392295604254, 757917063070089327])
  async def _answer(self, ctx: SlashContext, userid, answer):
    await ctx.respond(eat=True)
    userid = int(userid)
    found = main.collection.find_one({
          "userid": int(userid)
        })
    if not "conversation" in found:
      main.collection.update_one(filter={
        "userid": ctx.author.id
      }, update={
        "$set": {
        "conversation": [{
          "userid": ctx.author.id,
          "message": answer
        }]
      }
      })
      found = main.collection.find_one({
      "userid": ctx.author.id
      })
      embed = Embed(title=f"Neue Nachricht von `{ctx.author.name}#{ctx.author.discriminator}`", colour=Colour(0x56ff))
      embed.set_footer(text="This bot was created by justCoding!")
      embed.add_field(name=":globe_with_meridians:", value=f"Betreff: `{found['title']}`")
      embed.add_field(name=":book:", value=f"Kurzbeschreibung: `{found['desc']}`")
      embed.add_field(name=":mens:", value=f"Clientseitig: `{found['clientside']}`")
      embed.add_field(name=":clock1:", value=f"Zeitpunkt: `{found['time']}`")
      embed.add_field(name=":map:", value=f"Szenario: `{found['scenario']}`")
      embed.add_field(name=":card_box:", value=f"Verlorene Items: `{found['items']}`")
      embed.add_field(name=":man:", value=f"UserID: `{ctx.author.id}`")
      message_history = ""
      for i in found['conversation']:
        author = await self.bot.fetch_user(i['userid'])
        message_history += author.name + "#" + author.discriminator + ": *" + i['message'] + "*\n"
      
      message_history += ""
      embed.add_field(name=":books:", value=message_history)

      team = await self.bot.fetch_user(460143849172631553)
      team_dm = await team.create_dm()

      await team_dm.send(embed=embed)

      await ctx.send("Deine Nachricht wurde erfolgreich übermittelt.")
      await ctx.send(embed=embed)

    else:
      found_conversation = main.collection.find_one({
        "userid": userid
      })['conversation']
      found_conversation.append({
        "userid": ctx.author.id,
        "message": answer
      })
      main.collection.update_one({
        "userid": userid
      }, {
        "$set": {
          "conversation": found_conversation
        }
      })
      found = main.collection.find_one({
      "userid": userid
      })
      embed = Embed(title=f"Neue Nachricht von `{ctx.author.name}#{ctx.author.discriminator}`", colour=Colour(0x56ff))
      embed.set_footer(text="This bot was created by justCoding!")
      embed.add_field(name=":globe_with_meridians:", value=f"Betreff: `{found['title']}`")
      embed.add_field(name=":book:", value=f"Kurzbeschreibung: `{found['desc']}`")
      embed.add_field(name=":mens:", value=f"Clientseitig: `{found['clientside']}`")
      embed.add_field(name=":clock1:", value=f"Zeitpunkt: `{found['time']}`")
      embed.add_field(name=":map:", value=f"Szenario: `{found['scenario']}`")
      embed.add_field(name=":card_box:", value=f"Verlorene Items: `{found['items']}`")
      embed.add_field(name=":man:", value=f"UserID: `{ctx.author.id}`")
      message_history = ""
      for i in found['conversation']:
        author = await self.bot.fetch_user(i['userid'])
        message_history += author.name + "#" + author.discriminator + ": *" + i['message'] + "*\n"
      
      message_history += ""
      embed.add_field(name=":books:", value=message_history)

      team = await self.bot.fetch_user(userid)
      team_dm = await team.create_dm()

      await team_dm.send(embed=embed)

      await ctx.send("Deine Nachricht wurde erfolgreich übermittelt.", hidden=True)
      await (await ctx.author.create_dm()).send(embed=embed)


  @cog_ext.cog_slash(name="show", options=[
    {
      "name": "userid",
      "required": True,
      "type": 3,
      "description": "Die ID des Users"
    }
  ], description="Zeigt alle Details einer Anfrage", guild_ids=[703266392295604254, 757917063070089327])
  async def _show(self, ctx: SlashContext, userid: str):
    await ctx.respond(eat=True)
    if ctx.author_id != 460143849172631553:
      await ctx.send("Du hast hierfür keine Berechtigungen! ", hidden=True)
      return

    try:
      userid = int(userid)
    except:
      await ctx.send("Wir konnten den User nicht finden!", hidden=True)
      return

    found = main.collection.find_one({
      "userid": userid
    })
    if found == None:
      await ctx.send("Wir konnten den User nicht finden!", hidden=True)
      return

    try:
      target = await self.bot.fetch_user(userid)
    except:
      await ctx.send("Wir konnten den User nicht finden!", hidden=True)
      return

    embed = Embed(title=f"Details über den Vorfall von `{target.name}#{target.discriminator}`", colour=Colour(0x56ff))
    embed.set_footer(text="This bot was created by justCoding!")
    embed.add_field(name=":globe_with_meridians:", value=f"Betreff: `{found['title']}`")
    embed.add_field(name=":book:", value=f"Kurzbeschreibung: `{found['desc']}`")
    embed.add_field(name=":mens:", value=f"Clientseitig: `{found['clientside']}`")
    embed.add_field(name=":clock1:", value=f"Zeitpunkt: `{found['time']}`")
    embed.add_field(name=":map:", value=f"Szenario: `{found['scenario']}`")
    embed.add_field(name=":card_box:", value=f"Verlorene Items: `{found['items']}`")
    embed.add_field(name=":man:", value=f"UserID: `{userid}`")
    if "conversation" in found:
      message_history = ""
      for i in found['conversation']:
        author = await self.bot.fetch_user(i['userid'])
        message_history += author.name + "#" + author.discriminator + ": *" + i['message'] + "*\n"
      
      message_history += ""
      embed.add_field(name=":books:", value=message_history)
    dm = await ctx.author.create_dm()
    await dm.send(embed=embed)
    await ctx.send(content="Wir haben dir die Details per DM zukommen lassen!", hidden=True, delete_after=7.5)


def setup(bot):
  """Sets up the cog."""
  bot.add_cog(Slash(bot))
