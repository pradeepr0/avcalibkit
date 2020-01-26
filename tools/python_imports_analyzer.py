#! /usr/bin/env python3

import ast
import fileinput
import sys


def get_modules_imported_by(filename):

    class ImportsAnalyzer(ast.NodeVisitor):
        def __init__(self):
            self.imports = []

        def visit_Import(self, node):
            for key, vals in ast.iter_fields(node):
                if key == 'names':
                    for v in vals:
                        self.imports.append(v.name)
            self.generic_visit(node)

        def visit_ImportFrom(self, node):
            self.imports.append(node.module)
            # for key, vals in ast.iter_fields(node):
            #     if key == 'names':
            #         for v in vals:
            self.generic_visit(node)

    with open(filename) as f:
        tree = ast.parse(f.read())

    analyzer = ImportsAnalyzer()
    analyzer.visit(tree)
    return analyzer.imports


def main():
    for filename in sys.argv[1:]:
        print(filename)
        try:
            print('\t' + ' '.join(get_modules_imported_by(filename)))
        except SyntaxError as e:
            print('\t# ERROR:', e)

if __name__ == "__main__":
    main()
