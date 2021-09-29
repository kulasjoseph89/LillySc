import inspect
import time
import logging
import re
from pathlib import Path

from telethon import events, Button
from telethon.tl import functions
from telethon.tl import types
import glob, asyncio
import sys
from LillySc import tbot

def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import importlib
        import LillySc.events

        path = Path(f"LillySc./modules/{shortname}.py")
        name = "LillySc.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Successfully imported " + shortname)
    else:
        import importlib
        import LillySc.events

        path = Path(f"LillySc/modules/{shortname}.py")
        name = "LillySc.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.tbot = tbot
        mod.logger = logging.getLogger(shortname)
        spec.loader.exec_module(mod)
        sys.modules["LillySc.modules." + shortname] = mod
        print("Successfully imported " + shortname)


path = "LillySc/modules/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))
