"""Тесты генераторов числовых рядов."""
import pytest
from num_series.generator import (
    _validate_n,
    random_series,
    sine_series,
    trend_series
)
class TestValidateN:
    @pytest.mark.parametrize(
        "n",
        [1, 5, 100, 1000, 3.0]
    )
    def test_positive_integer_passes(self, n):
        _validate_n(n)

    @pytest.mark.parametrize(
        "n",
        [0, -1, -100, True, False]
    )
    def test_zero_negative_and_bool_rejected(self, n):
        with pytest.raises(
            ValueError,
            match="положительным целым"
        ):
            _validate_n(n)

    @pytest.mark.parametrize(
        "n",
        [3.5, -0.1, 1.0000001]
    )
    def test_non_integer_float_rejected(self, n):
        with pytest.raises(
            ValueError,
            match="положительным целым"
        ):
            _validate_n(n)

    @pytest.mark.parametrize(
        "n",
        ["5", "abc", None, [5], {"n": 5}]
    )
    def test_bad_types_rejected(self, n):
        with pytest.raises(
            ValueError,
            match="положительным целым"
        ):
            _validate_n(n)
    def test_error_message_contains_value_and_cause(self):
        with pytest.raises(ValueError) as exc_info:
            _validate_n("abc")

        assert "'abc'" in str(exc_info.value)
        assert "причина" in str(exc_info.value)
class TestRandomSeries:
    def test_length_and_float_type(self):
        data = random_series(10, seed=1)

        assert len(data) == 10

        assert all(
            isinstance(value, float)
            for value in data
        )
    def test_reproducible_with_seed(self):
        assert (
            random_series(20, seed=42)
            == random_series(20, seed=42)
        )
    def test_different_seeds_differ(self):
        assert (
            random_series(20, seed=1)
            != random_series(20, seed=2)
        )
    def test_within_bounds(self):
        data = random_series(
            100,
            low=-5,
            high=5,
            seed=0
        )

        assert all(
            -5 <= value <= 5
            for value in data
        )
    def test_low_must_be_less_than_high(self):
        with pytest.raises(
            ValueError,
            match="low должно быть меньше high"
        ):
            random_series(
                5,
                low=10,
                high=5
            )
    def test_invalid_n_raises(self):
        with pytest.raises(ValueError):
            random_series(0)
class TestSineSeries:
    def test_length_and_reproducible(self):
        assert len(sine_series(30, seed=0)) == 30

        assert (
            sine_series(30, noise=0.5, seed=7)
            == sine_series(30, noise=0.5, seed=7)
        )
    def test_zero_noise_is_deterministic(self):
        assert (
            sine_series(20, noise=0.0, seed=1)
            == sine_series(20, noise=0.0, seed=999)
        )
    def test_amplitude_bounds_without_noise(self):
        data = sine_series(
            100,
            amplitude=2.0,
            noise=0.0
        )

        assert all(
            -2.0 - 1e-9 <= value <= 2.0 + 1e-9
            for value in data
        )
    def test_negative_noise_rejected(self):
        with pytest.raises(ValueError, match="noise"):
            sine_series(10, noise=-0.1)
class TestTrendSeries:
    def test_linear_without_noise(self):
        assert trend_series(
            5,
            start=0,
            step=2.0,
            noise=0.0
        ) == [
            0.0,
            2.0,
            4.0,
            6.0,
            8.0
        ]
    def test_length_and_reproducible(self):
        assert len(trend_series(15, seed=0)) == 15

        assert (
            trend_series(10, noise=0.5, seed=3)
            == trend_series(10, noise=0.5, seed=3)
        )