.PHONY: clean-pyc clean-build docs clean

help:
	@echo "setup-devcontainer - Make devcontainer ready for development"
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "dist - package"

setup-devcontainer:
	sudo mv -n /.pyenvsrc/** /.pyenv
	sudo chmod 777 /.pyenv

	pyenv install 3.9
	pyenv install 3.10
	pyenv install 3.11

	pyenv local 3.9 3.10 3.11

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8

test:
	tox -e py38,py39,py310,py311

coverage:
	coverage run --source tapioca setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/tapioca.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ tapioca
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
