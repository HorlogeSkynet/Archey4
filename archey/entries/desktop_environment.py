"""Desktop environment detection class"""

import os

from .constants import DE_DICT


class DesktopEnvironment:
    """
    Just iterate over running processes to find a known-entry.
    If not, rely on the `XDG_CURRENT_DESKTOP` environment variable.
    """
    def __init__(self, processes, not_detected=None):
        for key, value in DE_DICT.items():
            if key in processes:
                desktop_environment = value
                break

        else:
            # Let's rely on an environment var if the loop above didn't `break`
            desktop_environment = os.getenv(
                'XDG_CURRENT_DESKTOP',
                not_detected
            )

        self.value = desktop_environment
