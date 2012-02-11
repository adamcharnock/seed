from distutils.core import setup
from seed import __version__

setup(
    name='seed',
    version=__version__,
    author='Adam Charnock',
    author_email='adam@playnice.ly',
    packages=['seed', 'seed.commands', 'seed.vcs'],
    scripts=[],
    url='https://github.com/adamcharnock/seed',
    license='LICENSE.txt',
    description='A utility for easily creating and releasing Python packages',
    long_description=open('README.rst').read(),
    entry_points=dict(console_scripts=['seed=seed:main']),
    install_requires=[
        "path.py>=2.2.2",
    ],
)
