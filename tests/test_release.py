from optparse import Values
import os
from seed.commands.release import ReleaseCommand
from tests import BaseSeedTest


class TestReleaseCommand(BaseSeedTest):

    def setUp(self):
        super(TestReleaseCommand, self).setUp()

    def test_dry_run_initial(self):
        self.create_package()
        self.write_meta_data()
        ok = os.system('seed release --initial --dry-run')
        self.assertEqual(ok, 0)

    def test_dry_run(self):
        self.create_package()
        self.write_meta_data()
        self.initial_release()
        ok = os.system('seed release --dry-run')
        self.assertEqual(ok, 0)

    def test_initial(self):
        self.create_package()
        self.write_meta_data()
        ok = os.system('seed release --initial --no-release')
        self.assertEqual(ok, 0)
        self.assertVersion('0.1.0')

    def test_no_args(self):
        self.create_package()
        self.write_meta_data()
        self.initial_release()
        ok = os.system('seed release --no-release')
        self.assertEqual(ok, 0)
        # bug release by default
        self.assertVersion('0.1.1')

    def test_bug(self):
        self.create_package()
        self.write_meta_data()
        self.initial_release()
        ok = os.system('seed release --bug --no-release')
        self.assertEqual(ok, 0)
        self.assertVersion('0.1.1')

    def test_minor(self):
        self.create_package()
        self.write_meta_data()
        self.initial_release()
        ok = os.system('seed release --minor --no-release')
        self.assertEqual(ok, 0)
        self.assertVersion('0.2.0')

    def test_major(self):
        self.create_package()
        self.write_meta_data()
        self.initial_release()
        ok = os.system('seed release --major --no-release')
        self.assertEqual(ok, 0)
        self.assertVersion('1.0.0')

    def test_specific(self):
        self.create_package()
        self.write_meta_data()
        self.initial_release()
        ok = os.system('seed release --release=2.3.4 --no-release')
        self.assertEqual(ok, 0)
        self.assertVersion('2.3.4')
