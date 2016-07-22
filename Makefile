.PHONY: neat test clean all

all:

clean: neat

neat:
	rm $(shell find . -regex '.*\.pyc')
	rm $(shell find . -name parsetab.py )
	rm $(shell find . -name parser.out )

test:
	python ./test.py
