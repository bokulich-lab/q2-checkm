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
	pip install git+https://github.com/Ecogenomics/CheckM.git@8b42a8ca13dda3a967e2247efe6032f9df1bd434
	$(PYTHON) setup.py install

dev: all
	bash install-pplacer.sh
	pip install pre-commit git+https://github.com/Ecogenomics/CheckM.git@8b42a8ca13dda3a967e2247efe6032f9df1bd434
	pip install -e .
	pre-commit install

clean: distclean

distclean: ;
