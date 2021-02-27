from discord.ext import commands
from discord import ChannelType
from discord import Embed
from discord import Colour
import main
from datetime import datetime
class DmConversation(commands.Cog):
  """This class is for all messages from the dms"""

  def __init__(self, bot):
    self.bot = bot
  
  @commands.Cog.listener()
  async def on_message(self, message):
    """This is called when the bot registers a message"""
    # Check if author is bot
    if message.author.bot:
      return
    # Check if channel is dm
    if message.channel.type is ChannelType.private:
      # Check if user has open case
      if main.collection.find_one({
        "userid": message.author.id
      }) is None:
        await message.channel.send("Du hast kein offenes Case!")
      # Check if time question was already answered
      elif not "time" in main.collection.find_one({
        "userid": message.author.id
      }):
        found = main.collection.find_one({
          "userid": message.author.id
        })
        operation = {"$set": {
          "time": message.content,
          "lastcontact": datetime.now()
        }}
        main.collection.update_one(found, operation)
        await message.channel.send(f"Der Zeitpunkt wurde auf `{message.content}` gesetzt.")
        await message.channel.send("Beschreibe den Lag kurz. Bitte beachte, dass sofern die Beschreibung zu ungenau ist, wir deinen Antrag nicht bearbeiten können! ")
      
      # Check if scenario question was already answered
      elif not "scenario" in main.collection.find_one({
          "userid": message.author.id
        }):
        found = main.collection.find_one({
          "userid": message.author.id
        })
        operation = {"$set": {
          "scenario": message.content,
          "lastcontact": datetime.now()
        }}
        main.collection.update_one(found, operation)
        await message.channel.send(f"Das Szenario wurde auf `{message.content}` gesetzt.")
        await message.channel.send("Nenne deine Items in einer Nachricht. Solltest du zwei Nachrichten senden, wird die zweite Nachricht ignoriert! Bitte gib Items immer mit ihrer Durability und Enchantments, sofern vorhanden, an! Unausführliche oder inkorrekte Angaben können zu einem Abbruch des Verfahrens führen! ")
      
      # Check if items question was already answered
      elif not "items" in main.collection.find_one({
          "userid": message.author.id
        }):
          found = main.collection.find_one({
            "userid": message.author.id
          })
          operation = {"$set": {
            "items": message.content,
            "lastcontact": datetime.now()
          }}
          main.collection.update_one(found, operation)
          await message.channel.send(f"Die verlorenen Items wurden auf `{message.content}` gesetzt.")

          # Generate embed
          embed = Embed(title="Angegebene Informationen", colour=Colour(0x56ff), description="Bitte kontrolliere, das die nachfolgenden Informationen korrekt sind. Sofern ja, antworte mit `Ja`. Sofern nein, antworte mit `Nein`")
          embed.set_footer(text="This bot was created by justCoding!")
          embed.add_field(name=":clock1:", value=f"Zeitpunkt: `{found['time']}`")
          embed.add_field(name=":map:", value=f"Szenario: `{found['scenario']}`")
          embed.add_field(name=":card_box:", value=f"Verlorene Items: `{message.content}`")

          # Send Embed
          await message.channel.send(embed=embed)

      # Check if wasnt confirmed
      elif not "confirmed" in main.collection.find_one({
          "userid": message.author.id
        }):
          found = main.collection.find_one({
            "userid": message.author.id
          })
          if message.content == "Ja":
            operation = {"$set": {
              "confirmed": True,
              "lastcontact": datetime.now()
            }}
            main.collection.update_one(found, operation)
          elif message.content == "Nein":
            main.collection.delete_one(found)
            await message.channel.send("Deine Anfrage wurde erfolgreich gestoppt!")
            return
          else:
            await message.channel.send("Das habe ich leider nicht verstanden. Bitte benutze nur `Ja` oder `Nein`")
            return
          # Establish dm with team member
          team_member = await self.bot.fetch_user(460143849172631553)
          team_channel = await team_member.create_dm()
          # Craft embed with information
          embed = Embed(title=f"Neue Anfrage von `{message.author.name}#{message.author.discriminator}`", colour=Colour(0x56ff), description="Bitte überprüfe die folgenden Daten und antworte dem User auf einem Server, der die Staff-Commands besitzt, mit */accept* oder */decline* oder */custom*.")
          embed.set_footer(text="This bot was created by justCoding!")
          embed.add_field(name=":globe_with_meridians:", value=f"Betreff: `{found['title']}`")
          embed.add_field(name=":book:", value=f"Kurzbeschreibung: `{found['desc']}`")
          embed.add_field(name=":clock1:", value=f"Zeitpunkt: `{found['time']}`")
          embed.add_field(name=":map:", value=f"Szenario: `{found['scenario']}`")
          embed.add_field(name=":card_box:", value=f"Verlorene Items: `{found['items']}`")
          embed.add_field(name=":man:", value=f"UserID: `{message.author.id}`")
          # Send message to team member
          await team_channel.send(embed=embed)
          # Send information to user
          await message.channel.send("Deine Anfrage wurde an ein Team-Mitglied weitergeleitet. Sofern sie vollständig, glaubwürdig und nachvollziehbar ist, wirst du deine Items in naher Zukunft zurückerhalten!")
      
      # Notify user that everything was filled in
      else:
        await message.channel.send("Du hast alle Angaben gemacht! Bitte warte, bis sich ein Teammitglied bei dir meldet!")

def setup(bot):
  """Sets up the cog."""
  bot.add_cog(DmConversation(bot))