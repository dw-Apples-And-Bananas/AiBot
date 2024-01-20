from openai import OpenAI, completions

with open("key") as f:
    key = f.readlines()
client = OpenAI(
  api_key=key[1].replace("\n","")
)

messages = [{"role": "system", "content": "You are an assistant called Ai-Chan."}]
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


async def request(msg, content):
    add_message({"role": "user", "content": f"{msg.author.name}: {content}"})
    completion = client.chat.completions.create(model='gpt-4', messages=get_messages())
    reply = completion.choices[0].message.content
    add_message({"role": "assistant", "content": reply})
    if len(get_messages()) > 5:
        del_message([1,2])
    await msg.reply(reply)
