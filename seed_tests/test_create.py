from optparse import Values
import os
from seed.commands.create import CreateCommand
from seed_tests import BaseSeedTest


class TestCreateCommand(BaseSeedTest):

    def setUp(self):
        super(TestCreateCommand, self).setUp()
        self.cmd = CreateCommand()

    def test_dry_run(self):
        self.cmd.main(
            args=['--dry-run'],
            initial_options={}
        )
        self.assertEqual(os.listdir(self.pkg_dir), [])

    def test_no_args(self):
        self.cmd.main(
            args=[],
            initial_options={}
        )
        self.assertEqual(set(os.listdir(self.pkg_dir)), set([
            'bin',
            'CHANGES.txt',
            'LICENSE.txt',
            'MANIFEST.in',
            'README.rst',
            'setup.py',
            'testpkg',
            'docs',
            'VERSION',
        ]))
        self.assertEqual(os.listdir(os.path.join(self.pkg_dir, 'testpkg')), [
            '__init__.py',
        ])
