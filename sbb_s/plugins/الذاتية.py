from sbb_s import sbb_s
from telethon import events
from os import remove

@sbb_s.ar_cmd(pattern="(جلب الصورة|ذاتية)")
async def datea(event):
    await event.delete()
    scertpic = await event.get_reply_message()
    downloadredthon = await scertpic.download_media()
    send = await sbb_s.send_file("me", downloadredthon)
    remove(downloadredthon)
