"""Entry base class"""

import logging
from abc import ABC as AbstractBaseClass
from abc import abstractmethod
from functools import cached_property
from typing import Optional

from archey.configuration import Configuration


class Entry(AbstractBaseClass):
    """Module base class"""

    _PRETTY_NAME: Optional[str] = None

    def __new__(cls, *_, **kwargs):
        """Hook object instantiation to handle our particular `disabled` config field"""
        if kwargs.get("options", {}).pop("disabled", False):
            return None

        return super().__new__(cls)

    @abstractmethod
    def __init__(
        self, name: Optional[str] = None, value=None, options: Optional[dict] = None, index: int = 0
    ):
        # Each entry will have always have the following attributes...
        # `name`: key (defaults to the instantiated entry class name);
        # `value`: value of entry as an appropriate object;
        # `options`: configuration options *specific* to an entry instance;
        # 'index': 0-based index (i.e. location in the list) of the entry;
        self.name = name or self._PRETTY_NAME or self.__class__.__name__
        self.value = value
        self.options = options or {}
        self.index = index

        # Propagates a reference to default strings specified in `Configuration`.
        self._default_strings = Configuration().get("default_strings")

        # Provision a logger for each entry.
        self._logger = logging.getLogger(self.__module__)

    @cached_property
    def pretty_value(self) -> [(str, str)]:
        """Provide a "pretty" value. Can be overridden by subclasses."""
        if self.value:
            # Let's assume we can just use `__str__` on the object in _value,
            # and create a single-line output with it.
            return [(self.name, str(self.value))]
        else:
            # If the value is "falsy" leave a generic "Not detected" message for this entry.
            return [(self.name, self._default_strings.get("not_detected"))]
