import discord
import openai
import json
import os
import sys
import time
from actions.pinterest import PinterestImageScraper

openai.api_key = "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"
client = discord.Client(intents=discord.Intents.all())

messages = ["The following is a conversation with Sherlock Holmes.\n", "Human: Hello, who are you?", "Holmes: I am Sherlock Holmes the detective. How can I help you today?"]

@client.event
async def on_ready():
    print(client.user, "Logged in.")

@client.event
async def on_message(msg):
    print(f"{msg.author.name}: {msg.content}")
    if msg.author == client.user:
        return
    content = str(msg.content)

    if content.lower().startswith("ai ") or msg.channel.name == "aichan":
        if content.lower().startswith("ai "):
            content = content[3::]
        try:
            messages.append(f"Human: {content}")
            response = openai.Completion.create(
                model="text-babbage-001",
                prompt="\n".join(messages),
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=[" Human:", " Holmes:"]
            )
            reply = response["choices"][0]["text"].replace("Holmes:", "").replace("Human:", "")
            if len(messages) > 8:
                del messages[3]
            await msg.reply(reply)
        except Exception as e:
            print(e)
            await msg.reply("error\n @D y l a n#0801")

    if content.startswith("image "):
        content = content[6::]
        result = PinterestImageScraper().make_ready(content)
        await msg.reply(str(result))


client.run("MTA4MTY1MDE0NTEzNDkyMzkyOA.Gkcc4A.EgDCwhk9xnmSAo0KgZfb9YbVdDhEcdyKruO-GM")
