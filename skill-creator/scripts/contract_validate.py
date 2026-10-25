"""Validate PowerSkills workflow, escalation, and bundled asset contracts."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOTS = (
    ROOT / "powerskills-tool" / "skills",
    ROOT / "powerskills-engineering" / "skills",
)
REF_PATTERN = re.compile(r"`((?:scripts|references|assets|evals)/[^'`\s)]+)`")
ROOT_ASSET_PATTERN = re.compile(r"`([A-Za-z0-9_.-]+\.(?:py|sh|yaml|yml|md|txt|json|nc|csv|dss|xlsx|sav|raw|dyr))`")
TOOL_PATTERN = re.compile(r"`([A-Za-z_][A-Za-z0-9_]*)\s*\(")


def parse_skill(path: Path) -> tuple[str, list[str]]:
    issues = []
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---" not in text[4:]:
        return text, ["missing or malformed YAML frontmatter"]
    closing = text.find("\n---", 4)
    body = text[closing + 4:]
    is_tool_skill = "powerskills-tool" in path.parts
    if is_tool_skill:
        if not re.search(r"(?mi)^#{1,3}\s+Escalation triggers\s*$", body):
            issues.append("missing Escalation triggers section")
    elif not re.search(r"(?mi)^#{1,3}\s+Preferred action order\s*$", body):
        issues.append("missing Preferred action order section")
    if is_tool_skill:
        if not re.search(r"(?mi)^#{1,3}\s+(Default tool ladder|Default ladder)\s*$", body):
            issues.append("missing default tool ladder")
        ladder = re.search(r"(?is)#{1,3}\s+(?:Default tool ladder|Default ladder)\s*\n(.*?)(?=\n#{1,3}\s|\Z)", body)
        if ladder:
            first = next((line for line in ladder.group(1).splitlines() if line.strip()), "").lower()
            if re.search(r"contingenc|eigenvalue|time.domain|optim[iz]e|harmonic|unit.commitment", first):
                issues.append("workflow does not start from the base case")
    if not re.search(r"(?mi)^#{1,3}\s+(Deliver|Report back)\s*$", body):
        issues.append("missing Deliver section")
    path_refs = set(REF_PATTERN.findall(body))
    path_basenames = {Path(ref).name for ref in path_refs}
    root_refs = set(ROOT_ASSET_PATTERN.findall(body))
    # A basename mentioned in prose is not a second root-level asset when the
    # same file is already referenced with its bundled relative path.
    refs = path_refs | {ref for ref in root_refs if ref not in path_basenames}
    for ref in sorted(refs):
        if not (path.parent / ref).exists():
            issues.append(f"missing bundled asset: {ref}")
    return body, issues


def validate(root: Path = ROOT) -> list[str]:
    """Validate skills under the supplied checkout root, not this script's checkout."""
    root = root.resolve()
    skill_roots = (
        root / "powerskills-tool" / "skills",
        root / "powerskills-engineering" / "skills",
    )
    failures = []
    count = 0
    for skill_root in skill_roots:
        if not skill_root.is_dir():
            failures.append(f"missing skill root: {skill_root.relative_to(root)}")
            continue
        for skill_md in sorted(skill_root.glob("*/SKILL.md")):
            count += 1
            _, issues = parse_skill(skill_md)
            failures.extend(f"{skill_md.relative_to(root)}: {issue}" for issue in issues)
    if count == 0:
        failures.append("no SKILL.md files discovered")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="PowerSkills checkout root")
    args = parser.parse_args()
    failures = validate(args.root.resolve())
    if failures:
        print("\n".join(f"FAIL: {failure}" for failure in failures))
        print(f"{len(failures)} contract failure(s)")
        return 1
    print("Skill contract validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
