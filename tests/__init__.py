import os
import shutil
from tempfile import mkdtemp
import unittest
from seed.commands.create import CreateCommand


class BaseSeedTest(unittest.TestCase):

    def setUp(self):
        container_dir = mkdtemp(suffix=self._testMethodName)
        self.pkg_dir = os.path.join(container_dir, 'testpkg')
        self._old_cwd = os.getcwd()
        os.mkdir(self.pkg_dir)
        os.chdir(self.pkg_dir)
        os.environ['PWD'] = self.pkg_dir

    def tearDown(self):
        os.chdir(self._old_cwd)
        os.environ['PWD'] = self._old_cwd
        shutil.rmtree(self.pkg_dir)

    def create_package(self, *args):
        CreateCommand().main(
            args=list(args),
            initial_options={}
        )
        os.system('git init .')
        os.system('git add .')
        os.system('git commit -m "Initial commit"')
        os.system('python setup.py develop')

    def write_meta_data(self):
        setup_py_path = os.path.join(self.pkg_dir, 'setup.py')
        with open(setup_py_path) as f:
            setup_py = f.read()
        setup_py = setup_py.replace("author='',", "author='Test User',")
        setup_py = setup_py.replace("author_email='',", "author_email='test@user.com',")
        setup_py = setup_py.replace("url='',", "url='http://example.com',")
        with open(setup_py_path, mode='w') as f:
            f.write(setup_py)

    def initial_release(self):
        ok = os.system('seed release --initial --no-release')

    def assertVersion(self, version):
        init_py_path = os.path.join(self.pkg_dir, 'testpkg', '__init__.py')
        with open(init_py_path) as f:
            init_py = f.read()
        self.assertIn("\n__version__ = '{0}'".format(version), init_py)

        ok = os.system("git show-ref --tags | grep `git log --format='%H' -n 1` | grep 'v{0}'".format(version))
        self.assertEqual(ok, 0, "Latest version not tagged in git")
