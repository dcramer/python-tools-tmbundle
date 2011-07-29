
"""
Implementation of the command-line I{pyflakes} tool.
"""
import os.path
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pyflakes'))

from pyflakes.scripts.pyflakes import check

def main():
    content = open(sys.argv[-1], 'r').read()

    warnings = check(content, '')
    for warning in warnings:
        print warning

if __name__ == '__main__':
    main()