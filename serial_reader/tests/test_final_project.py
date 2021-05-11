from unittest import TestCase

from serial_reader.sandbox import iam_alive


class BootstrapTest(TestCase):
    """ Simple test case """

    def test_sandbox(self):
        self.assertEqual(iam_alive(), "IAMALIVE")
