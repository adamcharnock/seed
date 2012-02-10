from distutils.core import setup
from pythonpackager import __version__

setup(
    name='python-packager',
    version=__version__,
    author='Adam Charnock',
    author_email='adam@playnice.ly',
    packages=['pythonpackager', 'pythonpackager.commands', 'pythonpackager.vcs'],
    scripts=[],
    url='',
    license='LICENSE.txt',
    description='',
    long_description=open('README.rst').read(),
    entry_points=dict(console_scripts=['pythonpackager=pythonpackager:main']),
    install_requires=[
        "path.py>=2.2.2",
    ],
)
