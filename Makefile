# byobash-demo/Makefile


#
# Run from the Sh Command Line
#


# show these examples and exit

default:
	@echo ''
	@echo 'make  # show these examples and exit'
	@echo 'make help  # show this help message and exit'
	@echo 'make push  # restyle & test the source, then tell me to push it'
	@echo ''
	@echo 'open https://twitter.com/intent/tweet?text=.@PELaVarre'
	@echo ''

# @echo 'make --  # should mean 'make push', but won't, not until you redefine 'make'?


# show this help message and exit

help:
	: # usage: make [|help|style|push]
	: #
	: # work to add Code into GitHub PELaVarre ByoBash-Demo
	: #
	: # examples:
	: #
	: #   make  # show these examples and exit
	: #   make help  # show this help message and exit
	: #   make style  # restyle & test the source, but don't push it
	: #   make push  # restyle & test the source, then tell me to push it
	: #
	: #   open https://twitter.com/intent/tweet?text=@PELaVarre
	: #


# restyle & test the source, but don't push it

style: black flake8
	@


# restyle & test the source, then tell me to push it

push: black flake8
	git log --oneline --no-decorate -1
	git status --short --ignored
	git describe --always --dirty
	:
	: did you mean:  git push
	: press ⌃D to execute, or ⌃C to quit
	cat -
	git push


# cut personal flair out of the spaces, commas, and quotes of the source

black:
	. ~/bin/black.source && black $$PWD/../byobash-demo/


# block pushes of many kinds of nonsense:  missing format args, uninitted vars, etc

FLAKE8_OPTS=--max-line-length=999 --max-complexity 10 --ignore=E203,W503
# --max-line-length=999  # Black max line lengths over Flake8 max line lengths
# --ignore=E203  # Black '[ : ]' rules over Flake8 E203 whitespace before ':'
# --ignore=W503  # 2017 Pep 8 and Black over Flake8 W503 line break before binary op

flake8:
	. ~/bin/pips.source && flake8 ${FLAKE8_OPTS} $$PWD/../byobash-demo/


# posted into:  https://github.com/pelavarre/byobash-demo/blob/main/Makefile
# copied from:  git clone https://github.com/pelavarre/byobash-demo.git
