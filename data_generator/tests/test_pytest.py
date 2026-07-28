"""Tests for data_generator package."""

import pandas as pd
import pytest

from data_generator import available_models, generate_dataset, generate_truth_dataset


def test_available_models_has_expected_entries() -> None:
    models = available_models()
    assert models == sorted(models)
    assert {"exponential", "linear", "quadratic", "logarithmic"}.issubset(models)


def test_generate_dataset_default_shape_and_metadata() -> None:
    data, truth = generate_dataset(seed=42, n_points=25)
    assert isinstance(data, pd.DataFrame)
    assert list(data.columns) == ["x", "y"]
    assert len(data) == 25
    assert truth["model_name"] in available_models()
    assert truth["seed"] == 42


def test_generate_dataset_specific_model_is_used() -> None:
    _, truth = generate_dataset(model_name="linear", seed=1)
    assert truth["model_name"] == "linear"


def test_generate_dataset_reproducible_with_seed() -> None:
    data_a, truth_a = generate_dataset(model_name="quadratic", seed=123)
    data_b, truth_b = generate_dataset(model_name="quadratic", seed=123)
    pd.testing.assert_frame_equal(data_a, data_b)
    assert truth_a == truth_b


def test_generate_dataset_bad_model_raises() -> None:
    with pytest.raises(ValueError, match="Unknown model"):
        generate_dataset(model_name="does-not-exist")


def test_generate_dataset_bad_n_points_raises() -> None:
    with pytest.raises(ValueError, match="n_points"):
        generate_dataset(n_points=1)


def test_generate_dataset_negative_noise_raises() -> None:
    with pytest.raises(ValueError, match="noise_fraction"):
        generate_dataset(noise_fraction=-0.1)


def test_generate_truth_dataset_defaults_to_original_point_count() -> None:
    _, truth = generate_dataset(model_name="linear", seed=3, n_points=17)
    truth_data = generate_truth_dataset(truth)
    assert list(truth_data.columns) == ["x", "y"]
    assert len(truth_data) == 17


def test_generate_truth_dataset_accepts_override_point_count() -> None:
    _, truth = generate_dataset(model_name="linear", seed=3, n_points=17)
    truth_data = generate_truth_dataset(truth, n_points=9)
    assert len(truth_data) == 9
