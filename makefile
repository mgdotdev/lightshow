.PHONY :test

test:
	python -m pip install -e .
	python -m pytest