.PHONY: neat test clean all

all:

clean: neat

neat:
	- rm $(shell find . -regex '.*\.pyc')
	- rm $(shell find . -name parsetab.py ) $(shell find . -name parser.out )

test: clean
	python ./test.py
