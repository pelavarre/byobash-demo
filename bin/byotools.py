#!/usr/bin/env python3

# deffed in many packages  # missing from:  https://pypi.org

"""
usage: import byotools as byo  # define Func's

give you the Python you need to welcome you competently into Sh work
"""


import __main__
import argparse
import difflib
import io
import os
import pdb
import re
import shlex
import string
import subprocess
import sys
import textwrap

_ = pdb


#
# Add some Def's to Import ArgParse
#


def argparse_compile_argdoc(help_option=None, help_opt=None):
    """Form an ArgumentParser from Main Doc, without Positional Args or Options"""

    #

    doc = __main__.__doc__
    grafs = str_splitgrafs(doc)

    usage = " ".join(_.strip() for _ in grafs[0])
    prog = usage.split()[1]  # second word of leading line of first paragraph

    description = " ".join(_.strip() for _ in grafs[1])

    add_help = False
    if (help_option, help_opt) == ("--help", "-h"):
        add_help = True

    epilog_grafs = grafs[2:]
    if epilog_grafs:
        if epilog_grafs[0][0].startswith("positional arguments"):
            epilog_grafs.pop(0)
        if epilog_grafs[0][0].startswith("options"):
            epilog_grafs.pop(0)

    epilog = str_joingrafs(epilog_grafs) if epilog_grafs else None

    #

    parser = argparse.ArgumentParser(
        prog=prog,
        description=description,
        add_help=add_help,  # False to leave "-h". "--h", "--he", ... "--help" undefined
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=epilog,
    )

    assert not hasattr(parser, "help_option")
    assert not hasattr(parser, "help_opt")

    parser.help_option = help_option
    parser.help_opt = help_opt

    #

    if not add_help:
        if help_option and help_opt:
            parser.add_argument(
                help_option,
                help_opt,
                action="count",
                help="show this help message and exit",
            )
        elif help_option:
            parser.add_argument(
                help_option, action="count", help="show this help message and exit"
            )
        elif help_opt:
            parser.add_argument(
                help_opt, action="count", help="show this help message and exit"
            )

    parser.add_argument(
        "--ext",
        metavar="EXT",
        nargs=argparse.OPTIONAL,  # aka 'nargs="?"'
        default=False,
        help="print the chosen source code, in the syntax of EXT, don't run it",
    )

    return parser


def argparse_format_testdoc():
    """Pick the Last Graf out of the ArgDoc, but drop its heading"""

    doc = __main__.__doc__
    grafs = str_splitgrafs(doc)

    last_graf = grafs[-1]
    ripped_graf = str_ripgraf(last_graf)
    testdoc = str_joingrafs([ripped_graf])

    return testdoc


# deffed in many files  # missing from docs.python.org
def argparse_match_argdoc_else(parser):
    """Exit nonzero, unless Doc equals Parser Format_Help"""

    main_doc = __main__.__doc__.strip()

    # Fetch the Parser Doc from a fitting virtual Terminal
    # Fetch from a Black Terminal of 89 columns, not current Terminal width
    # Fetch from later Python of "options:", not earlier Python of "optional arguments:"

    with_columns = os.getenv("COLUMNS")
    os.environ["COLUMNS"] = str(89)
    try:

        parser_doc = parser.format_help()

    finally:
        if with_columns is None:
            os.environ.pop("COLUMNS")
        else:
            os.environ["COLUMNS"] = with_columns

    parser_doc = parser_doc.replace("optional arguments:", "options:")

    # Fetch the Main Doc

    file_filename = os.path.split(__file__)[-1]

    got = main_doc
    got_filename = "{} --help".format(file_filename)
    want = parser_doc
    want_filename = "argparse.ArgumentParser(..."

    # Print the Diff to Parser Doc from Main Doc and exit, if Diff exists

    difflines = list(
        difflib.unified_diff(
            a=got.splitlines(),
            b=want.splitlines(),
            fromfile=got_filename,
            tofile=want_filename,
        )
    )

    if difflines:
        print("\n".join(difflines))

        sys.exit(1)  # trusts the caller to log SystemExit exceptions well


# deffed in many files  # missing from docs.python.org
def argparse_parse_args_else(parser, argv, shline):
    """Run the ArgV and exit, else return the Parsed Args to run"""

    parms = argv[1:]
    (options, seps, words) = shlex_parms_partition(parms)

    # Print the last Graf of the Epilog in a blank Frame without Heading, and exit zero

    if not parms:
        testdoc = argparse_format_testdoc()

        print()
        print(testdoc)
        print()

        sys.exit(0)

    # Print the Help Lines and exit zero

    help_opted = parser.help_opt in options

    help_optioned = None
    if parser.help_option:
        help_optioned = any(parser.help_option.startswith(_) for _ in options)

    if help_opted or help_optioned:
        parser.print_help()

        sys.exit(0)

    #

    stderr = io.StringIO()

    with_stderr = sys.stderr
    sys.stderr = stderr
    try:

        args = parser.parse_args(argv[1:])
        if args.ext in (False, None, ".py", "py"):

            return args

    except SystemExit as exc:
        if not exc.code:  # SystemExit '.code' = process exit status returncode

            raise

    finally:
        sys.stderr = with_stderr

    # Supply our defaults

    argv_0 = argv[0]

    alt_argv = list(argv)
    alt_argv[0] = os.path.basename(os.path.splitext(argv_0)[0])
    if parms != ["--"]:
        alt_shline = shlex_djoin(alt_argv)
        sys_stderr_print("+ {}".format(alt_shline))
    else:
        sh_shline = "bash -c {!r}".format(shline)
        alt_argv = shlex.split(sh_shline)
        sys_stderr_print("+ {}".format(shline))

    # Fall back to 'shverb' in place of 'shverb.py'

    run = subprocess.run(alt_argv)

    sys.exit(run.returncode)


#
# Add some Def's to Import Ast
#


def ast_func_exec_else(func, ext):
    """Exec the Py Source Chars of the Func if Ext is False, else print them"""

    py = ast_func_to_py(func)

    #

    lines = py.splitlines()

    lines.insert(0, "")
    lines.insert(0, "#!/usr/bin/env python3")

    import_index = -1
    for (index, line) in enumerate(lines):
        if line.startswith("import "):
            import_index = index

    lines.insert(import_index + 1, "")

    #

    alt_py = "\n".join(lines)
    if (ext is None) or ext:
        print(alt_py)
    else:
        exec(alt_py)


def ast_func_to_py(func):
    """Convert to Py Source Chars from Func"""

    funcname = func.__name__
    def_tag = "def {}".format(funcname)

    modulename = func.__module__
    module = sys.modules[modulename]
    pyfile = module.__file__

    with open(pyfile) as reading:
        pyfile_chars = reading.read()

    py = None

    grafs = str_splitgrafs(pyfile_chars)
    for graf in reversed(grafs):
        if graf[0].startswith(def_tag):
            ripgraf = str_ripgraf(graf)
            py = str_joingrafs([ripgraf])

            break

    assert py, (funcname, pyfile)

    return py


#
# Add some Def's to Class List
#


# deffed in many files  # missing from docs.python.org
def list_strip(items):  # todo: coin a name for "\n".join(items).strip().splitlines()
    """Drop the leading and trailing Falsey Items"""

    # Find the leftmost Truthy Item, else 0

    index = 0
    while items[index:]:
        if items[index]:

            break

        index += 1

    # Find the rightmost Truthy Item, else -1

    rindex = -1
    while items[:rindex]:
        if items[rindex]:

            break

        rindex -= 1

    # Drop the leading and trailing Falsey Items,
    # by way of picking all the Items from leftmost through rightmost Truthy Item

    lstrip = items[index:]
    strip = lstrip[: (rindex + 1)] if (rindex < -1) else lstrip

    return strip


#
# Add some Def's to Import ShLex and Import String
#


SH_PLAIN = (  # all printable Ascii except not " !#$&()*;<>?[]^`{|}~" and " and ' and \
    "%+,-./"
    + string.digits
    + ":=@"
    + string.ascii_uppercase
    + "_"
    + string.ascii_lowercase
)


SH_QUOTABLE = SH_PLAIN + " " + "!#&()*;<>?[]^{|}~"
# all printable Ascii except not $ Dollar and ` Backtick, and not " and ' and \


# deffed in many files  # missing from docs.python.org
def shlex_djoin(parms):  # see also 'shlex.join' since Oct/2019 Python 3.8
    """Quote, but quote compactly despite '"' and '~', when that's still easy"""

    shline = " ".join(shlex_dquote(_) for _ in parms)

    return shline  # such as:  echo "let's" speak freely, even casually


# deffed in many files  # missing from docs.python.org
def shlex_dquote(parm):
    """Quote 1 Parm, but quote compactly despite '"' and '~', when that's still easy"""

    # Follow the Library, when they agree no quote marks required

    quoted = shlex_quote(parm)
    if quoted[:1] not in ("'", '"'):

        return quoted

    # Accept the ^ Caret when the Parm does start with the ^ Caret
    # Accept the ~ Tilde when the Parm does Not start with the ~ Tilde

    unplain_set = set(parm) - set(SH_PLAIN)

    if parm.startswith("^"):  # forwards the ^ Caret as start of Parm
        unplain_set = set(parm[1:]) - set(SH_PLAIN)

    if not parm.startswith("~"):  # forwards the ~ Tilde if after start of Parm
        unplain_set = unplain_set - set("~")

    if (parm.count("{") == 1) and (parm.count("}") == 1):  # forwards {} wout ,
        head = parm.partition("{")[0]
        tail = parm.rpartition("}")[-1]
        if "," not in (head + tail):  # todo: overly restrictive for:  echo ,}{,
            unplain_set = unplain_set - set("{}")

    unplain_ascii_set = "".join(_ for _ in unplain_set if ord(_) < 0x80)
    if not unplain_ascii_set:

        return parm

    # Try the " DoubleQuote to shrink it

    unquotable_set = set(parm) - set(SH_QUOTABLE) - set("'")
    unquotable_ascii_set = "".join(_ for _ in unquotable_set if ord(_) < 0x80)
    if not unquotable_ascii_set:
        doublequoted = '"' + parm + '"'
        if len(doublequoted) < len(quoted):
            late = shlex_quote_later(doublequoted)

            return late

            # such as:  print(shlex_dquote("i just can't"))  # "i just can't"

    # Give up and mostly settle for the Library's work

    late = shlex_quote_later(quoted)

    return late

    # todo: figure out when the ^ Caret is plain enough to need no quoting
    # todo: figure out when the {} Braces are plain enough to need no quoting
    # todo: figure out when the ! Bang is plain enough to need no quoting

    # todo: figure out when the * ? [ ] are plain enough to need no quoting
    # so long as we're calling Bash not Zsh
    # and the Dirs don't change out beneath us


# deffed in many files  # missing from docs.python.org
def shlex_quote_later(early):
    """Slide the ' Quote or " DoubleQuote past the Mark of an Option"""

    matched = re.match(r"^'-[A-Z_a-z]+", string=early)
    matched = matched or re.match(r'^"-[A-Z_a-z]+', string=early)
    if not matched:

        return early

    stop = matched.end()
    late = early[1:stop] + early[0] + early[stop:]  # such as -e'$' from '-e$'

    return late


# deffed in many files  # missing from docs.python.org
def shlex_quote(parm):  # missing from Python till Oct/2019 Python 3.8
    """Mark up 1 Parm with Quote Marks and Backslants, so Sh agrees it is 1 Word"""

    # Trust the library, if available

    if hasattr(shlex, "quote"):
        quoted = shlex.quote(parm)

        return quoted

        # see also:  git rev-parse --sq-quote "i just can't"  # 'i just can'\''t'

    # Emulate the library roughly, because often good enough

    unplain_set = set(parm) - set(SH_PLAIN)
    if not unplain_set:

        return parm

    quoted = repr(parm)  # as if the Py rules agree with Sh rules

    return quoted  # such as:  print(shlex_quote("<=>"))  # the 5 chars '<=>'

    # test results with:  python3 -c 'import sys; print(sys.argv)' ...


def shlex_parms_partition(parms, mark=None):
    """Split Options from Positional Args, in the classic way of ArgParse and Sh"""

    options = list()
    seps = list()
    words = list()

    for (index, parm) in enumerate(parms):

        # Pick out the First Sep
        # and take the remaining Parms as Positional Args, not as Options

        if parm == "--":
            seps.append(parm)

        # Pick out each Option, before the First Sep

        elif not seps:
            if (parm != "-") and parm.startswith("-") and not parm.startswith("---"):
                options.append(parm)

            # Pick out each Arg before the First Sep

            elif mark is not None:
                marked = mark + parm
                options.append(marked)
            else:
                words.append(parm)

        # Pick out each Arg after the First Sep

        else:
            words.append(parm)

    return (options, seps, words)


#
# Add some Def's to Class Str and Class Bytes, not found in 'import textwrap'
#


# deffed in many files  # missing from docs.python.org
def str_ldent(chars):  # kin to 'str.lstrip'
    """Pick out the Spaces etc, at left of some Chars"""

    lstrip = chars.lstrip()
    length = len(chars) - len(lstrip)
    dent = chars[:length] if lstrip else ""

    return dent


# deffed in many files  # missing from docs.python.org
def str_joingrafs(grafs):
    """Form a Doc of Grafs separated by Empty Lines, from a List of Lists of Lines"""

    chars = ""
    for graf in grafs:
        if chars:
            chars += "\n\n"
        chars += "\n".join(graf)

    return chars


# good enough for now, but not yet obviously complete and correct
def str_ripgraf(graf):
    """Pick the lines below the head line of a paragraph, and dedent them"""

    grafdoc = "\n".join(graf[1:])
    dedent = textwrap.dedent(grafdoc)
    strip = dedent.strip()
    graf = strip.splitlines()

    return graf


# deffed in many files  # missing from docs.python.org
def str_splitgrafs(doc):  # todo: keepends=True
    """Form a List of Lists of Lines, from a Doc of Grafs separated by Empty Lines"""

    grafs = list()

    lines = doc.splitlines()

    graf = list()
    for line in lines:

        # Add an Empty Line

        if not line:
            if graf:

                graf.append(line)

        # Add a More Dented Line

        elif graf and (len(str_ldent(line)) > len(str_ldent(graf[0]))):

            graf.append(line)

        # Else strip and close this Graf

        else:
            strip = list_strip(graf)
            if strip:

                grafs.append(strip)

            # And then open the next Graf with this Line

            graf = list()
            graf.append(line)

    # Strip and close the last Graf too

    strip = list_strip(graf)
    if strip:

        grafs.append(strip)

    return grafs


#
# Add some Def's to Import Sys
#


# deffed in many files  # missing from docs.python.org
def sys_stderr_print(*args, **kwargs):
    """Work like Print, but write Stderr in place of Stdout"""

    kwargs_ = dict(kwargs)
    if "file" not in kwargs_.keys():
        kwargs_["file"] = sys.stderr

    sys.stdout.flush()
    print(*args, **kwargs)
    sys.stderr.flush()


# posted into:  https://github.com/pelavarre/byobash-demo/blob/main/bin/byotools.py
# copied from:  git clone https://github.com/pelavarre/byobash-demo.git
