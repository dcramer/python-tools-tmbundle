
"""
Implementation of the command-line I{pyflakes} tool.
"""

import _ast
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

checker = __import__('pyflakes.checker').checker

def check(codeString, filename):
    try:
        tree = compile(codeString, filename, 'exec', _ast.PyCF_ONLY_AST)
    except (SyntaxError, IndentationError):
        value = sys.exc_info()[1]
        try:
            (lineno, offset, line) = value[1][1:]
        except IndexError:
            print >> sys.stderr, 'could not compile %r' % (filename,)
            raise SystemExit
        if line.endswith("\n"):
            line = line[:-1]
        print >> sys.stderr, '%s:%d: could not compile' % (filename, lineno)
        print >> sys.stderr, line
        print >> sys.stderr, " " * (offset-2), "^"
        raise SystemExit
    else:
        w = checker.Checker(tree, filename)
        w.messages.sort(lambda a, b: cmp(a.lineno, b.lineno))
        return w.messages

def main():
    warnings = check(sys.stdin.read(), '')
    for warning in warnings:
        print warning

if __name__ == '__main__':
    main()