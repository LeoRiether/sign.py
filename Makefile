.PHONY: main prime test

main:
	python3 -m sign.sign

test:
	pytest

prime:
	python3 -m sign.miller_rabin
