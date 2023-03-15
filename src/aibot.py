import discord
import openai
import json
import os
import sys
import time
from actions.pinterest import PinterestImageScraper


openai.api_key = "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"
client = discord.Client(intents=discord.Intents.all())


messages = [{"role": "system", "content": "You are an assistant called Ai-Chan. Include user name."}]
def get_messages():
    global messages
    return messages
def add_message(msg):
    global messages
    messages.append(msg)
def del_message(items:list):
    global messages
    m = messages
    for i in items: del m[i]
    messages = m




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
            add_message({"role": "user", "content": f"{msg.author.name}: {content}"})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=get_messages(),
                max_tokens=150)
            print(response["usage"])
            reply = response["choices"][0]["message"]["content"]
            add_message({"role": "assistant", "content": reply})
            await msg.reply(reply)
            if len(get_messages()) > 5:
                del_message([1,2])
        except Exception as e:
            await msg.reply(e)

    if content.startswith("image "):
        content = content[6::]
        result = PinterestImageScraper().make_ready(content)
        await msg.reply(str(result))


if __name__ == "__main__":
    client.run("MTA4MTY1MDE0NTEzNDkyMzkyOA.Gkcc4A.EgDCwhk9xnmSAo0KgZfb9YbVdDhEcdyKruO-GM")
