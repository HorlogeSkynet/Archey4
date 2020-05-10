"""Public IP address detection class"""

from socket import timeout as SocketTimeoutError
from subprocess import check_output, DEVNULL, TimeoutExpired, CalledProcessError
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from archey.entry import Entry


class WanIp(Entry):
    """Uses different ways to retrieve the public IPv{4,6} addresses"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ipv4_addr = self._retrieve_ipv4_address()

        # IPv6 address retrieval (unless the user doesn't want it).
        if self._configuration.get('ip_settings')['wan_ip_v6_support']:
            ipv6_addr = self._retrieve_ipv6_address()
        else:
            ipv6_addr = None

        if self._format_to_json:
            self.value = list(filter(None, (ipv4_addr, ipv6_addr))) \
                or self._configuration.get('default_strings')['no_address']

        else:
            self.value = ', '.join(
                filter(None, (ipv4_addr, ipv6_addr))
            ) or self._configuration.get('default_strings')['no_address']

    def _retrieve_ipv4_address(self):
        try:
            ipv4_addr = check_output(
                [
                    'dig', '+short', '-4', 'A', 'myip.opendns.com',
                    '@resolver1.opendns.com'
                ],
                timeout=self._configuration.get('timeout')['ipv4_detection'],
                stderr=DEVNULL, universal_newlines=True
            ).rstrip()
        except (FileNotFoundError, TimeoutExpired, CalledProcessError):
            try:
                ipv4_addr = urlopen(
                    'https://v4.ident.me/',
                    timeout=self._configuration.get('timeout')['ipv4_detection']
                )
            except (HTTPError, URLError, SocketTimeoutError):
                # The machine does not seem to be connected to Internet...
                return None

            ipv4_addr = ipv4_addr.read().decode().strip()

        return ipv4_addr

    def _retrieve_ipv6_address(self):
        try:
            ipv6_addr = check_output(
                [
                    'dig', '+short', '-6', 'AAAA', 'myip.opendns.com',
                    '@resolver1.ipv6-sandbox.opendns.com'
                ],
                timeout=self._configuration.get('timeout')['ipv6_detection'],
                stderr=DEVNULL, universal_newlines=True
            ).rstrip()
        except (FileNotFoundError, TimeoutExpired, CalledProcessError):
            try:
                response = urlopen(
                    'https://v6.ident.me/',
                    timeout=self._configuration.get('timeout')['ipv6_detection']
                )
            except (HTTPError, URLError, SocketTimeoutError):
                # It looks like this machine doesn't have any IPv6 address...
                # ... or is not connected to Internet.
                return None

            ipv6_addr = response.read().decode().strip()

        return ipv6_addr
