#!/usr/bin/env python3
"""Validate skills against the Agent Skills spec and library conventions.

Checks per skills/<dir>/SKILL.md:
  - YAML frontmatter parses and contains required fields
  - name: lowercase-hyphen, <= 64 chars, matches directory name
  - description: non-empty, <= 1024 chars
  - body: non-empty
  - every "see <skill-name>" cross-reference resolves to a skill in this repo
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
XREF_RE = re.compile(r"see ([a-z0-9]+(?:-[a-z0-9]+)+)")

def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm_text = text[3:end]
    body = text[end + 4:]
    # Minimal YAML: top-level "key:" scalars and folded strings; enough for validation.
    fields = {}
    current_key = None
    for line in fm_text.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z-]+):\s*(.*)$", line)
        if m:
            current_key = m.group(1)
            val = m.group(2).strip()
            fields[current_key] = "" if val in (">-", ">", "|", "|-") else val
        elif line.startswith((" ", "\t")) and current_key:
            fields[current_key] = (fields[current_key] + " " + line.strip()).strip()
    return fields, body

def main() -> int:
    errors = []
    dirs = sorted(d for d in SKILLS.iterdir() if d.is_dir())
    names = {d.name for d in dirs}
    if not dirs:
        errors.append("no skill directories found under skills/")

    for d in dirs:
        skill_md = d / "SKILL.md"
        label = f"skills/{d.name}"
        if not skill_md.exists():
            errors.append(f"{label}: missing SKILL.md")
            continue
        text = skill_md.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{label}: missing or unterminated YAML frontmatter")
            continue
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if not name:
            errors.append(f"{label}: frontmatter missing required 'name'")
        elif not NAME_RE.match(name):
            errors.append(f"{label}: name '{name}' must be lowercase-hyphen")
        elif len(name) > 64:
            errors.append(f"{label}: name exceeds 64 characters")
        elif name != d.name:
            errors.append(f"{label}: name '{name}' != directory '{d.name}'")
        if not desc:
            errors.append(f"{label}: frontmatter missing required 'description'")
        elif len(desc) > 1024:
            errors.append(f"{label}: description is {len(desc)} chars (max 1024)")
        if not body.strip():
            errors.append(f"{label}: empty body")
        for ref in XREF_RE.findall(body):
            if ref not in names:
                errors.append(f"{label}: dangling cross-reference 'see {ref}'")

    if errors:
        print(f"FAIL — {len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK — {len(dirs)} skills validated, all cross-references resolve.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
