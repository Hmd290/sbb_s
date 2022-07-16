import os
from typing import Optional

from moviepy.editor import VideoFileClip
from PIL import Image

from ...core.logger import logging
from ...core.managers import edit_or_reply
from ..tools import media_type
from .utils import runcmd

LOGS = logging.getLogger(__name__)


async def media_to_pic(event, reply, noedits=False):  # sourcery no-metrics
    mediatype = media_type(reply)
    if mediatype not in [
        "Photo",
        "Round Video",
        "Gif",
        "Sticker",
        "Video",
        "Voice",
        "Audio",
        "Document",
    ]:
        return event, None
    if not noedits:
        sbb_sevent = await edit_or_reply(
            event, "**⎙ :: جاري التحويل انتظر قليلا  ** ...."
        )

    else:
        sbb_sevent = event
    sbb_smedia = None
    sbb_sfile = os.path.join("./temp/", "meme.png")
    if os.path.exists(sbb_sfile):
        os.remove(sbb_sfile)
    if mediatype == "Photo":
        sbb_smedia = await reply.download_media(file="./temp")
        im = Image.open(sbb_smedia)
        im.save(sbb_sfile)
    elif mediatype in ["Audio", "Voice"]:
        await event.client.download_media(reply, sbb_sfile, thumb=-1)
    elif mediatype == "Sticker":
        sbb_smedia = await reply.download_media(file="./temp")
        if sbb_smedia.endswith(".tgs"):
            sbb_scmd = f"lottie_convert.py --frame 0 -if lottie -of png '{sbb_smedia}' '{sbb_sfile}'"
            stdout, stderr = (await runcmd(sbb_scmd))[:2]
            if stderr:
                LOGS.info(stdout + stderr)
        elif sbb_smedia.endswith(".webp"):
            im = Image.open(sbb_smedia)
            im.save(sbb_sfile)
    elif mediatype in ["Round Video", "Video", "Gif"]:
        await event.client.download_media(reply, sbb_sfile, thumb=-1)
        if not os.path.exists(sbb_sfile):
            sbb_smedia = await reply.download_media(file="./temp")
            clip = VideoFileClip(media)
            try:
                clip = clip.save_frame(sbb_sfile, 0.1)
            except Exception:
                clip = clip.save_frame(sbb_sfile, 0)
    elif mediatype == "Document":
        mimetype = reply.document.mime_type
        mtype = mimetype.split("/")
        if mtype[0].lower() == "image":
            sbb_smedia = await reply.download_media(file="./temp")
            im = Image.open(sbb_smedia)
            im.save(sbb_sfile)
    if sbb_smedia and os.path.lexists(sbb_smedia):
        os.remove(sbb_smedia)
    if os.path.lexists(sbb_sfile):
        return sbb_sevent, sbb_sfile, mediatype
    return sbb_sevent, None


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    thumb_image_path = path or os.path.join(
        "./temp/", f"{os.path.basename(video_file)}.jpg"
    )
    command = f"ffmpeg -ss {duration} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await runcmd(command))[1]
    if err:
        LOGS.error(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None
