from optparse import Values
import os
from seed.commands.help import HelpCommand
from seed.exceptions import CommandError
from seed_tests import BaseSeedTest


class TestCreateCommand(BaseSeedTest):

    def setUp(self):
        super(TestCreateCommand, self).setUp()
        self.cmd = HelpCommand()

    def test_help(self):
        self.cmd.main(
            args=[],
            initial_options={}
        )

    def test_help_specific_command(self):
        self.cmd.main(
            args=['release'],
            initial_options={}
        )

    def test_help_command_missing(self):
        self.assertRaises(CommandError, self.cmd.main,
            args=['foo'],
            initial_options={}
        )
