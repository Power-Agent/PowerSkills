from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import pytest

# package_skill imports quick_validate through the scripts package.
sys.path.insert(0, str(Path(__file__).parents[1]))
from scripts.package_skill import package_skill  # noqa: E402


def make_valid_skill(root: Path) -> Path:
    skill_dir = root / "sample-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        "---\nname: sample-skill\ndescription: A test skill.\n---\n\n# Sample\n",
        encoding="utf-8",
    )
    return skill_dir


def test_package_excludes_build_artifacts_but_keeps_nested_evals(tmp_path: Path) -> None:
    skill_dir = make_valid_skill(tmp_path)
    (skill_dir / "guide.md").write_text("Guide", encoding="utf-8")
    (skill_dir / "evals").mkdir()
    (skill_dir / "evals" / "private.json").write_text("{}", encoding="utf-8")
    (skill_dir / "references").mkdir()
    (skill_dir / "references" / "evals").mkdir()
    (skill_dir / "references" / "evals" / "example.json").write_text("{}", encoding="utf-8")
    (skill_dir / "__pycache__").mkdir()
    (skill_dir / "__pycache__" / "module.pyc").write_bytes(b"bytecode")
    (skill_dir / "node_modules").mkdir()
    (skill_dir / "node_modules" / "dependency.js").write_text("ignored", encoding="utf-8")
    (skill_dir / ".DS_Store").write_text("ignored", encoding="utf-8")
    (skill_dir / "module.pyc").write_bytes(b"bytecode")
    output_dir = tmp_path / "dist"

    archive = package_skill(skill_dir, output_dir)

    assert archive is not None
    with zipfile.ZipFile(archive) as zipf:
        names = set(zipf.namelist())
    assert "sample-skill/SKILL.md" in names
    assert "sample-skill/guide.md" in names
    assert "sample-skill/references/evals/example.json" in names
    assert "sample-skill/evals/private.json" not in names
    assert not any("__pycache__" in name or "node_modules" in name for name in names)
    assert not any(name.endswith(".pyc") or name.endswith(".DS_Store") for name in names)


def test_package_skips_symlinked_files_outside_skill_tree(tmp_path: Path) -> None:
    skill_dir = make_valid_skill(tmp_path)
    outside_secret = tmp_path / "outside-secret.txt"
    outside_secret.write_text("do not package", encoding="utf-8")
    link = skill_dir / "external.txt"
    try:
        link.symlink_to(outside_secret)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"symlinks are not available: {exc}")

    archive = package_skill(skill_dir, tmp_path / "dist")

    assert archive is not None
    with zipfile.ZipFile(archive) as zipf:
        names = set(zipf.namelist())
    assert "sample-skill/external.txt" not in names
    assert "sample-skill/SKILL.md" in names


def test_package_rejects_symlinked_skill_manifest(tmp_path: Path) -> None:
    skill_dir = tmp_path / "sample-skill"
    skill_dir.mkdir()
    external_manifest = tmp_path / "external-SKILL.md"
    external_manifest.write_text(
        "---\nname: sample-skill\ndescription: A test skill.\n---\n",
        encoding="utf-8",
    )
    (skill_dir / "SKILL.md").symlink_to(external_manifest)

    assert package_skill(skill_dir, tmp_path / "dist") is None


def test_package_does_not_include_archive_when_output_is_skill_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    skill_dir = make_valid_skill(tmp_path)
    (skill_dir / "guide.md").write_text("Guide", encoding="utf-8")
    monkeypatch.chdir(skill_dir)

    archive = package_skill(skill_dir)

    assert archive == skill_dir / "sample-skill.skill"
    assert archive.is_file()
    with zipfile.ZipFile(archive) as zipf:
        names = set(zipf.namelist())
        assert zipf.testzip() is None
    assert "sample-skill/SKILL.md" in names
    assert "sample-skill/guide.md" in names
    assert "sample-skill/sample-skill.skill" not in names
