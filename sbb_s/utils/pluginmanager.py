import importlib
import sys
from pathlib import Path

from sbb_s import CMD_HELP, LOAD_PLUG

from ..Config import Config
from ..core import LOADED_CMDS, PLG_INFO
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..core.session import sbb_s
from ..helpers.tools import media_type
from ..helpers.utils import _format, _sbb_stools, _sbb_sutils, install_pip, reply_id
from .decorators import admin_cmd, sudo_cmd

LOGS = logging.getLogger("sbb_s")


def load_module(shortname, plugin_path=None):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        path = Path(f"sbb_s/plugins/{shortname}.py")
        checkplugins(path)
        name = "sbb_s.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("تم بنجاح تثبيت ملف " + shortname)
    else:
        if plugin_path is None:
            path = Path(f"sbb_s/plugins/{shortname}.py")
            name = f"sbb_s.plugins.{shortname}"
        else:
            path = Path((f"{plugin_path}/{shortname}.py"))
            name = f"{plugin_path}/{shortname}".replace("/", ".")
        checkplugins(path)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = sbb_s
        mod.LOGS = LOGS
        mod.Config = Config
        mod._format = _format
        mod.tgbot = sbb_s.tgbot
        mod.sudo_cmd = sudo_cmd
        mod.CMD_HELP = CMD_HELP
        mod.reply_id = reply_id
        mod.admin_cmd = admin_cmd
        mod._sbb_sutils = _sbb_sutils
        mod._sbb_stools = _sbb_stools
        mod.media_type = media_type
        mod.edit_delete = edit_delete
        mod.install_pip = install_pip
        mod.parse_pre = _format.parse_pre
        mod.edit_or_reply = edit_or_reply
        mod.logger = logging.getLogger(shortname)
        mod.borg = sbb_s
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["sbb_s.plugins." + shortname] = mod
        LOGS.info("تم بنجاح تثبيت ملف " + shortname)


def remove_plugin(shortname):
    try:
        cmd = []
        if shortname in PLG_INFO:
            cmd += PLG_INFO[shortname]
        else:
            cmd = [shortname]
        for cmdname in cmd:
            if cmdname in LOADED_CMDS:
                for i in LOADED_CMDS[cmdname]:
                    sbb_s.remove_event_handler(i)
                del LOADED_CMDS[cmdname]
        return True
    except Exception as e:
        LOGS.error(e)
    try:
        for i in LOAD_PLUG[shortname]:
            sbb_s.remove_event_handler(i)
        del LOAD_PLUG[shortname]
    except BaseException:
        pass
    try:
        name = f"sbb_s.plugins.{shortname}"
        for i in reversed(range(len(sbb_s._event_builders))):
            ev, cb = sbb_s._event_builders[i]
            if cb.__module__ == name:
                del sbb_s._event_builders[i]
    except BaseException:
        raise ValueError


def checkplugins(filename):
    with open(filename, "r") as f:
        filedata = f.read()
    filedata = filedata.replace("sendmessage", "send_message")
    filedata = filedata.replace("sendfile", "send_file")
    filedata = filedata.replace("editmessage", "edit_message")
    with open(filename, "w") as f:
        f.write(filedata)