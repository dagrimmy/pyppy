all: pylint-src black pytest mypy

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

apidoc:
	cd docs && make clean && sphinx-apidoc --force -e -o ./source ../pyppy