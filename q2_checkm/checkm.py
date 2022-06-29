# ----------------------------------------------------------------------------
# Copyright (c) 2022, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import glob
import json
import os
import tempfile
from copy import deepcopy
from distutils.dir_util import copy_tree
from typing import Mapping
from zipfile import ZipFile

import pandas as pd
import pkg_resources
import q2templates
from q2_types_genomics.per_sample_data._format import MultiMAGSequencesDirFmt

from q2_checkm.plots import _draw_detailed_plots, _draw_overview_plots
from q2_checkm.utils import (
    _get_plots_per_sample,
    _process_checkm_arg,
    _process_common_input_params,
    run_command,
)

TEMPLATES = pkg_resources.resource_filename("q2_checkm", "assets")


def _evaluate_bins(
    results_dir: str, bins: MultiMAGSequencesDirFmt, db_path: str, common_args: list
) -> dict:
    """Evaluates bins for all samples using CheckM.

    Args:
        results_dir (str): Location where the final results should be stored.
        bins (MultiMAGSequencesDirFmt): The bins to be analyzed.
        db_path (str): Path to the CheckM database.
        common_args (list): List of common arguments to be passed to CheckM.

    Returns:
        dict: Dictionary containing the paths to the generated reports.
    """
    base_cmd = ["checkm", "lineage_wf", *common_args]
    stats_fps = {}

    manifest: pd.DataFrame = bins.manifest.view(pd.DataFrame)
    manifest["sample_dir"] = manifest.filename.apply(lambda x: os.path.dirname(x))
    sample_dirs = manifest["sample_dir"].unique()
    for sample_dir in sample_dirs:
        sample = os.path.split(sample_dir)[-1]
        sample_results = os.path.join(results_dir, sample)

        cmd = deepcopy(base_cmd)
        cmd.extend(["-x", "fasta", sample_dir, sample_results])
        run_command(cmd, env={**os.environ, "CHECKM_DATA_PATH": db_path})

        stats_fp = os.path.join(sample_results, "storage", "bin_stats_ext.tsv")
        if os.path.isfile(stats_fp):
            stats_fps[sample] = stats_fp
        else:
            raise FileNotFoundError(f"CheckM stats file {stats_fp} could not be found.")

    return stats_fps


def _draw_checkm_plots(
    results_dir: str, bins: MultiMAGSequencesDirFmt, db_path: str, plot_type: str = "gc"
) -> dict:
    """Draws CheckM plots for all samples.

    Args:
        results_dir (str): Location where the plots should be stored.
        bins (MultiMAGSequencesDirFmt): The bins to be analyzed.
        db_path (str): The path to the CheckM database.
        plot_type (str): The type of plot to be drawn (one of: gc/nx/coding).

    Returns:
        dict: A dictionary containing the paths to the generated plots in a
            form: {sample_id: plot_dir}.
    """
    base_cmd = [
        "checkm",
        f"{plot_type}_plot",
        "-x",
        "fasta",
        "--image_type",
        "svg",
        "--font_size",
        "10",
    ]
    # TODO: the numbers should probably be configurable
    dist_values = [] if plot_type == "nx" else ["50", "75", "90"]
    plots = {}

    manifest: pd.DataFrame = bins.manifest.view(pd.DataFrame)
    manifest["sample_dir"] = manifest.filename.apply(lambda x: os.path.dirname(x))
    sample_dirs = manifest["sample_dir"].unique()
    for sample_bins in sample_dirs:
        sample = os.path.split(sample_bins)[-1]
        sample_plots = os.path.join(results_dir, "plots", plot_type, sample)
        checkm_files = os.path.join(results_dir, sample)
        plots[sample] = sample_plots

        cmd = deepcopy(base_cmd)
        cmd.append(checkm_files) if plot_type == "coding" else False
        cmd.extend([sample_bins, sample_plots, *dist_values])
        run_command(cmd, env={**os.environ, "CHECKM_DATA_PATH": db_path})
    return plots


def _parse_checkm_reports(reports: Mapping[str, str]) -> pd.DataFrame:
    """Combines CheckM's reports from all samples into one pandas DataFrame.

    Args:
        reports (Mapping[str, str]): A dictionary containing report paths.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the parsed CheckM metrics.
    """
    dfs = [_parse_single_checkm_report(_id, fp) for _id, fp in reports.items()]
    results_df = pd.concat(dfs)
    results_df.reset_index(drop=True, inplace=True)
    return results_df


def _parse_single_checkm_report(sample_id: str, report_fp: str) -> pd.DataFrame:
    """Parses a single CheckM report into a pandas DataFrame.

    Args:
        sample_id (str): The sample ID.
        report_fp (str): The path to the CheckM report file.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the parsed CheckM
            metrics for a single sample.
    """
    # read the raw CheckM report
    with open(report_fp, "r") as fh:
        stats = {
            k: json.loads(v.replace("'", '"'))
            for [k, v] in [line.split("\t") for line in fh.readlines()]
        }

    # convert report to DataFrame
    df = pd.DataFrame.from_dict(stats, orient="index")
    df.reset_index(drop=False, inplace=True)
    col_names = {
        "index": "bin_id",
        "marker lineage": "marker_lineage",
        "# genomes": "genomes",
        "# markers": "markers",
        "# marker sets": "marker_sets",
        "0": "count0",
        "1": "count1",
        "2": "count2",
        "3": "count3",
        "4": "count4",
        "5+": "count5_or_more",
        "Completeness": "completeness",
        "Contamination": "contamination",
        "GC": "gc",
        "GC std": "gc_std",
        "Genome size": "genome_size",
        "# ambiguous bases": "ambiguous_bases",
        "# scaffolds": "scaffolds",
        "# contigs": "contigs",
        "Longest scaffold": "longest_scaffold",
        "Longest contig": "longest_contig",
        "N50 (scaffolds)": "n50_scaffolds",
        "N50 (contigs)": "n50_contigs",
        "Mean scaffold length": "mean_scaffold_length",
        "Mean contig length": "mean_contig_length",
        "Coding density": "coding_density",
        "Translation table": "translation_table",
        "# predicted genes": "predicted_genes",
        "GCN0": "gcn0",
        "GCN1": "gcn1",
        "GCN2": "gcn2",
        "GCN3": "gcn3",
        "GCN4": "gcn4",
        "GCN5+": "gcn5_or_more",
    }
    df.rename(columns=col_names, inplace=True)
    df["sample_id"] = sample_id

    # reorder columns
    df = df[["sample_id", *col_names.values()]]

    return df


def _classify_completeness(completeness: float) -> str:
    """Converts CheckM's completeness score into one of four
        completeness categories.

    Args:
        completeness (float): CheckM's completeness score (0-100).

    Returns:
        str: One of four completeness categories.
    """
    if completeness >= 90.0:
        return "near"
    elif 90.0 > completeness >= 70.0:
        return "substantial"
    elif 70.0 > completeness >= 50.0:
        return "moderate"
    else:
        return "partial"


def _zip_checkm_plots(plots_per_sample: Mapping[str, Mapping[str, str]], zip_path: str):
    """Creates a single zip archive containing all plots produced by CheckM
        for all the samples.

    Args:
        plots_per_sample (Mapping[str, Mapping[str, str]]): Dictionary
            containing the mapping of plot paths per plot type per sample.
        zip_path (str): The path to the zip archive.
    """
    with ZipFile(zip_path, "w") as zf:
        for sample_id in plots_per_sample.keys():
            plot_fps = [
                glob.glob(os.path.join(v, "*.svg"))
                for k, v in plots_per_sample[sample_id].items()
            ]
            plot_fps = [x for sublist in plot_fps for x in sublist]
            common_path = os.path.commonpath(plot_fps)
            for plot_fp in plot_fps:
                arcname = os.path.relpath(plot_fp, common_path)
                zf.write(plot_fp, arcname=arcname)


def evaluate_bins(
    output_dir: str,
    bins: MultiMAGSequencesDirFmt,
    db_path: str,
    reduced_tree: bool = None,
    unique: int = None,
    multi: int = None,
    force_domain: bool = None,
    no_refinement: bool = None,
    individual_markers: bool = None,
    skip_adj_correction: bool = None,
    skip_pseudogene_correction: bool = None,
    aai_strain: float = None,
    ignore_thresholds: bool = None,
    e_value: float = None,
    length: float = None,
    threads: int = None,
    pplacer_threads: int = None,
):

    kwargs = {
        k: v for k, v in locals().items() if k not in ["output_dir", "bins", "db_path"]
    }
    common_args = _process_common_input_params(
        processing_func=_process_checkm_arg, params=kwargs
    )

    # TODO: check that CheckM's database is available (or fetch?)

    with tempfile.TemporaryDirectory() as tmp:
        results_dir = os.path.join(tmp, "results")

        # run CheckM's lineage_wf pipeline, draw all the QC plots and zip
        # them into a single archive for download
        reports = _evaluate_bins(results_dir, bins, db_path, common_args)
        all_plots = {}
        for plot_type in ["gc", "nx", "coding"]:
            plot_dirs = _draw_checkm_plots(
                results_dir, bins, db_path, plot_type=plot_type
            )
            all_plots[f"plots_{plot_type}"] = plot_dirs

        plots_per_sample = _get_plots_per_sample(all_plots)

        _zip_checkm_plots(
            plots_per_sample, os.path.join(TEMPLATES, "checkm", "checkm_plots.zip")
        )

        # TODO: calculate bin coverage and add one more plot
        #  (depth vs. genome size)

        # convert CheckM reports into a DataFrame and add completeness info
        checkm_results = _parse_checkm_reports(reports)
        checkm_results.to_csv(
            os.path.join(TEMPLATES, "checkm", "results.tsv"),
            sep="\t",
            index=False,
        )
        checkm_results["qc_category"] = checkm_results["completeness"].apply(
            _classify_completeness
        )

        # prepare viz templates and copy all the required files
        context = {
            "tabs": [
                {"title": "QC overview", "url": "index.html"},
                {"title": "Sample details", "url": "sample_details.html"},
            ],
            "samples": json.dumps(list(reports.keys())),
            "vega_plots_detailed": json.dumps(_draw_detailed_plots(checkm_results)),
            "vega_plots_overview": json.dumps(_draw_overview_plots(checkm_results)),
        }

        index = os.path.join(TEMPLATES, "checkm", "index.html")
        sample_details = os.path.join(TEMPLATES, "checkm", "sample_details.html")

        copy_tree(os.path.join(TEMPLATES, "checkm"), output_dir)
        copy_tree(os.path.join(results_dir, "plots"), os.path.join(output_dir, "plots"))

        templates = [index, sample_details]
        q2templates.render(templates, output_dir, context=context)

        # until Bootstrap 3 is replaced with v5, remove the v3 scripts as
        # the HTML files are adjusted to work with v5
        os.remove(
            os.path.join(output_dir, "q2templateassets", "css", "bootstrap.min.css")
        )
        os.remove(
            os.path.join(output_dir, "q2templateassets", "js", "bootstrap.min.js")
        )
