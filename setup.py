# ----------------------------------------------------------------------------
# Copyright (c) 2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import find_packages, setup

import versioneer

setup(
    name="q2-checkm",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license="BSD-3-Clause",
    packages=find_packages(),
    author="Michal Ziemski",
    author_email="ziemski.michal@gmail.com",
    description="QIIME 2 plugin for (meta)genome quality assessment using CheckM.",
    url="https://github.com/bokulich-lab/q2-checkm",
    entry_points={"qiime2.plugins": ["q2-checkm=q2_checkm.plugin_setup:plugin"]},
    package_data={
        "q2_checkm": [
            "citations.bib",
            "assets/checkm/*",
            "assets/checkm/data/*",
            "assets/checkm/js/*",
            "assets/checkm/css/*",
        ],
        "q2_checkm.tests": [
            "data/*",
            "data/bins/*",
            "data/bins/*/*",
            "data/checkm_reports/*/*/*",
            "data/plots/*/*/*",
        ],
    },
    zip_safe=False,
)
