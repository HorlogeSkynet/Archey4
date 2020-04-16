"""Public IP address detection class"""

from subprocess import check_output, DEVNULL, TimeoutExpired, CalledProcessError
from urllib.error import URLError
from urllib.request import urlopen

from archey.configuration import Configuration
from archey.entry import Entry


class WanIp(Entry):
    """Uses different ways to retrieve the public IPv{4,6} addresses"""
    def __init__(self):
        super().__init__()

        # The configuration object is needed to retrieve some settings below.
        self.configuration = Configuration()['entries']['WanIp']

        # IPv6 address retrieval (unless the user doesn't want it).
        if self.configuration['ipv6_support']:
            try:
                ipv6_addr = check_output(
                    [
                        'dig', '+short', '-6', 'AAAA', 'myip.opendns.com',
                        '@resolver1.ipv6-sandbox.opendns.com'
                    ],
                    timeout=(self.configuration['ipv6_timeout_secs'] / 2),
                    stderr=DEVNULL, universal_newlines=True
                ).rstrip()

            except (FileNotFoundError, TimeoutExpired, CalledProcessError):
                try:
                    ipv6_addr = urlopen(
                        'https://v6.ident.me/',
                        timeout=(self.configuration['ipv6_timeout_secs'] / 2)
                    )
                    if ipv6_addr and ipv6_addr.getcode() == 200:
                        ipv6_addr = ipv6_addr.read().decode().strip()

                except URLError:
                    # It looks like this user doesn't have any IPv6 address...
                    # ... or is not connected to Internet.
                    ipv6_addr = None

        else:
            ipv6_addr = None

        # IPv4 addresses retrieval (anyway).
        try:
            ipv4_addr = check_output(
                [
                    'dig', '+short', '-4', 'A', 'myip.opendns.com',
                    '@resolver1.opendns.com'
                ],
                timeout=(self.configuration['ipv4_timeout_secs'] / 2),
                stderr=DEVNULL, universal_newlines=True
            ).rstrip()

        except (FileNotFoundError, TimeoutExpired, CalledProcessError):
            try:
                ipv4_addr = urlopen(
                    'https://v4.ident.me/',
                    timeout=(self.configuration['ipv4_timeout_secs'] / 2)
                )
                if ipv4_addr and ipv4_addr.getcode() == 200:
                    ipv4_addr = ipv4_addr.read().decode().strip()

            except URLError:
                # The user does not look connected to Internet...
                ipv4_addr = None

        self.value = ', '.join(
            filter(None, (ipv4_addr, ipv6_addr))
        ) or Configuration()['default_strings']['no_address']
