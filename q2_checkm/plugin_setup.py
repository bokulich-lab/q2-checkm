# ----------------------------------------------------------------------------
# Copyright (c) 2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from q2_types.sample_data import SampleData
from q2_types_genomics.per_sample_data import MAGs
from qiime2.core.type import Bool, Float, Int, Range, Str
from qiime2.plugin import Citations, Plugin

import q2_checkm
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

checkm_params = {
    "db_path": Str,
    "reduced_tree": Bool,
    "unique": Int % Range(1, None),
    "multi": Int % Range(1, None),
    "force_domain": Bool,
    "no_refinement": Bool,
    "individual_markers": Bool,
    "skip_adj_correction": Bool,
    "skip_pseudogene_correction": Bool,
    "aai_strain": Float % Range(0, 1),
    "ignore_thresholds": Bool,
    "e_value": Float % Range(0, 1),
    "length": Float % Range(0, 1),
    "threads": Int % Range(1, None),
    "pplacer_threads": Int % Range(1, None),
}

# fmt: off
checkm_param_descriptions = {
    "db_path": "Path to the database required by CheckM. For more details see: "
               "https://github.com/Ecogenomics/CheckM/wiki/Installation#"
               "required-reference-data.",
    "reduced_tree": "Use reduced tree (requires <16GB of memory) for "
                    "determining lineage of each bin.",
    "unique": "Minimum number of unique phylogenetic markers required to use "
              "lineage-specific marker set. Default: 10.",
    "multi": "Maximum number of multi-copy phylogenetic markers before "
             "defaulting to domain-level marker set. Default: 10.",
    "force_domain": "Use domain-level sets for all bins.",
    "no_refinement": "Do not perform lineage-specific marker set refinement.",
    "individual_markers": "Treat marker as independent "
                          "(i.e., ignore co-located set structure).",
    "skip_adj_correction": "Do not exclude adjacent marker genes when "
                           "estimating contamination.",
    "skip_pseudogene_correction": "Skip identification and filtering of pseudogenes.",
    "aai_strain": "AAI threshold used to identify strain heterogeneity. Default: 0.9.",
    "ignore_thresholds": "Ignore model-specific score thresholds.",
    "e_value": "E-value cut off. Default: 1e-10.",
    "length": "Percent overlap between target and query. Default: 0.7.",
    "threads": "Number of threads. Default: 1.",
    "pplacer_threads": "Number of threads used by pplacer (memory usage increases "
                       "linearly with additional threads). Default: 1."
}
# fmt: on

plugin.visualizers.register_function(
    function=q2_checkm.evaluate_bins,
    inputs={
        "bins": SampleData[MAGs],
    },
    parameters=checkm_params,
    input_descriptions={
        "bins": "MAGs to be analyzed.",
    },
    parameter_descriptions=checkm_param_descriptions,
    name="Evaluate quality of the generated MAGs using CheckM.",
    description="This method uses CheckM to assess the quality of assembled MAGs.",
    citations=[
        citations["matsen2010"],
        citations["hyatt2012"],
        citations["parks2015b"],
        citations["hmmer2022"],
    ],
)
