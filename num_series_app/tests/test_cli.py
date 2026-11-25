"""Интеграционные проверки CLI через subprocess."""
import subprocess
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
MAIN = ROOT / "main.py"

def run_cli(*args: str) -> subprocess.CompletedProcess:
    """Запускает main.py текущим интерпретатором Python."""

    return subprocess.run(
        [
            sys.executable,
            str(MAIN),
            *args
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
        timeout=30
    )
class TestCLI:
    def test_runs_successfully(self):
        result = run_cli(
            "--kind", "sine",
            "--n", "20",
            "--window", "3",
            "--seed", "1"
        )

        assert result.returncode == 0, result.stderr

        assert "Среднее арифметическое" in result.stdout
        assert "SMA" in result.stdout
        assert "EMA" in result.stdout

    def test_all_kinds_work(self):

        for kind in ("random", "sine", "trend"):

            result = run_cli(
                "--kind", kind,
                "--n", "10",
                "--window", "3"
            )

            assert result.returncode == 0, (
                f"{kind}: {result.stderr}"
            )

    def test_defaults_work(self):
        result = run_cli()

        assert result.returncode == 0, result.stderr

    def test_invalid_kind_fails(self):
        result = run_cli(
            "--kind",
            "foo"
        )

        assert result.returncode != 0

    def test_invalid_n_fails_gracefully(self):
        result = run_cli(
            "--n",
            "-5"
        )

        assert result.returncode == 1
        assert "Ошибка" in result.stderr

    def test_invalid_window_fails_gracefully(self):
        result = run_cli(
            "--n", "5",
            "--window", "10"
        )

        assert result.returncode == 1
        assert "больше длины" in result.stderr

    def test_benchmark_flag(self):
        result = run_cli(
            "--kind", "random",
            "--n", "50",
            "--window", "5",
            "--benchmark"
        )

        assert result.returncode == 0, result.stderr

        assert "list" in result.stdout
        assert "deque" in result.stdout
class TestCLIIO:
    def test_save_then_load(self, tmp_path):

        pytest.importorskip(
            "num_series.io_json"
        )

        path = tmp_path / "series.json"

        first = run_cli(
            "--kind", "sine",
            "--n", "10",
            "--window", "3",
            "--save", str(path)
        )

        assert first.returncode == 0, first.stderr
        assert path.exists()

        second = run_cli(
            "--load", str(path),
            "--window", "3"
        )

        assert second.returncode == 0, second.stderr

        assert "Источник данных: файл:" in second.stdout

    def test_load_missing_file_fails(self, tmp_path):

        result = run_cli(
            "--load",
            str(tmp_path / "nope.json")
        )

        assert result.returncode == 1
        assert "не найден" in result.stderr

    def test_export_csv(self, tmp_path):

        path = tmp_path / "series.csv"

        result = run_cli(
            "--n", "10",
            "--window", "3",
            "--export", str(path)
        )

        assert result.returncode == 0, result.stderr
        assert path.exists()
        assert (
            path.read_text(
                encoding="utf-8"
            ).splitlines()[0]
            == "i,value"
        )
