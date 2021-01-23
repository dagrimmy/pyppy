all: pylint-src black pytest

pylint-src:
	pylint pyppy/

pylint-test:
	pylint test/

black:
	black pyppy/

pytest:
	pytest test/

mypy:
	mypy pyppy/