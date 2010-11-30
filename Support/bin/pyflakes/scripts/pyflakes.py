
"""
Implementation of the command-line I{pyflakes} tool.
"""

import _ast
import sys
import os
import optparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

checker = __import__('pyflakes.checker').checker

def check(codeString, filename, exclude=()):
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
        for warning in w.messages:
            if warning.level not in exclude:
                print warning
        return w.messages


def checkPath(filename, exclude=()):
    """
    Check the given path, printing out any warnings detected.

    @return: the number of warnings printed
    """
    if os.path.exists(filename):
        return check(file(filename, 'U').read() + '\n', filename, exclude)
    else:
        print >> sys.stderr, '%s: no such file' % (filename,)
        raise SystemExit

def main():
    def traverse_path(warnings, dirpath, dirnames, filenames):
        if dirpath.startswith('./'):
            dirpath = dirpath[2:]
        
        # Exclusions
        for p in options.exclude_files:
            if dirpath.startswith(p):
                return

        for filename in filenames:
            path = os.path.join(dirpath, filename)
            # Exclusions
            for p in options.exclude_files:
                if path.startswith(p):
                    return
            if filename.endswith('.py'):
                warnings += checkPath(path, options.exclude)
    
    parser = optparse.OptionParser(usage='usage: %prog [options] module')
    parser.add_option('-x', '--exclude', action='append', dest='exclude', help='exclude levels', default=[])
    parser.add_option('-X', '--exclude-files', action='append', dest='exclude_files', help='exclude files', default=[])

    (options, args) = parser.parse_args()
    warnings = []
    if args:
        for arg in args:
            if os.path.isdir(arg):
                if arg == '.':
                    arg = './'
                for dirpath, dirnames, filenames in os.walk(arg):
                    traverse_path(warnings, dirpath, dirnames, filenames)
            else:
                warnings += checkPath(arg, options.exclude)
    else:
        warnings += check(sys.stdin.read(), '<stdin>')

    raise SystemExit(sum(1 for w in warnings if w.level == 'E') > 0)

if __name__ == '__main__':
    main()