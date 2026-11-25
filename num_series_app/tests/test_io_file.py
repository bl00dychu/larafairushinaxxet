"""Тесты чтения TXT, CSV и автоматического выбора формата."""
import pytest
from num_series.io_file import (
    load_series_txt,
    load_series_csv,
    load_series_auto
)

from num_series.io_json import save_series_json
class TestLoadSeriesTxt:
    def test_valid_txt_with_comments_and_blanks(self, tmp_path):
        path = tmp_path / "data.txt"

        path.write_text(
            "# комментарий\n\n1.5\n-2\n3.25\n",
            encoding="utf-8"
        )

        assert load_series_txt(path) == [
            1.5,
            -2.0,
            3.25
        ]

    def test_non_numeric_line_reports_line_number(self, tmp_path):
        path = tmp_path / "bad.txt"

        path.write_text(
            "1.0\n2.0\nabc\n",
            encoding="utf-8"
        )

        with pytest.raises(
            ValueError,
            match=r":3:"
        ):
            load_series_txt(path)

    def test_empty_file_raises(self, tmp_path):
        path = tmp_path / "empty.txt"

        path.write_text(
            "# только комментарий\n\n",
            encoding="utf-8"
        )

        with pytest.raises(
            ValueError,
            match="не содержит чисел"
        ):
            load_series_txt(path)

class TestLoadSeriesCsv:
    def test_csv_with_header_and_mixed_separators(self, tmp_path):
        path = tmp_path / "data.csv"

        path.write_text(
            "value1,value2\n"
            "1.0, 2.5\n"
            "3.0; 4.5\n",
            encoding="utf-8"
        )

        assert load_series_csv(path) == [
            1.0,
            2.5,
            3.0,
            4.5
        ]
    def test_csv_non_numeric_on_second_line_raises(self, tmp_path):
        path = tmp_path / "bad.csv"

        path.write_text(
            "1.0, 2.0\n"
            "3.0, oops\n",
            encoding="utf-8"
        )

        with pytest.raises(
            ValueError,
            match=r":2:"
        ):
            load_series_csv(path)
    def test_csv_missing_file_raises(self, tmp_path):
        with pytest.raises(
            ValueError,
            match="не найден"
        ):
            load_series_csv(
                tmp_path / "absent.csv"
            )


class TestLoadSeriesAuto:
    def test_auto_detects_json_txt_csv(self, tmp_path):

        json_path = tmp_path / "s.json"

        save_series_json(
            [1.0, 2.0],
            json_path
        )

        txt_path = tmp_path / "s.txt"

        txt_path.write_text(
            "3.0\n4.0\n",
            encoding="utf-8"
        )

        csv_path = tmp_path / "s.csv"

        csv_path.write_text(
            "5.0,6.0\n",
            encoding="utf-8"
        )

        assert load_series_auto(json_path) == [
            1.0,
            2.0
        ]

        assert load_series_auto(txt_path) == [
            3.0,
            4.0
        ]

        assert load_series_auto(csv_path) == [
            5.0,
            6.0
        ]
    def test_csv_with_header_after_comment(self, tmp_path):
        path = tmp_path / "header.csv"

        path.write_text(
            "# generated file\n"
            "value\n"
            "1\n"
            "2\n",
            encoding="utf-8"
        )
        assert load_series_csv(path) == [
            1.0,
            2.0
        ]
