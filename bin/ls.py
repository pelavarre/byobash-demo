#!/usr/bin/env python3

"""
usage: ls.py [--help] [--ext [EXT]] [-1]

show the files and dirs inside a dir

options:
  --help       show this help message and exit
  --ext [EXT]  print the chosen source code, in the syntax of EXT, don't run it
  -1           show 1 file or dir per line

examples:

  bin/ls.py  # show these examples and exit
  bin/ls.py --h  # show this help message and exit
  bin/ls.py --  # 'ls -1Fdrt *'

  bin/ls.py -1  # show one file or dir per line
  bin/ls.py --ext=.py -1  # show the python code for this, don't run it
  bin/ls.py --e -1  # same deal as 'ls.py --ext=.py -1', just more abbreviated

  bin/ls.py -C  # fallback to call on 'ls' to run undefined options
"""


import sys


import byotools as byo


def main(argv):
    "Run from the Sh Command Line" ""

    parser = byo.argparse_compile_argdoc("--help", help_opt=None)  # don't define '-h'
    parser.add_argument("-1", action="count", help="show 1 file or dir per line")
    byo.argparse_match_argdoc_else(parser)

    args = byo.argparse_parse_args_else(parser, argv=argv, shline="ls -1Fdrt *")

    byo.ast_func_exec_else(ls_1, ext=args.ext)


def ls_1():

    import os

    names = os.listdir()
    names = list(_ for _ in names if not _.startswith("."))

    for name in sorted(names):
        print(name)


#
# Run from the Sh Command Line
#


if __name__ == "__main__":

    main(sys.argv)


# posted into:  https://github.com/pelavarre/byobash-demo/blob/main/bin/ls.py
# copied from:  git clone https://github.com/pelavarre/byobash-demo.git
