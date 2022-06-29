# ----------------------------------------------------------------------------
# Copyright (c) 2022, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import unittest

from qiime2.plugin.testing import TestPluginBase

from q2_checkm.utils import (
    _get_plots_per_sample,
    _process_checkm_arg,
    _process_common_input_params,
)


def fake_processing_func(key, val):
    if not val:
        return
    elif isinstance(val, bool):
        return [f"--{key}"]
    else:
        return [f"--{key}", str(val)]


class TestCheckMUtils(TestPluginBase):
    package = "q2_checkm.tests"

    def test_process_common_inputs_bools(self):
        kwargs = {"arg1": False, "arg2": True}
        obs = _process_common_input_params(fake_processing_func, kwargs)
        exp = ["--arg2"]
        self.assertListEqual(obs, exp)

    def test_process_common_inputs_nones(self):
        kwargs = {"arg1": "some-value", "arg2": None}
        obs = _process_common_input_params(fake_processing_func, kwargs)
        exp = ["--arg1", "some-value"]
        self.assertListEqual(obs, exp)

    def test_process_common_inputs_with_values(self):
        kwargs = {"arg1": "value1", "arg2": "value2"}
        obs = _process_common_input_params(fake_processing_func, kwargs)
        exp = ["--arg1", "value1", "--arg2", "value2"]
        self.assertListEqual(obs, exp)

    def test_process_common_inputs_mix(self):
        kwargs = {"arg1": None, "arg2": "some-value", "arg3": False, "arg4": True}
        obs = _process_common_input_params(fake_processing_func, kwargs)
        exp = ["--arg2", "some-value", "--arg4"]
        self.assertListEqual(obs, exp)

    def test_process_arg_bool(self):
        obs = _process_checkm_arg("reduced_tree", True)
        exp = ["--reduced_tree"]
        self.assertListEqual(exp, obs)

    def test_process_arg_non_bool(self):
        obs = _process_checkm_arg("threads", 2)
        exp = ["--threads", "2"]
        self.assertListEqual(exp, obs)

    def test_get_plots_per_sample(self):
        obs = _get_plots_per_sample(
            {
                "plots_gc": {"samp1": "abc", "samp2": "def"},
                "plots_nx": {"samp1": "cba", "samp2": "fed"},
            }
        )
        exp = {
            "samp1": {"plots_gc": "abc", "plots_nx": "cba"},
            "samp2": {"plots_gc": "def", "plots_nx": "fed"},
        }
        self.assertDictEqual(exp, obs)

    def test_get_plots_per_sample_uneven(self):
        with self.assertRaisesRegex(ValueError, r".*Sample counts were: \[2, 1, 3\]."):
            _get_plots_per_sample(
                {
                    "plots_gc": {"samp1": "abc", "samp2": "def"},
                    "plots_nx": {"samp1": "cba"},
                    "plots_coding": {"samp1": "a", "samp2": "d", "samp3": "e"},
                }
            )


if __name__ == "__main__":
    unittest.main()
