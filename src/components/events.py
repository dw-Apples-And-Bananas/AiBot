import json
import time
from datetime import datetime


class Events(dict):
    def __init__(self):
        with open("./events.json") as f:
            super().__init__(json.load(f))
        self.last_reminder = time.time() - 14400

    async def read(self, msg, content):
        output = []
        for i, event in enumerate(self):
            date = self[event]["date"]
            desc = self[event]["desc"]
            joined = "(Joined)" if msg.author.id in self[event]["participants"] else "(Not Joined)"
            output.append(f"{i+1}. {event} [date: {date}, desc: {desc}] {joined}")
        await msg.reply("\n".join(output)+"\n\nTo join an event run `events.join 'event'`")

    def write(self):
        with open("./events.json", "w") as f:
            json.dump(self, f, indent=2)

    async def add(self, msg, content):
        name, date, desc = content.split("/")
        self[name] = {"date":date,"desc":desc,"participants":[]}
        self.write()
        await msg.reply(f"**Added Event**\nname: {name}\ndate: {date}\ndescription: {desc}\n\nTo edit event run `events.help edit`")

    async def join(self, msg, content):
        if content in [event for event in self]:
            self[content]["participants"].append(msg.author.id)
            self.write()
            await msg.reply(f"You have joined '{content}', I will notify you when the event starts.")
        else:
            await msg.reply("If your having trouble run `events.help join`")

    async def remind(self, msg, content):
        if time.time() - self.last_reminder > 14400 or content == "force":
            self.last_reminder = time.time()
            output = ["**Events Reminder**"]
            for event in self:
                today = datetime.today()
                date = datetime.strptime(self[event]["date"], "%Y-%m-%d %H:%M")
                diff = date-today
                output.append(f"{diff.days} days until {event}")
            await msg.channel.send("\n".join(output))

    async def help(self, msg, content):
        content = content.lower()
        if content == "add":
            await msg.reply("`events.add 'name/year-month-day hour-minute/description'`\nexample: `events.add JPod Anniversary/2023-12-31 15:30/Celebrating the anniversary of Jpod! Join VC.`")
        else:
            await msg.reply("`events.help 'function'`\nexample: `events.help add`")


events = Events()

