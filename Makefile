.PHONY: sign verify prime test

sign:
	python3 -m sign.sign

verify:
	python3 -m sign.verify

test:
	pytest -v

prime:
	python3 -m sign.miller_rabin
