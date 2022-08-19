.PHONY: all lint test test-cov install dev prep-dev-container clean distclean

PYTHON ?= python

all: ;

lint:
	q2lint
	flake8

test: all
	py.test

test-cov: all
	coverage run -m pytest
	coverage xml

install: all
	bash install-pplacer.sh
	pip install git+https://github.com/Ecogenomics/CheckM.git@8b42a8ca13dda3a967e2247efe6032f9df1bd434
	$(PYTHON) setup.py install

dev: all
	bash install-pplacer.sh
	pip install pre-commit git+https://github.com/Ecogenomics/CheckM.git@8b42a8ca13dda3a967e2247efe6032f9df1bd434
	pip install -e .
	pre-commit install

prep-dev-container: all
	conda install mamba -qy -n base -c conda-forge
	mamba install -p /opt/conda/envs/qiime2-$(QIIME_VERSION) -qy -c conda-forge -c bioconda -c defaults --file requirements.txt flake8 coverage wget pytest-xdist autopep8
	/opt/conda/envs/qiime2-$(QIIME_VERSION)/bin/pip install -q https://github.com/qiime2/q2lint/archive/master.zip
	/opt/conda/envs/qiime2-$(QIIME_VERSION)/bin/pip install -e .

clean: distclean

distclean: ;
