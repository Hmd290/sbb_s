import sys

import sbb_s
from sbb_s import BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from .Config import Config
from .core.logger import logging
from .core.session import sbb_s
from .utils import mybot  # love,
from .utils import (
    add_bot_to_logger_group,
    load_plugins,
    saves,
    setup_bot,
    startupmessage,
    verifyLoggerGroup,
)

LOGS = logging.getLogger("arabic")

cmdhr = Config.COMMAND_HAND_LER


try:
    LOGS.info("يتم اعداد البوت")
    sbb_s.loop.run_until_complete(setup_bot())
    LOGS.info("تم تحميل بيانات البوت المساعد")
except Exception as e:
    LOGS.error(f"{e}")
    sys.exit()

# try:
# LOGS.info("يتم تفعيل ردثون")
# sbb_s.loop.run_until_complete(love())
# LOGS.info("تم تفعيل ردثون")
# except Exception as meo:
#  LOGS.error(f"- {meo}")


try:
    LOGS.info("يتم تفعيل وضع الانلاين")
    sbb_s.loop.run_until_complete(mybot())
    LOGS.info("تم تفعيل وضع الانلاين بنجاح ✓")
except Exception as meo:
    LOGS.error(f"- {meo}")

try:
    LOGS.info("يتم تفعيل وضع حمايه الحساب من الاختراق")
    sbb_s.loop.create_task(saves())
    LOGS.info("تم تفعيل وضع حمايه الحساب من الاختراق")
except Exception as bb:
    LOGS.error(f"- {bb}")


async def startup_process():
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    print("تم الان بنجاح اكتمال تنصيب بوت ردثون !!!")
    print(
        f"مبروك الان اذهب في التلجرام و ارسل {cmdhr}الاوامر لرؤية اذا كان البوت شغال\
        \n اذا احتجت مساعده اذهب الى مجموعه https://t.me/redthon_support"
    )
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    return


sbb_s.loop.run_until_complete(startup_process())
if len(sys.argv) not in (1, 3, 4):
    sbb_s.disconnect()
else:
    try:
        sbb_s.run_until_disconnected()
    except ConnectionError:
        pass
