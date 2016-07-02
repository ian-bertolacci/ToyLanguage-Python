.PHONY: neat test

neat:
	rm $(shell find . -regex '.*\.pyc')

test:
	python ./test.py
