import disnake
from disnake.ext import commands
from time import time
import re
import sqlite3

conn = sqlite3.connect("words.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS main (word TEXT, count INT)")
conn.commit()

regular = re.compile('[a-z0-9а-яё_]+')
relink = re.compile('(https?:\/\/)?([\w-]{1,32}\.[\w-]{1,32})[^\s@]')

bot = commands.Bot(intents = disnake.Intents.all())

@bot.slash_command()
async def count(inter):
    timer = time()
    counter = 0
    await inter.response.send_message("processing...")
    for channel in inter.guild.channels:
        if isinstance(channel, disnake.TextChannel):
            async for message in channel.history(limit = 300000):
                counter += 1
                print(counter)
                text = message.content.lower()
                try: 
                    text = re.subn('(https?:\/\/)([\w-]{1,32}\.[\w-]{1,32})[^\s@]*', '', text)[0]
                except:
                    pass
                words = regular.findall(text)
                for word in words:
                    if len(word) == 1: continue
                    entry = cursor.execute("SELECT * FROM main WHERE word = ?", (word, )).fetchone()
                    if entry != None:
                        cursor.execute("UPDATE main SET count = ? + 1 WHERE word = ?", (entry[1], word))
                        conn.commit()
                    else:
                        cursor.execute("INSERT INTO main (word, count) VALUES (?, ?)", (word, 1))
                        conn.commit()
    await inter.channel.send(f"{counter} messages iterated in {time() - timer} seconds")


bot.run('YOUR_BOT_TOKEN')