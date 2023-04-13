import openai

openai.api_key = "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"

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


async def request(msg, content):
    add_message({"role": "user", "content": f"{msg.author.name}: {content}"})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=get_messages(),
    )
    print(response["usage"])
    reply = response["choices"][0]["message"]["content"]
    add_message({"role": "assistant", "content": reply})
    if len(get_messages()) > 5:
        del_message([1,2])
    await msg.reply(reply)
