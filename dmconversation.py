from discord.ext import commands
from discord import ChannelType
from discord import Embed
from discord import Colour
import main
from datetime import datetime
import time


class DmConversation(commands.Cog):
    """This class is for all messages from the dms."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """This is called when the bot registers a message."""
        # Check if author is bot
        if message.author.bot:
            return
        # Check if channel is dm
        if message.channel.type is ChannelType.private:
            # Search fo db entry
            found = main.collection.find_one({
                "userid": message.author.id
            })
            # Check if user has open case
            if found is None:
                await message.channel.send("Du hast kein offenes Case!")
            # Check if time question was already answered
            elif "time" not in found:
                operation = {"$set": {
                    "time": message.content,
                    "lastcontact": datetime.now()
                }}
                main.collection.update_one(found, operation)
                await message.channel.send(f"Der Zeitpunkt wurde auf `{message.content}` gesetzt.")
                embed = Embed(title="Lag-Beschreibung", colour=Colour(0x3d14eb),
                              description="Beschreibe den Lag. Folgende Fragen könnten dir einen Anhaltspunkt geben: ```Was ist dir aufgefallen, wie hat sich der Lag gegenüber dir veräußert? Was war die Todesnachricht? Bist du oft gestorben? Wenn ja, beim wievielten Tod hast du deine Items verloren? Warum konntest du deine Items nicht zurückhohlen? Sofern es mit der Situation zusammenhängt: Wo warst du auf dem Server? Bist du auf einem Boot oder in einem Minecart gefahren? Warst du an einer automatischen Farm? Hattest du in der letzten halben Stunde irgendwelche Internetprobleme? Waren andere Personen auf dem Server? Hast du mit anderen Personen währenddessen gesprochen?```",
                              timestamp=datetime.utcfromtimestamp(time.time()))

                embed.set_footer(text="This bot was created by justCoding!")

                embed.add_field(name=":question:",
                                value="Wir benutzen diese Angaben, um den Lag leichter in den Logs aufzuspüren und uns besser in die Situation einzufühlen. ")
                embed.add_field(name=":exclamation:",
                                value="Sofern die Angaben zu ungenau sind, wird dein Antrag abgelehnt. Du könntest z.B. versuchen, einen Großteil der oben genannten Beispielfragen zu beantworten.")

                await message.channel.send(embed=embed)

            # Check if scenario question was already answered
            elif "scenario" not in found:
                operation = {"$set": {
                    "scenario": message.content,
                    "lastcontact": datetime.now()
                }}
                main.collection.update_one(found, operation)
                await message.channel.send(f"Das Szenario wurde auf `{message.content}` gesetzt.")
                embed = Embed(title="Verlorene Items", colour=Colour(0x3d14eb),
                              description="Nenne deine verlorenen Items in einer Nachricht. Beachte dass deine Nachricht nicht länger als 2.000 Zeichen lang sein darf.",
                              timestamp=datetime.utcfromtimestamp(time.time()))

                embed.set_footer(text="This bot was created by justCoding!")

                embed.add_field(name=":question:",
                                value="Wir benutzen diese Angaben, um dir deine Items zurückzuerstatten.")
                embed.add_field(name=":exclamation:",
                                value="Nenne auch verlorene Enchantments. **Nicht angegebene Items werden auch auf nachträgliche Rückfrage nich erstattet.** Nimm dir also Zeit, vor dem Absenden der Nachricht oder am Ende der Konversation, deine Angaben zu überprüfen!")

                await message.channel.send(embed=embed)

            # Check if items question was already answered
            elif not "items" in found:
                operation = {"$set": {
                    "items": message.content,
                    "lastcontact": datetime.now()
                }}
                main.collection.update_one(found, operation)
                await message.channel.send(f"Die verlorenen Items wurden auf `{message.content}` gesetzt.")

                # Generate embed
                embed = Embed(title="Angegebene Informationen", colour=Colour(0x56ff),
                              description="Bitte kontrolliere, das die nachfolgenden Informationen korrekt sind. Sofern ja, antworte mit `Ja`. Sofern nein, antworte mit `Nein`")
                embed.set_footer(text="This bot was created by justCoding!")
                embed.add_field(name=":clock1:", value=f"Zeitpunkt: `{found['time']}`")
                embed.add_field(name=":map:", value=f"Szenario: `{found['scenario']}`")
                embed.add_field(name=":card_box:", value=f"Verlorene Items: `{message.content}`")

                # Send Embed
                await message.channel.send(embed=embed)

            # Check if wasnt confirmed
            elif not "confirmed" in found:
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
                    await message.channel.send(
                        "Das habe ich leider nicht verstanden. Bitte benutze nur `Ja` oder `Nein`")
                    return
                # Craft embed with information
                embed = Embed(title=f"Neue Anfrage von `{message.author.name}#{message.author.discriminator}`",
                              colour=Colour(0x56ff),
                              description="Bitte überprüfe die folgenden Daten und antworte dem User auf einem Server, der die Staff-Commands besitzt, mit */accept* oder */decline* oder */custom*.")
                embed.set_footer(text="This bot was created by justCoding!")
                embed.add_field(name=":globe_with_meridians:", value=f"Betreff: `{found['title']}`")
                embed.add_field(name=":book:", value=f"Kurzbeschreibung: `{found['desc']}`")
                embed.add_field(name=":mens:", value=f"Clientseitig: `{found['clientside']}`")
                embed.add_field(name=":clock1:", value=f"Zeitpunkt: `{found['time']}`")
                embed.add_field(name=":map:", value=f"Szenario: `{found['scenario']}`")
                embed.add_field(name=":card_box:", value=f"Verlorene Items: `{found['items']}`")
                embed.add_field(name=":man:", value=f"UserID: `{message.author.id}`")
                for member in main.team_members:
                  dm = await (await self.bot.fetch_user(member)).create_dm()
                  await dm.send(embed=embed)
                # Send information to user
                embed = Embed(title="Erfolgreiche Übertragung", colour=Colour(0x3d14eb),
                              description="Deine Nachricht wurde erfolgreich an die Organisation übertragen. Bitte habe etwas Geduld, die Bearbeitung deiner Anfrage sollte normalerweise nicht länger als drei Tage dauern. Du erhälst dann eine Nachricht hier über den Chat! Wir öffnen hier nun ein Ticket-System. Jede Nachricht wird ab jetzt mit in die Datei aufgenommen. ",
                              timestamp=datetime.utcfromtimestamp(time.time()))

                embed.set_footer(text="This bot was created by justCoding!")

                embed.add_field(name=":question:",
                                value="Du fragst dich jetzt vielleicht, warum wir so ein kompliziertes System nutzen. Die Antwort darauf ist ganz einfach: Weil es am Ende so doch viel einfacher ist. Ohne unnötiges Hin- und Herschreiben mit Teammitgliedern werden alle wichtigen Informationen eingeholt! ")
                embed.add_field(name=":exclamation:",
                                value="Bitte achte auf deine DMs. Möglicherweise schon akzeptierte Anfragen können fallen gelassen werden, wenn du nicht antwortest!")
                await message.channel.send(embed=embed)

            # Notify user that everything was filled in
            else:
                found = main.collection.find_one({
                    "userid": message.author.id
                })
                if not "conversation" in found:
                    main.collection.update_one(filter={
                        "userid": message.author.id
                    }, update={
                        "$set": {
                            "conversation": [{
                                "userid": message.author.id,
                                "message": message.content
                            }]
                        }
                    })
                    found = main.collection.find_one({
                        "userid": message.author.id
                    })
                    embed = Embed(title=f"Neue Nachricht von `{message.author.name}#{message.author.discriminator}`",
                                  colour=Colour(0x56ff))
                    embed.set_footer(text="This bot was created by justCoding!")
                    embed.add_field(name=":globe_with_meridians:", value=f"Betreff: `{found['title']}`")
                    embed.add_field(name=":book:", value=f"Kurzbeschreibung: `{found['desc']}`")
                    embed.add_field(name=":mens:", value=f"Clientseitig: `{found['clientside']}`")
                    embed.add_field(name=":clock1:", value=f"Zeitpunkt: `{found['time']}`")
                    embed.add_field(name=":map:", value=f"Szenario: `{found['scenario']}`")
                    embed.add_field(name=":card_box:", value=f"Verlorene Items: `{found['items']}`")
                    embed.add_field(name=":man:", value=f"UserID: `{message.author.id}`")
                    message_history = ""
                    for i in found['conversation']:
                        author = await self.bot.fetch_user(i['userid'])
                        message_history += author.name + "#" + author.discriminator + ": *" + i['message'] + "*\n"

                    message_history += ""
                    embed.add_field(name=":books:", value=message_history)

                    for member in main.team_members:
                        dm = await (await self.bot.fetch_user(member)).create_dm()
                        await dm.send(embed=embed)

                    await message.channel.send("Deine Nachricht wurde erfolgreich übermittelt.")
                    await message.channel.send(embed=embed)

                else:
                    found_conversation = main.collection.find_one({
                        "userid": message.author.id
                    })['conversation']
                    found_conversation.append({
                        "userid": message.author.id,
                        "message": message.content
                    })
                    main.collection.update_one({
                        "userid": message.author.id
                    }, {
                        "$set": {
                            "conversation": found_conversation
                        }
                    })
                    found = main.collection.find_one({
                        "userid": message.author.id
                    })
                    embed = Embed(title=f"Neue Nachricht von `{message.author.name}#{message.author.discriminator}`",
                                  colour=Colour(0x56ff))
                    embed.set_footer(text="This bot was created by justCoding!")
                    embed.add_field(name=":globe_with_meridians:", value=f"Betreff: `{found['title']}`")
                    embed.add_field(name=":book:", value=f"Kurzbeschreibung: `{found['desc']}`")
                    embed.add_field(name=":mens:", value=f"Clientseitig: `{found['clientside']}`")
                    embed.add_field(name=":clock1:", value=f"Zeitpunkt: `{found['time']}`")
                    embed.add_field(name=":map:", value=f"Szenario: `{found['scenario']}`")
                    embed.add_field(name=":card_box:", value=f"Verlorene Items: `{found['items']}`")
                    embed.add_field(name=":man:", value=f"UserID: `{message.author.id}`")
                    message_history = ""
                    for i in found['conversation']:
                        author = await self.bot.fetch_user(i['userid'])
                        message_history += author.name + "#" + author.discriminator + ": *" + i['message'] + "*\n"

                    message_history += ""
                    embed.add_field(name=":books:", value=message_history)

                    for member in main.team_members:
                        dm = await (await self.bot.fetch_user(member)).create_dm()
                        await dm.send(embed=embed)

                    await message.channel.send("Deine Nachricht wurde erfolgreich übermittelt.")
                    await message.channel.send(embed=embed)


def setup(bot):
    """Sets up the cog."""
    bot.add_cog(DmConversation(bot))
