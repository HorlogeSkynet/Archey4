"""Test module for Archey's installed system packages detection module"""

import os
import unittest
from unittest.mock import DEFAULT as DEFAULT_SENTINEL, MagicMock, patch

from archey.constants import DEFAULT_CONFIG
from archey.test.entries import HelperMethods
from archey.entries.packages import Packages


class TestPackagesEntry(unittest.TestCase):
    """
    Here, we mock the `check_output` calls and check afterwards
      that the outputs are correct.
    Sorry for the code style, mocking this class is pretty boring.

    Note: Due to the presence of trailing spaces, we may have to manually
            "inject" the OS line separator in some mocked outputs.
    """
    @patch(
        'archey.entries.packages.check_output',
        return_value="""\
sqlite-libs-3.30.1-r1 x86_64 {{sqlite}} (Public-Domain) [installed]
musl-1.1.24-r2 x86_64 {{musl}} (MIT) [installed]
libbz2-1.0.8-r1 x86_64 {{bzip2}} (bzip2-1.0.6) [installed]
gdbm-1.13-r1 x86_64 {{gdbm}} (GPL) [installed]
ncurses-libs-6.1_p20200118-r3 x86_64 {{ncurses}} (MIT) [installed]
zlib-1.2.11-r3 x86_64 {{zlib}} (Zlib) [installed]
apk-tools-2.10.4-r3 x86_64 {{apk}-tools} (GPL2) [installed]
readline-8.0.1-r0 x86_64 {{readline}} (GPL-2.0-or-later) [installed]
""")
    def test_match_with_apk(self, check_output_mock):
        """Simple test for the APK packages manager"""
        check_output_mock.side_effect = self._check_output_side_effect('apk')

        self.assertEqual(Packages().value, 8)

# `apt` is disabled for now.
#    @patch(
#        'archey.entries.packages.check_output',
#        return_value="""\
#accountsservice/stable,now 0.6.45-2 amd64 [installed,automatic]
#acl/stable,now 2.2.53-4 amd64 [installed,automatic]
#adb/stable,now 1:8.1.0+r23-5 amd64 [installed]
#adduser/stable,now 3.118 all [installed]
#adwaita-icon-theme/stable,now 3.30.1-1 all [installed,automatic]
#albatross-gtk-theme/stable,now 1.7.4-1 all [installed,automatic]
#alsa-utils/stable,now 1.1.8-2 amd64 [installed,automatic]
#""")
#    def test_match_with_apt(self, check_output_mock):
#        """Simple test for the APT packages manager"""
#        check_output_mock.side_effect = self._check_output_side_effect('apt')

#        self.assertEqual(Packages().value, 7)

    @patch(
        'archey.entries.packages.check_output',
        return_value="""\
Installed Packages
GConf2.x86_64                  3.2.6-17.fc26           @@commandline
GeoIP.x86_64                   1.6.11-1.fc26           @@commandline
GeoIP-GeoLite-data.noarch      2017.07-1.fc26          @@commandline
GraphicsMagick.x86_64          1.3.26-3.fc26           @@commandline
""")
    def test_match_with_dnf(self, check_output_mock):
        """Simple test for the DNF packages manager"""
        check_output_mock.side_effect = self._check_output_side_effect('dnf')

        self.assertEqual(Packages().value, 4)

    @patch(
        'archey.entries.packages.check_output',
        return_value="""\
accountsservice         install
acl                     install
adb                     install
adduser                 install
adwaita-icon-theme      install
albatross-gtk-theme     deinstall
alien                   install
""")
    def test_match_with_dpkg(self, check_output_mock):
        """Simple test for the DPKG packages manager"""
        check_output_mock.side_effect = self._check_output_side_effect('dpkg')

        self.assertEqual(Packages().value, 6)

    @patch(
        'archey.entries.packages.check_output',
        return_value="""\

These are the packages that would be merged, in order:

Calculating dependencies  ... done!
[ebuild     U  ] sys-libs/glibc-2.25-r10 [2.25-r9]
[ebuild   R    ] sys-apps/busybox-1.28.0 {linesep}\
[ebuild  N     ] sys-libs/libcap-2.24-r2  \
USE="pam -static-libs" ABI_X86="(64) -32 (-x32)" {linesep}\
[ebuild     U  ] app-misc/pax-utils-1.2.2-r2 [1.1.7]
[ebuild   R    ] x11-misc/shared-mime-info-1.9 {linesep}\

""".format(linesep=os.linesep))
    def test_match_with_emerge(self, check_output_mock):
        """Simple test for the Emerge packages manager"""
        check_output_mock.side_effect = self._check_output_side_effect('emerge')

        self.assertEqual(Packages().value, 5)

    @patch(
        'archey.entries.packages.check_output',
        return_value="""\
acl 2.2.52-4
archey4 v4.3.3-1
archlinux-keyring 20180108-1
argon2 20171227-3
""")
    def test_match_with_pacman(self, check_output_mock):
        """Simple test for the Pacman packages manager"""
        check_output_mock.side_effect = self._check_output_side_effect('pacman')

        self.assertEqual(Packages().value, 4)

    @patch(
        'archey.entries.packages.check_output',
        return_value="""\
cdrecord-2.01-10.7.el5
bluez-libs-3.7-1.1
setarch-2.0-1.1
MySQL-client-3.23.57-1
""")
    def test_match_with_rpm(self, check_output_mock):
        """Simple test for the RPM packages manager"""
        check_output_mock.side_effect = self._check_output_side_effect('rpm')

        self.assertEqual(Packages().value, 4)

    @patch(
        'archey.entries.packages.check_output',
        return_value="""\
Loaded plugins: fastestmirror, langpacks
Installed Packages
GConf2.x86_64                   3.2.6-8.el7         @base/$releasever
GeoIP.x86_64                    1.5.0-11.el7        @base            {linesep}\
ModemManager.x86_64             1.6.0-2.el7         @base            {linesep}\
ModemManager-glib.x86_64        1.6.0-2.el7         @base            {linesep}\
""".format(linesep=os.linesep))
    def test_match_with_yum(self, check_output_mock):
        """Simple test for the Yum packages manager"""
        check_output_mock.side_effect = self._check_output_side_effect('yum')

        self.assertEqual(Packages().value, 4)

    @patch(
        'archey.entries.packages.check_output',
        return_value="""\
Loading repository data...
Reading installed packages...

S  | Name          | Summary                             | Type       {linesep}\
---+---------------+-------------------------------------+------------
i+ | 5201          | Recommended update for xdg-utils    | patch      {linesep}\
i  | GeoIP-data    | Free GeoLite country-data for GeoIP | package    {linesep}\
i  | make          | GNU make                            | package    {linesep}\
i  | GNOME Nibbles | Guide a worm around a maze          | application
i  | at            | A Job Manager                       | package    {linesep}\
""".format(linesep=os.linesep))
    def test_match_with_zypper(self, check_output_mock):
        """Simple test for the Zypper packages manager"""
        check_output_mock.side_effect = self._check_output_side_effect('zypper')

        self.assertEqual(Packages().value, 5)

    @patch('archey.entries.packages.check_output')
    @HelperMethods.patch_clean_configuration
    def test_no_packages_manager(self, check_output_mock):
        """No packages manager is available at the moment..."""
        check_output_mock.side_effect = self._check_output_side_effect()

        packages = Packages()

        output_mock = MagicMock()
        packages.output(output_mock)

        self.assertIsNone(packages.value)
        self.assertEqual(
            output_mock.append.call_args[0][1],
            DEFAULT_CONFIG['default_strings']['not_detected']
        )


    @staticmethod
    def _check_output_side_effect(pkg_manager_cmd=None):
        """Internal helper method to facilitate `check_output` mocking"""
        def _check_output(args, stderr, env, universal_newlines):  # pylint: disable=unused-argument
            """
            This closure is a drop-replacement for our `check_output` call.
            If the _called_ program is `pkg_manager_cmd`, patched `return_value` will be returned.
            If not, `FileNotFoundError` would be raised.
            """
            if args[0] == pkg_manager_cmd:
                return DEFAULT_SENTINEL

            raise FileNotFoundError

        return _check_output


if __name__ == '__main__':
    unittest.main()
