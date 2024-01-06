"""Windows manager detection class"""

import os
import platform
import re
from subprocess import DEVNULL, CalledProcessError, check_output

from archey.configuration import Configuration
from archey.entry import Entry
from archey.processes import Processes

WM_DICT = {
    "Amethyst": "Amethyst",
    "awesome": "Awesome",
    "beryl": "Beryl",
    "blackbox": "Blackbox",
    "bspwm": "bspwm",
    "cinnamon": "Cinnamon",
    "chunkwm": "ChunkWM",
    "compiz": "Compiz",
    "deepin-wm": "Deepin WM",
    "dwm": "DWM",
    "enlightenment": "Enlightenment",
    "herbstluftwm": "herbstluftwm",
    "fluxbox": "Fluxbox",
    "fvwm": "FVWM",
    "i3": "i3",
    "icewm": "IceWM",
    "kwin_x11": "KWin",
    "kwin_wayland": "KWin",
    "metacity": "Metacity",
    "musca": "Musca",
    "openbox": "Openbox",
    "pekwm": "PekWM",
    "qtile": "QTile",
    "ratpoison": "RatPoison",
    "Rectangle": "Rectangle",
    "scrotwm": "ScrotWM",
    "Spectacle": "Spectacle",
    "stumpwm": "StumpWM",
    "subtle": "Subtle",
    "monsterwm": "MonsterWM",
    "wingo": "Wingo",
    "wmaker": "Window Maker",
    "wmfs": "Wmfs",
    "wmii": "wmii",
    "xfwm4": "Xfwm",
    "xmonad": "Xmonad",
    "yabai": "Yabai",
}


class WindowManager(Entry):
    # Icons
    configuration = Configuration()
    icon = configuration.get("icon")

    if icon == True:
        _PRETTY_NAME = "\ueae4 Window Manager"
    else:
        _PRETTY_NAME = "Window Manager"

    """
    Uses `wmctrl` to retrieve some information about the window manager.
    If not available, fall back on a simple iteration over the processes.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.value = re.search(  # type: ignore
                r"(?<=Name: ).*",
                check_output(["wmctrl", "-m"], stderr=DEVNULL, universal_newlines=True),
            ).group(0)

            # Check Display-Server-Protokoll

            session = os.environ.get('XDG_SESSION_TYPE', '')
            if session == "x11":
                session = "X11"
            elif session == "wayland":
                session = "Wayland"

            if session != "":
                self.value = self.value + " (" + session + ")"

        except (FileNotFoundError, CalledProcessError):
            processes = Processes().list
            for wm_id, wm_name in WM_DICT.items():
                if wm_id in processes:
                    self.value = wm_name
                    break
            else:
                if platform.system() == "Darwin":
                    self.value = "Quartz Compositor"
