import ast
import logging
import os
import re
import subprocess

PRINT_REX = re.compile(r"^from __future__ import [^#]*print_function")


def uses_print_without_future(filepath):
    with open(filepath, "r") as f:
        raw = f.read()
        try:
            tree = ast.parse(raw)
        except Exception as e:
            # Not py2 - maybe py3?
            logging.warning("Skipping {} - {}".format(filepath, e))
            return True

    for line in raw.split("\n"):
        if PRINT_REX.match(line):
            return False

    for node in ast.walk(tree):
        if isinstance(node, ast.Print):
            return True


def find_print_files():
    for dirpath, _, files in os.walk("."):
        for filename in files:
            if "venv" in dirpath:
                continue
            if not filename.endswith(".py"):
                continue
            if filename.endswith("_py2.py"):
                continue

            filepath = os.path.join(dirpath, filename)

            if uses_print_without_future(filepath):
                yield filepath


def add_future_import(filepath):

    with open(filepath, "r") as f:
        lines = f.readlines()

    import_block = []
    for k, line in enumerate(lines):
        if line.startswith("from ") or line.startswith("import "):
            import_block.append(k)

        if import_block and not line.startswith("from __future__"):
            import_block.append(k)
            break

    # Case 1: no imports
    if not import_block:
        lines = ["from __future__ import print_function\n"] + lines

    # Case 2: no __future__ imports
    elif import_block[0] == import_block[1]:
        k = import_block[0]
        lines = (
            lines[:k] + ["from __future__ import print_function\n"] + lines[k:]
        )

    # Case 3: __future__ imports
    else:
        already_imported = False
        for line in lines[import_block[0]:import_block[1]]:
            if PRINT_REX.match(line):
                already_imported = True
                break

        if not already_imported:
            k = import_block[0]
            lines = lines[:k] + ["from __future__ import print_function\n"] + lines[k:]

    with open(filepath, "w") as f:
        f.writelines(lines)


def smush_print_statements():
    for filepath in find_print_files():
        subprocess.check_call(
            " ".join(["2to3", "-f", "print", "-w", filepath]),
            shell=True,
        )
        add_future_import(filepath)


if __name__ == "__main__":
    smush_print_statements()
