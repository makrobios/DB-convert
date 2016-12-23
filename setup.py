from distutils.core import setup
import py2exe
import sys

sys.setrecursionlimit(3000)

setup(windows=['Import_Final_py3.py'])

