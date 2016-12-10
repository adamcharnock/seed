import os
import shutil
from tempfile import mkdtemp
import unittest
from seed.commands.create import CreateCommand


class BaseSeedTest(unittest.TestCase):

    def setUp(self):
        container_dir = mkdtemp(suffix=self._testMethodName)
        self.pkg_dir = os.path.join(container_dir, 'testpkg')
        self.seed_dir = os.getcwd()
        os.mkdir(self.pkg_dir)
        os.chdir(self.pkg_dir)
        os.environ['PWD'] = self.pkg_dir

    def tearDown(self):
        os.chdir(self.seed_dir)
        os.environ['PWD'] = self.seed_dir

        # It is useful to be able to skip cleanup when doing
        # coverage reporting as some source files are needed to
        # upload to coveralls.io
        do_cleanup = not os.path.exists(os.path.join(self.seed_dir, '.nocleanup'))
        if do_cleanup:
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
        version_path = os.path.join(self.pkg_dir, 'VERSION')
        with open(version_path) as f:
            version = f.read()
        self.assertTrue(version in version)

        ok = os.system("git show-ref --tags | grep `git log --format='%H' -n 1` | grep '{0}'".format(version))
        self.assertEqual(ok, 0, "Latest version not tagged in git")

    def run_with_coverage(self, command):
        with_coverage_cmd = \
            "coverage run -p --source=seed {seed_dir}/seed/run.py {command}".format(
                seed_dir=self.seed_dir,
                command=command,
            )
        status = os.system(with_coverage_cmd)
        os.system("cp {pkg_dir}/.coverage.* {seed_dir}".format(
            pkg_dir=self.pkg_dir,
            seed_dir=self.seed_dir,
        ))
        return status
