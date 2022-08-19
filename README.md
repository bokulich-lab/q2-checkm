# q2-checkm
![CI](https://github.com/bokulich-lab/q2-checkm/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/bokulich-lab/q2-checkm/branch/main/graph/badge.svg?token=RSZD1TD9HG)](https://codecov.io/gh/bokulich-lab/q2-checkm)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

QIIME 2 plugin for assessing the quality of (meta)genomes using CheckM.

Notes on CheckM version:
CheckM version currently used by q2-checkm is pinned to a specific commit:
https://github.com/Ecogenomics/CheckM.git@8b42a8ca13dda3a967e2247efe6032f9df1bd434.
We are not using the corresponding version available through conda, as it has _pplacer_
as a pinned dependency (and this dependency cannot be resolved on some systems).
Instead, we are manually taking care of checkm's dependencies and just installing
it through pip.
