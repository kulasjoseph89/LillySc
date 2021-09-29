from LillySc import TOKEN, tbot
import LillySc.events

try:
    tbot.start(bot_token=TOKEN)
except Exception:
    print("Bot Token Invalid")
    exit(1)

async def start_log():
    await tbot.send_message(-1001486931338, "**Scrapper Started!**")


tbot.loop.run_until_complete(start_log())

tbot.run_until_disconnected()

