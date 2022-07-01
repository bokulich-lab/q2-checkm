# q2-checkm
![CI](https://github.com/bokulich-lab/q2-checkm/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/bokulich-lab/q2-checkm/branch/main/graph/badge.svg?token=RSZD1TD9HG)](https://codecov.io/gh/bokulich-lab/q2-checkm)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

QIIME 2 plugin for assessing the quality of (meta)genomes using CheckM.

Notes on CheckM compatibility:
CheckM version currently used by q2-checkm is pinned to a specific commit:
https://github.com/misialq/CheckM.git@29916b666ba8834d0191d631110ffbdf4494cac9.
This is required to make it compatible with the most recent QIIME 2 version
which uses Python 3.8.
