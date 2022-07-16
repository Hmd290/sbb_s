import glob
import os

from sbb_s import sbb_s

from ..core.managers import edit_or_reply
from ..helpers.utils import _sbb_sutils

# ============================@ Constants @===============================
exts = ["jpg", "png", "webp", "webm", "m4a", "mp4", "mp3", "tgs"]

cmds = [
    "rm -rf downloads",
    "mkdir downloads",
]
# ========================================================================


@sbb_s.ar_cmd(pattern="(ري|رست)لود$")
async def _(event):
    cmd = event.pattern_match.group(1)
    sbb_s = await edit_or_reply(event, "**⌔∮ انتظر من 2-3 دقائق**")
    if cmd == "رست":
        for file in exts:
            removing = glob.glob(f"./*.{file}")
            for i in removing:
                os.remove(i)
        for i in cmds:
            await _sbb_sutils.runcmd(i)
    await event.client.reload(sbb_s)
