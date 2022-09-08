.PHONY: main prime test

main:
	python3 sign/sign.py

test:
	PYTHONPATH=./sign pytest

prime:
	python3 sign/miller_rabin.py
