"""Distribution and architecture detection class"""

from subprocess import check_output

import distro

from archey.entry import Entry


class Distro(Entry):
    """Uses `distro` module and `uname` system program to format `${DISTRO} [${ARCH}]` string"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        distro_name = distro.name(pretty=True)
        if not distro_name:
            distro_name = self._configuration.get('default_strings')['not_detected']

        architecture = check_output(
            ['uname', '-m'],
            universal_newlines=True
        ).rstrip()

        self.value = '{0} [{1}]'.format(distro_name, architecture)
