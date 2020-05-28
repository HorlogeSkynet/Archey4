"""Test module for `archey.distributions`"""

import unittest
from unittest.mock import patch

from archey.distributions import Distributions


class TestDistributionsUtil(unittest.TestCase):
    """
    Test cases for the `Distributions` (enumeration / utility) class.
    """
    def test_constant_values(self):
        """Test enumeration member instantiation from value"""
        self.assertEqual(Distributions('debian'), Distributions.DEBIAN)
        self.assertRaises(ValueError, Distributions, 'unknown')

    @patch(
        'archey.distributions.sys.platform',
        'win32'
    )
    def test_detection_windows(self):
        """Test output for Windows"""
        self.assertEqual(
            Distributions.run_detection(),
            Distributions.WINDOWS
        )

    @patch(
        'archey.distributions.sys.platform',
        'linux'
    )
    @patch(
        'archey.distributions.check_output',
        return_value=b'X.Y.Z-R-Microsoft\n'
    )
    def test_detection_windows_subsystem(self, _):
        """Test output for Windows Subsystem Linux"""
        self.assertEqual(
            Distributions.run_detection(),
            Distributions.WINDOWS
        )

    @patch(
        'archey.distributions.sys.platform',
        'linux'
    )
    @patch(
        'archey.distributions.check_output',
        return_value=b'X.Y.Z-R-ARCH\n'
    )
    @patch(
        'archey.distributions.distro.id',
        return_value='debian'
    )
    def test_detection_known_distro_id(self, _, __):
        """Test known distribution output"""
        self.assertEqual(
            Distributions.run_detection(),
            Distributions.DEBIAN
        )

    @patch(
        'archey.distributions.sys.platform',
        'linux'
    )
    @patch(
        'archey.distributions.check_output',
        return_value=b'X.Y.Z-R-ARCH\n'
    )
    @patch(
        'archey.distributions.distro.id',
        return_value='an-unknown-distro-id'
    )
    @patch(
        'archey.distributions.distro.like',
        return_value=''  # No `ID_LIKE` specified.
    )
    def test_detection_unknown_distro_id(self, _, __, ___):
        """Test unknown distribution output"""
        self.assertEqual(
            Distributions.run_detection(),
            Distributions.LINUX
        )

    @patch(
        'archey.distributions.sys.platform',
        'linux'
    )
    @patch(
        'archey.distributions.check_output',
        return_value=b'X.Y.Z-R-ARCH\n'
    )
    @patch(
        'archey.distributions.distro.id',
        return_value=''  # Unknown distribution.
    )
    @patch(
        'archey.distributions.distro.like',
        return_value='ubuntu'  # Oh, it's actually an Ubuntu-based one !
    )
    def test_detection_known_distro_like(self, _, __, ___):
        """Test distribution matching from the `os-release`'s `ID_LIKE` option"""
        self.assertEqual(
            Distributions.run_detection(),
            Distributions.UBUNTU
        )

    @patch(
        'archey.distributions.sys.platform',
        'linux'
    )
    @patch(
        'archey.distributions.check_output',
        return_value=b'X.Y.Z-R-ARCH\n'
    )
    @patch(
        'archey.distributions.distro.id',
        return_value=''  # Unknown distribution.
    )
    @patch(
        'archey.distributions.distro.like',
        return_value='an-unknown-distro-id arch'  # Hmmm, an unknown Arch-based...
    )
    def test_detection_distro_like_second(self, _, __, ___):
        """Test distribution matching from the `os-release`'s `ID_LIKE` option (second candidate)"""
        self.assertEqual(
            Distributions.run_detection(),
            Distributions.ARCH_LINUX
        )

    @patch(
        'archey.distributions.sys.platform',
        'linux'
    )
    @patch(
        'archey.distributions.check_output',
        return_value=b'X.Y.Z-R-ARCH\n'
    )
    @patch(
        'archey.distributions.distro.id',
        return_value=''  # Unknown distribution.
    )
    @patch(
        'archey.distributions.distro.like',
        return_value=''  # No `ID_LIKE` either...
    )
    def test_detection_both_distro_calls_fail(self, _, __, ___):
        """Test distribution fall-back when `distro` soft-fail two times"""
        self.assertEqual(
            Distributions.run_detection(),
            Distributions.LINUX
        )
