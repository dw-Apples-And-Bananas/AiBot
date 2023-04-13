import discord
import json
import os
import sys
import time
from definitions import definitions
import components


client = discord.Client(intents=discord.Intents.all())

devmode = True

@client.event
async def on_ready():
    print(client.user, "Logged in.")


@client.event
async def on_message(msg):
    print(f"{msg.author.name}: {msg.content}")
    if msg.author == client.user:
        return
    content = str(msg.content)

    func = content.split(" ")[0].lower()
    arg = " ".join(content.split(" ")[1::]) if len(content.split(" ")) > 0 else ""

    if devmode:
        await definitions[func](msg, arg)
    else:
        try:
            await definitions[func](msg, arg)
        except:
            pass

    await definitions["events.remind"](msg, "")

    # if content.startswith("image "):
    #     content = content[6::]
    #     result = PinterestImageScraper().make_ready(content)
    #     await msg.reply(str(result))

if __name__ == "__main__":
    with open("key") as f:
        key = f.readlines()
    client.run(key[0])
