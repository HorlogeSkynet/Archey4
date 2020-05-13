"""Local IP addresses detection class"""

import netifaces

from archey.entry import Entry


class LanIp(Entry):
    """Relies on the `netifaces` module to detect LAN IP addresses"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        address_types = [netifaces.AF_INET]
        if self._configuration.get('ip_settings')['lan_ip_v6_support']:
            address_types.append(netifaces.AF_INET6)

        ip_addresses = []

        # Loop through all available network interfaces.
        for if_name in netifaces.interfaces():
            # Fetch associated addresses elements.
            if_addrs = netifaces.ifaddresses(if_name)

            # For each IPv4 (or IPv6 address)...
            for addr_type in address_types:
                if addr_type not in if_addrs:
                    continue

                for if_addr in if_addrs[addr_type]:
                    # Filter out loopback addresses.
                    if (addr_type == netifaces.AF_INET and if_addr['addr'].startswith('127.')) \
                        or if_addr['addr'] == '::1':
                        continue

                    ip_addresses.append(if_addr['addr'].split('%')[0])

        lan_ip_max_count = self._configuration.get('ip_settings')['lan_ip_max_count']
        if lan_ip_max_count is not False:
            ip_addresses = ip_addresses[:lan_ip_max_count]

        self.value = ip_addresses or self._configuration.get('default_strings')['no_address']


    def output(self, output):
        """Adds the entry to `output` after pretty-formatting the IP address list."""
        if isinstance(self.value, list):
            # If we found IP addresses, join them together nicely.
            output.append(
                self.name,
                ', '.join(self.value)
            )
        else:
            # Otherwise go with the default behaviour for the "no address" string.
            super().output(output)
