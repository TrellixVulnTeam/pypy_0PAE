from __future__ import print_function

# __________  Entry point  __________

def entry_point(argv):
    if len(argv) > 1:
        name = argv[1]
    else:
        name = "py3"

    value = next(iter(range(3)))

    print("Hello,", name + "!", "Value is:", value)

    return 0

# _____ Define and setup target ___

def target(*args):
    return entry_point
