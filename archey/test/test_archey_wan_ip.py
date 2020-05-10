"""Test module for Archey's public IP address detection module"""

import unittest
from unittest.mock import patch

from socket import timeout as SocketTimeoutError
from subprocess import TimeoutExpired
from urllib.error import URLError

from archey.entries.wan_ip import WanIp


class TestWanIpEntry(unittest.TestCase):
    """
    Here, we mock calls to `dig` or `urlopen`.
    """
    @patch(
        'archey.entries.wan_ip.check_output',
        side_effect=[
            'XXX.YY.ZZ.TTT\n',
            '0123::4567:89a:dead:beef\n'
        ]
    )
    @patch(
        'archey.configuration.Configuration.get',
        side_effect=[
            {'ipv4_detection': None},  # Needed key.
            {'wan_ip_v6_support': True},
            {'ipv6_detection': None}  # Needed key.
        ]
    )
    def test_ipv6_and_ipv4(self, _, __):
        """Test the regular case : Both IPv4 and IPv6 are retrieved"""
        self.assertEqual(
            WanIp().value,
            'XXX.YY.ZZ.TTT, 0123::4567:89a:dead:beef'
        )

    @patch(
        'archey.entries.wan_ip.check_output',
        return_value='XXX.YY.ZZ.TTT'
    )
    @patch(
        'archey.configuration.Configuration.get',
        side_effect=[
            {'ipv4_detection': None},  # Needed key.
            {'wan_ip_v6_support': False}
        ]
    )
    def test_ipv4_only(self, _, __):
        """Test only public IPv4 detection"""
        self.assertEqual(
            WanIp().value,
            'XXX.YY.ZZ.TTT'
        )

    @patch(
        'archey.entries.wan_ip.check_output',
        side_effect=[
            'XXX.YY.ZZ.TTT',            # The IPv4 address is detected
            TimeoutExpired('dig', 1)  # `check_output` call will fail
        ]
    )
    @patch('archey.entries.wan_ip.urlopen')
    @patch(
        'archey.configuration.Configuration.get',
        side_effect=[
            {'ipv4_detection': None},   # Needed key.
            {'wan_ip_v6_support': True},
            {'ipv6_detection': None},  # Needed key.
            {'ipv6_detection': None}   # Needed key.
        ]
    )
    def test_ipv6_timeout(self, _, urlopen_mock, ___):
        """Test when `dig` call timeout for the IPv6 detection"""
        urlopen_mock.return_value.read.return_value = b'0123::4567:89a:dead:beef\n'

        self.assertEqual(
            WanIp().value,
            'XXX.YY.ZZ.TTT, 0123::4567:89a:dead:beef'
        )

    @patch(
        'archey.entries.wan_ip.check_output',
        side_effect=TimeoutExpired('dig', 1)  # `check_output` call will fail
    )
    @patch(
        'archey.entries.wan_ip.urlopen',
        side_effect=URLError('<urlopen error timed out>')  # `urlopen` call will fail
    )
    @patch(
        'archey.configuration.Configuration.get',
        side_effect=[
            {'ipv4_detection': None},  # Needed key.
            {'ipv4_detection': None},  # Needed key.
            {'wan_ip_v6_support': False},
            {'no_address': 'No Address'}
        ]
    )
    def test_ipv4_timeout_twice(self, _, __, ___):
        """Test when both `dig` and `URLOpen` trigger timeouts..."""
        self.assertEqual(WanIp().value, 'No Address')

    @patch(
        'archey.entries.wan_ip.check_output',
        side_effect=TimeoutExpired('dig', 1)  # `check_output` call will fail
    )
    @patch(
        'archey.entries.wan_ip.urlopen',
        side_effect=SocketTimeoutError('The read operation timed out')  # `urlopen` call will fail
    )
    @patch(
        'archey.configuration.Configuration.get',
        side_effect=[
            {'ipv4_detection': None},  # Needed key.
            {'ipv4_detection': None},  # Needed key.
            {'wan_ip_v6_support': False},
            {'no_address': 'No Address'}
        ]
    )
    def test_ipv4_timeout_twice_socket_error(self, _, __, ___):
        """Test when both `dig` timeouts and `URLOpen` raises `socket.timeout`..."""
        self.assertEqual(WanIp().value, 'No Address')

    @patch(
        'archey.entries.wan_ip.check_output',
        return_value=''  # No address will be returned
    )
    @patch(
        'urllib.request.urlopen',
        return_value=None  # No object will be returned
    )
    @patch(
        'archey.configuration.Configuration.get',
        side_effect=[
            {'ipv4_detection': None},  # Needed key.
            {'wan_ip_v6_support': False},
            {'no_address': 'No Address'}
        ]
    )
    def test_no_address(self, _, __, ___):
        """Test when no address could be retrieved"""
        self.assertEqual(WanIp().value, 'No Address')


    @patch(
        'archey.entries.wan_ip.urlopen',
        side_effect=URLError('<urlopen error timed out>')  # all `urlopen` calls will fail
    )
    @patch('archey.configuration.Configuration.get')
    @patch('archey.entries.wan_ip.check_output')
    def test_wan_ip_json_output(self, ip_cmd_mock, config_mock, __):
        """Test the JSON output of `WanIp`"""
        # Test with two addresses
        config_mock.side_effect = [
            {'ipv4_detection': None},  # Needed key.
            {'wan_ip_v6_support': True},
            {'ipv6_detection': None}  # Needed key.
        ]
        ip_cmd_mock.side_effect = [
            'XXX.YY.ZZ.TTT\n',
            '0123::4567:89a:dead:beef\n'
        ]
        self.assertListEqual(
            WanIp(format_to_json=True).value,
            ['XXX.YY.ZZ.TTT', '0123::4567:89a:dead:beef'],
            msg='Testing two addresses'
        )

        # Test with one address
        config_mock.side_effect = [
            {'ipv4_detection': None},  # Needed key.
            {'wan_ip_v6_support': False}
        ]
        ip_cmd_mock.side_effect = [
            'XXX.YY.ZZ.TTT\n'
        ]
        self.assertListEqual(
            WanIp(format_to_json=True).value,
            ['XXX.YY.ZZ.TTT'],
            msg='Testing one address'
        )

        # Test with no addresses
        config_mock.side_effect = [
            {'ipv4_detection': None},  # Needed key.
            {'ipv4_detection': None},  # Needed key.
            {'wan_ip_v6_support': False},
            {'no_address': 'No Address'}
        ]
        ip_cmd_mock.side_effect = TimeoutExpired('dig', 1)
        self.assertEqual(
            WanIp(format_to_json=True).value,
            'No Address',
            msg='Testing no addresses (timeout)'
        )


if __name__ == '__main__':
    unittest.main()
