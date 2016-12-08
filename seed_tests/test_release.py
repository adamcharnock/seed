# coding=utf-8
import os
from seed_tests import BaseSeedTest


class TestReleaseCommand(BaseSeedTest):

    def setUp(self):
        super(TestReleaseCommand, self).setUp()

    def test_dry_run_initial(self):
        self.create_package()
        self.write_meta_data()
        ok = self.run_with_coverage('release --initial --dry-run')
        self.assertEqual(ok, 0)

    def test_dry_run(self):
        self.create_package()
        self.write_meta_data()
        self.initial_release()
        ok = self.run_with_coverage('release --dry-run')
        self.assertEqual(ok, 0)

    def test_initial(self):
        self.create_package()
        self.write_meta_data()
        ok = self.run_with_coverage('release --initial --no-release')
        self.assertEqual(ok, 0)
        self.assertVersion('0.1.0')

    def test_no_args(self):
        self.create_package()
        self.write_meta_data()
        self.initial_release()
        ok = self.run_with_coverage('release --no-release')
        self.assertEqual(ok, 0)
        # bug release by default
        self.assertVersion('0.1.1')

    def test_bug(self):
        self.create_package()
        self.write_meta_data()
        self.initial_release()
        ok = self.run_with_coverage('release --bug --no-release')
        self.assertEqual(ok, 0)
        self.assertVersion('0.1.1')

    def test_minor(self):
        self.create_package()
        self.write_meta_data()
        self.initial_release()
        ok = self.run_with_coverage('release --minor --no-release')
        self.assertEqual(ok, 0)
        self.assertVersion('0.2.0')

    def test_major(self):
        self.create_package()
        self.write_meta_data()
        self.initial_release()
        ok = self.run_with_coverage('release --major --no-release')
        self.assertEqual(ok, 0)
        self.assertVersion('1.0.0')

    def test_specific(self):
        self.create_package()
        self.write_meta_data()
        self.initial_release()
        ok = self.run_with_coverage('release --release=2.3.4 --no-release')
        self.assertEqual(ok, 0)
        self.assertVersion('2.3.4')

    def test_unicode(self):
        self.create_package()
        os.system('git commit -m "Initial cømmit"')
        self.write_meta_data()
        self.initial_release()
        ok = self.run_with_coverage('release --no-release')
        self.assertEqual(ok, 0)
        # bug release by default
        self.assertVersion('0.1.1')
