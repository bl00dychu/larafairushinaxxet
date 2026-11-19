from main import main
def test_cli_runs(capsys):
    assert main(["--kind", "trend", "--n", "5", "--window", "3"])==0
    assert "Среднее арифметическое" in capsys.readouterr().out
    