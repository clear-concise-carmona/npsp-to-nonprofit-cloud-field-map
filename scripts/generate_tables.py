#!/usr/bin/env python3
"""
generate_tables.py

Reads every YAML file in field-map/ and regenerates the matching Markdown
comparison table in docs/. This is the only supported way to edit the
generated docs - edit the YAML, then re-run this script. Do not hand-edit
files under docs/, they will be overwritten.

Usage:
    python scripts/generate_tables.py

Requires: PyYAML (see scripts/requirements.txt)
"""
from __future__ import annotations

import pathlib
import sys

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
FIELD_MAP_DIR = REPO_ROOT / "field-map"
DOCS_DIR = REPO_ROOT / "docs"

RELATIONSHIP_BADGE = {
    "direct": "Direct",
    "renamed": "Renamed",
    "redesign_required": "Redesign required",
    "no_equivalent": "No equivalent",
    "new_in_npc": "New in Nonprofit Cloud",
}

CONFIDENCE_BADGE = {
    "confirmed": "Confirmed",
    "inferred": "Inferred",
    "unconfirmed": "Unconfirmed",
}


def format_sources(sources: list[str]) -> str:
    if not sources:
        return "_none cited_"
    return "; ".join(f"[source]({s})" for s in sources)


def render_object_mapping(mapping: dict) -> str:
    npsp = mapping["npsp_side"]
    npc = mapping["nonprofit_cloud_side"]
    rel = RELATIONSHIP_BADGE.get(mapping["relationship"], mapping["relationship"])
    lines = [
        "## Object-level mapping",
        "",
        f"**NPSP object(s):** `{npsp['object_api_name']}`",
        "",
        npsp["summary"].strip(),
        "",
        f"**Nonprofit Cloud object(s):** `{npc['object_api_name']}`",
        "",
        npc["summary"].strip(),
        "",
        f"**Relationship: {rel}**",
        "",
        mapping["notes"].strip(),
        "",
        f"Sources: {format_sources(mapping.get('sources', []))}",
        "",
    ]
    return "\n".join(lines)


def render_fields_table(fields: list[dict]) -> str:
    header = (
        "| NPSP field | Nonprofit Cloud field | Relationship | Confidence | Notes | Source |\n"
        "|---|---|---|---|---|---|\n"
    )
    rows = []
    for f in fields:
        rel = RELATIONSHIP_BADGE.get(f["relationship"], f["relationship"])
        conf = CONFIDENCE_BADGE.get(f["confidence"], f["confidence"])
        notes = " ".join(f.get("notes", "").split())
        rows.append(
            "| `{npsp}` | `{npc}` | {rel} | {conf} | {notes} | {src} |".format(
                npsp=f["npsp_field"],
                npc=f["nonprofit_cloud_field"],
                rel=rel,
                conf=conf,
                notes=notes,
                src=format_sources(f.get("sources", [])),
            )
        )
    return header + "\n".join(rows) + "\n"


def render_file(yaml_path: pathlib.Path) -> str:
    data = yaml.safe_load(yaml_path.read_text())
    title = yaml_path.stem.replace("-", " ").title()
    parts = [
        f"# {title}: Field Map",
        "",
        f"_Generated from `{yaml_path.relative_to(REPO_ROOT)}` by `scripts/generate_tables.py`. "
        f"Do not hand-edit this file - edit the YAML source and regenerate._",
        "",
        render_object_mapping(data["object_mapping"]),
        "## Field-level mapping",
        "",
        render_fields_table(data["fields"]),
    ]
    return "\n".join(parts)


def main() -> int:
    if not FIELD_MAP_DIR.exists():
        print(f"error: {FIELD_MAP_DIR} not found", file=sys.stderr)
        return 1
    DOCS_DIR.mkdir(exist_ok=True)
    yaml_files = sorted(FIELD_MAP_DIR.glob("*.yaml"))
    if not yaml_files:
        print(f"error: no YAML files found in {FIELD_MAP_DIR}", file=sys.stderr)
        return 1
    for yaml_path in yaml_files:
        out_path = DOCS_DIR / f"field-map-{yaml_path.stem}.md"
        out_path.write_text(render_file(yaml_path))
        print(f"wrote {out_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
