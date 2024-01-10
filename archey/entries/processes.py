"""Processes entry class"""

from archey.entry import Entry
from archey.processes import Processes as ProcessesUtil


class Processes(Entry):
    """
    Simple wrapper to `archey.processes` to provide the number of running processes as an entry.
    """

    _ICON = "\ueba2"  # cod_server_process 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.value = ProcessesUtil().number
