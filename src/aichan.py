import discord
import openai
import json

openai.api_key = "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"
client = discord.Client(intents=discord.Intents.all())

messages = []
messages.append({"role": "system", "content": "You are an assistant called Ai-Chan."})

with open("./history.json", "r") as f:
    history = json.load(f)
with open("./data.json", "r") as f:
    data = json.load(f)

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
        messages.append({"role": "user", "content": f"{msg.author.name}: {content}"})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        await msg.reply(reply)
        history[response["created"]] = {"author":str(msg.author.id), "message":content, "response":reply, "usage":response["usage"]}
        with open("./history.json", "w") as f:
            json.dump(history, f, indent=2)
        try:
            data[str(msg.author.id)]["tokens"] += response["usage"]["total_tokens"]
        except:
            data[str(msg.author.id)] = {"tokens": response["usage"]["total_tokens"]}
        with open("./data.json", "w") as f:
            json.dump(data, f, indent=2)

    if content.startswith("image "):
        return
        content = content[6::]
        response = openai.Image.create(
          prompt=content,
          n=1,
          size="1024x1024"
        )
        image_url = response['data'][0]['url']
        await msg.reply(image_url)


client.run("MTA4MTY1MDE0NTEzNDkyMzkyOA.Gkcc4A.EgDCwhk9xnmSAo0KgZfb9YbVdDhEcdyKruO-GM")