"""Test module for Archey's terminal detection module"""

import unittest
from unittest.mock import MagicMock, patch

from archey.entries.terminal import Terminal


class TestTerminalEntry(unittest.TestCase):
    """
    For this entry, we'll verify that the output contains what the environment
      is supposed to give, plus the right number of "colorized" characters.
    """
    @patch(
        'archey.entries.terminal.os.getenv',
        return_value='TERMINAL'
    )
    @patch(
        'archey.configuration.Configuration.get',
        side_effect=[
            {'not_detected': None},  # Needed key.
            {'use_unicode': False}
        ]
    )
    def test_without_unicode(self, _, __):
        """Test simple output, without Unicode support (default)"""
        output_mock = MagicMock()
        Terminal().output(output_mock)
        output = output_mock.append.call_args[0][1]
        self.assertTrue(output.startswith('TERMINAL '))
        self.assertEqual(output.count('#'), 7 * 2)

    @patch(
        'archey.entries.terminal.os.getenv',
        return_value='TERMINAL'
    )
    @patch(
        'archey.configuration.Configuration.get',
        side_effect=[
            {'not_detected': None},  # Needed key.
            {'use_unicode': True}
        ]
    )
    def test_with_unicode(self, _, __):
        """Test simple output, with Unicode support !"""
        output_mock = MagicMock()
        Terminal().output(output_mock)
        output = output_mock.append.call_args[0][1]
        self.assertTrue(output.startswith('TERMINAL '))
        self.assertEqual(output.count('\u2588'), 7 * 2)

    @patch(
        'archey.entries.terminal.os.getenv',
        return_value='Not detected'  # Set the "Not detected" string here, as we mock `os.getenv`.
    )
    @patch(
        'archey.configuration.Configuration.get',
        side_effect=[
            {'not_detected': None},  # Needed key.
            {'use_unicode': False}
        ]
    )
    def test_not_detected(self, _, __):
        """Test simple output, with Unicode support !"""
        output_mock = MagicMock()
        Terminal().output(output_mock)
        output = output_mock.append.call_args[0][1]
        self.assertTrue(output.startswith('Not detected '))
        self.assertEqual(output.count('#'), 7 * 2)


if __name__ == '__main__':
    unittest.main()
