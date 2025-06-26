.PHONY: all lint test test-cov test-docker install dev clean distclean

PYTHON ?= python

all: ;

lint:
	q2lint
	flake8

test: all
	py.test

test-cov: all
	python -m pytest --cov=q2_checkm -n 4 && coverage xml -o coverage.xml

test-docker: all
	qiime info
	qiime checkm --help

install: all
	bash install-pplacer.sh
	$(PYTHON) -m pip install checkm-genome
	$(PYTHON) -m pip install -v .

dev: all
	bash install-pplacer.sh
	$(PYTHON) -m pip install pre-commit checkm-genome
	$(PYTHON) -m pip install -e .
	pre-commit install

clean: distclean

distclean: ;
