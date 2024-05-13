# q2-checkm
![CI](https://github.com/bokulich-lab/q2-checkm/actions/workflows/ci-dev.yml/badge.svg)
[![codecov](https://codecov.io/gh/bokulich-lab/q2-checkm/branch/main/graph/badge.svg?token=RSZD1TD9HG)](https://codecov.io/gh/bokulich-lab/q2-checkm)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

QIIME 2 plugin for assessing the quality of (meta)genomes using CheckM.

## Installation

### Conda environment
You can install q2-checkm in an existing QIIME 2 environment or create a new environment by following the instructions for the 
[tiny distribution](https://docs.qiime2.org/2024.2/install/native/#install-qiime-2-within-a-conda-environment).

### Install pplacer
`pplacer`  is only available through conda for Linux - you can use our script to fetch the binary directly:
```shell
curl -s https://raw.githubusercontent.com/bokulich-lab/q2-checkm/main/install-pplacer.sh | bash
```

### Install remaining dependencies
```shell
mamba install -c bioconda -c conda-forge -c qiime2 -c defaults \
  dendropy "altair<5.0.0" hmmer prodigal pysam matplotlib numpy q2templates
```
### Install checkm and q2-checkm
```shell
pip install checkm-genome git+https://github.com/bokulich-lab/q2-checkm.git
```

### Refresh QIIME 2 cache
```shell
qiime dev refresh-cache
```

## Notes on CheckM version
CheckM version currently used by q2-checkm is pinned to a specific commit:
https://github.com/Ecogenomics/CheckM.git@8b42a8ca13dda3a967e2247efe6032f9df1bd434.
We are not using the corresponding version available through conda, as it has _pplacer_
as a pinned dependency (and this dependency cannot be resolved on some systems).
Instead, we are manually taking care of checkm's dependencies and just installing
it through pip.

## Notes on Altair version
Installing q2-checkm in an existing QIIME 2 environment by following the instructions above may case Altair to be downgraded to version <5. Proceed with caution! 
