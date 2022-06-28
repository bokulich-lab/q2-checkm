# ----------------------------------------------------------------------------
# Copyright (c) 2022, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import Citations, Plugin

from q2_checkm import __version__

citations = Citations.load("citations.bib", package="q2_checkm")

plugin = Plugin(
    name="checkm",
    version=__version__,
    website="https://github.com/bokulich-lab/q2-checkm",
    package="q2_checkm",
    description="QIIME 2 plugin for (meta)genome quality assessment using CheckM.",
    short_description="QIIME 2 plugin for genome QC using CheckM.",
)
