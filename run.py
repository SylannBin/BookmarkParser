#!/usr/bin/env python3
import sys
import os

from parser import Bookmark


HELP = "Usage: {} <bookmark-file-path>".format(__file__)


def parse_argv(args):
    if len(args) < 2:
        print(HELP)
        sys.exit()
    return args[1]


def main(args):
    FILENAME = parse_argv(args)
    if (not os.path.isfile(FILENAME)):
        print("The provided file does not exist")
        sys.exit()

    with open(FILENAME, mode='rt', encoding='utf-8') as f:
        bookmarks = Bookmark(f.readlines())
        bookmarks.parse()
        bookmarks.show()
    # TODO: Add a method to show the result
    # TODO: Add a method to write it to a file
    # ???: Database?
    # ???: More sources?


if __name__ == '__main__':
    main(sys.argv)
