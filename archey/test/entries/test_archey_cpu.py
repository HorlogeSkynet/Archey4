"""Test module for Archey's CPU detection module"""

import unittest
from unittest.mock import MagicMock, call, mock_open, patch

from archey.entries.cpu import CPU
from archey.test.entries import HelperMethods
from archey.constants import DEFAULT_CONFIG


class TestCPUEntry(unittest.TestCase):
    """
    Here, we mock the `open` call on `/proc/cpuinfo` with fake content.
    In some cases, `lscpu` output is being mocked too.
    """
    @patch(
        'archey.entries.cpu.open',
        mock_open(
            read_data="""\
processor\t: 0
vendor_id\t: CPU-VENDOR-NAME
cpu family\t: X
model\t\t: YY
model name\t: CPU-MODEL-NAME
"""),
        create=True
    )
    def test_model_name_match_cpuinfo(self):
        """Test `/proc/cpuinfo` parsing"""
        self.assertDictEqual(
            CPU().value,
            {'CPU-MODEL-NAME': 1}
        )

    @patch(
        'archey.entries.cpu.open',
        mock_open(
            read_data="""\
processor\t: 0
vendor_id\t: CPU-VENDOR-NAME
cpu family\t: X
model\t\t: YY
model name\t: CPU-MODEL-NAME

processor\t: 0
vendor_id\t: CPU-VENDOR-NAME
cpu family\t: X
model\t\t: YY
model name\t: ANOTHER-CPU-MODEL

processor\t: 0
vendor_id\t: CPU-VENDOR-NAME
cpu family\t: X
model\t\t: YY
model name\t: ANOTHER-CPU-MODEL
"""),
        create=True
    )
    def test_multiple_cpus_from_proc_cpuinfo(self):
        """Test `/proc/cpuinfo` parsing"""
        self.assertDictEqual(
            CPU().value,
            {
                'CPU-MODEL-NAME': 1,
                'ANOTHER-CPU-MODEL': 2
            }
        )

    @patch(
        'archey.entries.cpu.open',
        mock_open(
            read_data="""\
processor\t: 0
vendor_id\t: CPU-VENDOR-NAME
cpu family\t: X
model\t\t: YY
"""),
        create=True
    )
    @patch(
        'archey.entries.cpu.check_output',
        return_value="""\
Architecture:        x86_64
CPU op-mode(s):      32-bit, 64-bit
Byte Order:          Little Endian
CPU(s):              4
On-line CPU(s) list: 0-3
Thread(s) per core:  X
Core(s) per socket:  Y
Socket(s):           1
NUMA node(s):        1
Vendor ID:           CPU-VENDOR-NAME
CPU family:          Z
Model:               \xde\xad\xbe\xef
Model name:          CPU-MODEL-NAME-WITHOUT-PROC-CPUINFO
""")
    def test_model_name_match_lscpu(self, _):
        """
        Test model name parsing from `lscpu` output.

        See issue #29 (ARM architectures).
        `/proc/cpuinfo` will not contain `model name` info.
        `lscpu` output will be used instead.
        """
        self.assertDictEqual(
            CPU().value,
            {'CPU-MODEL-NAME-WITHOUT-PROC-CPUINFO': 4}
        )

    @patch(
        'archey.entries.cpu.open',
        mock_open(
            read_data="""\
processor\t: 0
vendor_id\t: CPU-VENDOR-NAME
cpu family\t: X
model\t\t: YY
model name\t: CPU  MODEL\t  NAME
"""),
        create=True
    )
    def test_spaces_squeezing(self):
        """Test name sanitizing, needed on some platforms"""
        self.assertDictEqual(
            CPU().value,
            {'CPU MODEL NAME': 1}
        )

    @patch(
        'archey.entries.cpu.open',
        side_effect=PermissionError(),
        create=True
    )
    @patch(
        'archey.entries.cpu.check_output',
        return_value="""\
Architecture:        x86_64
CPU op-mode(s):      32-bit, 64-bit
Byte Order:          Little Endian
CPU(s):              4
On-line CPU(s) list: 0-3
Thread(s) per core:  X
Core(s) per socket:  Y
Socket(s):           1
NUMA node(s):        1
Vendor ID:           CPU-VENDOR-NAME
CPU family:          Z
Model:               \xde\xad\xbe\xef
Model name:          CPU-MODEL-NAME-WITHOUT-PROC-CPUINFO
""")
    def test_proc_cpuinfo_unreadable(self, _, __):
        """Check Archey does not crash when `/proc/cpuinfo` is not readable"""
        self.assertDictEqual(
            CPU().value,
            {'CPU-MODEL-NAME-WITHOUT-PROC-CPUINFO': 4}
        )

    @HelperMethods.patch_clean_configuration
    def test_various_output_configuration(self):
        """Test (non-)detection when there is not any graphical candidate"""
        cpu_instance_mock = HelperMethods.entry_mock(CPU)
        output_mock = MagicMock()

        cpu_instance_mock.value = {
            'CPU-MODEL-NAME': 1,
            'ANOTHER-CPU-MODEL': 2
        }

        with self.subTest('Single-line combined output.'):
            CPU.output(cpu_instance_mock, output_mock)
            output_mock.append.assert_called_once_with(
                'CPU',
                'CPU-MODEL-NAME, 2 x ANOTHER-CPU-MODEL'
            )

        output_mock.reset_mock()

        with self.subTest('Single-line combined output (no count).'):
            cpu_instance_mock.options['show_count'] = False

            CPU.output(cpu_instance_mock, output_mock)
            output_mock.append.assert_called_once_with(
                'CPU',
                'CPU-MODEL-NAME, ANOTHER-CPU-MODEL'
            )

        output_mock.reset_mock()

        with self.subTest('Multi-lines output (with counts).'):
            cpu_instance_mock.options['show_count'] = True
            cpu_instance_mock.options['one_line'] = False

            CPU.output(cpu_instance_mock, output_mock)
            self.assertEqual(output_mock.append.call_count, 2)
            output_mock.append.assert_has_calls(
                [
                    call(
                        'CPU',
                        'CPU-MODEL-NAME'
                    ),
                    call(
                        'CPU',
                        '2 x ANOTHER-CPU-MODEL'
                    )
                ],
                any_order=True  # Since Python < 3.6 doesn't have definite `dict` ordering.
            )

        output_mock.reset_mock()

        with self.subTest('No CPU detected output.'):
            cpu_instance_mock.value = {}

            CPU.output(cpu_instance_mock, output_mock)
            output_mock.append.assert_called_once_with(
                'CPU',
                DEFAULT_CONFIG['default_strings']['not_detected']
            )


if __name__ == '__main__':
    unittest.main()
