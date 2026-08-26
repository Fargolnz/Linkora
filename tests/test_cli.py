"""End-to-end tests driving the command-line interface."""

from __future__ import annotations

import sys

import pytest

import main as cli


def _run_cli(argv, tmp_path, capsys):
    code = cli.main(argv + ["--out", str(tmp_path)])
    captured = capsys.readouterr()
    return code, captured


def test_compiles_sample(tmp_path, capsys):
    source = tmp_path / "page.lkr"
    source.write_text(
        'Link { title: "GitHub", url: "https://github.com" }\n',
        encoding="utf-8",
    )
    out_dir = tmp_path / "site"

    code = cli.main([str(source), "--out", str(out_dir)])
    captured = capsys.readouterr()

    assert code == 0
    assert (out_dir / "index.html").is_file()
    assert "Generated" in captured.out


def test_reports_errors_and_returns_nonzero(tmp_path, capsys):
    source = tmp_path / "bad.lkr"
    source.write_text(
        'Link { title: "GitHub" }\n',
        encoding="utf-8",
    )
    out_dir = tmp_path / "site"

    code = cli.main([str(source), "--out", str(out_dir)])
    captured = capsys.readouterr()

    assert code == 1
    assert "Semantic Error" in captured.err
    assert "required property 'url'" in captured.err
    assert not (out_dir / "index.html").exists()


def test_missing_source_file_returns_nonzero(tmp_path, capsys):
    code = cli.main([str(tmp_path / "nope.lkr"), "--out", str(tmp_path / "site")])
    captured = capsys.readouterr()
    assert code == 1
    assert "source file not found" in captured.err


def test_default_output_directory(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "page.lkr"
    source.write_text('', encoding="utf-8")

    code = cli.main([str(source)])
    capsys.readouterr()

    assert code == 0
    assert (tmp_path / "output" / "index.html").is_file()


def test_imported_main_is_executable():
    assert callable(cli.main)
    assert cli.__name__ == "main"
