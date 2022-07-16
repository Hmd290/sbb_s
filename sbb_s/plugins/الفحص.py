import random
import time
from datetime import datetime
from platform import python_version

from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)

from sbb_s import StartTime, sbb_s, sbb_sversion

from ..core.managers import edit_or_reply
from ..helpers.functions import check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention


@sbb_s.ar_cmd(pattern="فحص$")
async def amireallyalive(event):
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    sbb_sevent = await edit_or_reply(
        event,
        "**⌔∮ عزيزي المستخدم اذا هذه الرسالة بقت ولم تظهر لك كليشه الفحص يرجى اضاف الكليشه بشكل صحيح مره اخرى**",
    )
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  ✥ "
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "₰ [𝙧𝙚𝙙𝙩𝙝𝙤𝙣 𝙖𝙧𝙖𝙗𝙞𝙘 𝙪𝙨𝙚𝙧𝙗𝙤𝙩](t.me/redthon) ₰"
    sbb_s_IMG = gvarstatus("ALIVE_PIC")
    sbb_s_caption = gvarstatus("ALIVE_TEMPLATE") or temp
    caption = sbb_s_caption.format(
        ALIVE_TEXT=ALIVE_TEXT,
        EMOJI=EMOJI,
        mention=mention,
        uptime=uptime,
        telever=version.__version__,
        jmver=sbb_sversion,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
    )
    if sbb_s_IMG:
        sbb_s = [x for x in sbb_s_IMG.split()]
        PIC = random.choice(sbb_s)
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=caption, reply_to=reply_to_id
            )
            await sbb_sevent.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                sbb_sevent,
                f"**⌔∮ عليك استخدام رابط تليجراف لا يمكن استخدام اي رابط ثاني واعد استخدام الامر  ⪼  `.اضف صورة الحماية` <بالرد على الرابط> ",
            )
    else:
        await edit_or_reply(
            sbb_sevent,
            caption,
        )


temp = """{ALIVE_TEXT}
**{EMOJI} قاعدۿ البيانات :** `{dbhealth}`
**{EMOJI} أصـدار التـيليثون :** `{telever}`
**{EMOJI} أصـدار ردثـــون :** `{jmver}`
**{EMOJI} الوقت:** `{uptime}` 
**{EMOJI} أصدار البـايثون :** `{pyver}`
**{EMOJI} المسـتخدم:** {mention}"""



from sbb_s import sbb_s
from telethon import events
from telethon import version
from platform import python_version

@sbb_s.ar_cmd(pattern="ردثون$")
async def _(event):
    await event.delete()
    redthonget = await event.get_sender()
    hnarsl = event.to_id
    redthon_pic = "https://telegra.ph/file/7bac18f40e26d091b6720.jpg"
    await sbb_s.send_file(hnarsl, redthon_pic, caption=f"اهلا بك {redthonget.first_name}\n\n اصدار ردثون: 5.0.0\n اصدار البايثون: {python_version()}\n اصدار التيليثون: {version.__version__}\n\nشكرا لك\nردثون™")
