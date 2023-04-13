import components.ai as ai
import components.events as events

definitions = {
        "ai": ai.request,
        "events": events.events.read,
        "events.add": events.events.add,
        "events.join": events.events.join,
        "events.remind": events.events.remind,
        "events.help": events.events.help,
}
