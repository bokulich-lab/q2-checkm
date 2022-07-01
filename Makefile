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
	pip install git+https://github.com/misialq/CheckM.git@29916b666ba8834d0191d631110ffbdf4494cac9
	$(PYTHON) setup.py install

dev: all
	bash install-pplacer.sh
	pip install pre-commit pip install git+https://github.com/misialq/CheckM.git@29916b666ba8834d0191d631110ffbdf4494cac9
	pip install -e .
	pre-commit install

prep-dev-container: all
	conda install mamba -qy -n base -c conda-forge
	mamba install -p /opt/conda/envs/qiime2-$(QIIME_VERSION) -qy -c conda-forge -c bioconda -c defaults --file requirements.txt flake8 coverage wget pytest-xdist autopep8
	/opt/conda/envs/qiime2-$(QIIME_VERSION)/bin/pip install -q https://github.com/qiime2/q2lint/archive/master.zip
	/opt/conda/envs/qiime2-$(QIIME_VERSION)/bin/pip install -e .

clean: distclean

distclean: ;
