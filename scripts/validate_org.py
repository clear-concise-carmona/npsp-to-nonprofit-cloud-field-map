#!/usr/bin/env python3
"""
validate_org.py

Diffs this repo's field map against the actual schema of a live Salesforce org,
using the Tooling/Schema REST API. Use this to:

  1. Confirm entries marked "confidence: inferred" or "confidence: unconfirmed"
     against a real Nonprofit Cloud org.
  2. Catch drift - Salesforce ships new API versions regularly, and Nonprofit
     Cloud's Fundraising objects are still under active development
     (several objects in this map were introduced as recently as API v64.0).
  3. Sanity-check that an NPSP object this map assumes still exists in your org
     actually exists, before you rely on it for a migration script.

This script does NOT modify anything in the target org. It only reads schema
metadata (describe calls), never record data.

Setup:
    pip install -r requirements.txt
    export SF_INSTANCE_URL="https://your-domain.my.salesforce.com"
    export SF_ACCESS_TOKEN="..."     # e.g. from `sf org display --json`

Usage:
    python scripts/validate_org.py --side npsp     # check NPSP objects/fields exist
    python scripts/validate_org.py --side npc       # check Nonprofit Cloud objects/fields exist
    python scripts/validate_org.py --side both      # check everything referenced in the map

Exit code is non-zero if any *confirmed* map entry fails to match the org
(a stronger signal than mismatches on inferred/unconfirmed rows, which are
expected to need this kind of check).
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import sys
from dataclasses import dataclass, field

import requests
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
FIELD_MAP_DIR = REPO_ROOT / "field-map"

API_VERSION = "v62.0"


@dataclass
class DescribeCache:
    instance_url: str
    access_token: str
    _cache: dict = field(default_factory=dict)

    def describe(self, sobject: str) -> dict | None:
        """Return the describe payload for `sobject`, or None if it doesn't exist."""
        if sobject in self._cache:
            return self._cache[sobject]
        url = f"{self.instance_url}/services/data/{API_VERSION}/sobjects/{sobject}/describe"
        resp = requests.get(
            url, headers={"Authorization": f"Bearer {self.access_token}"}, timeout=30
        )
        if resp.status_code == 404:
            self._cache[sobject] = None
            return None
        resp.raise_for_status()
        payload = resp.json()
        self._cache[sobject] = payload
        return payload

    def field_names(self, sobject: str) -> set[str] | None:
        payload = self.describe(sobject)
        if payload is None:
            return None
        return {f["name"] for f in payload.get("fields", [])}


API_NAME_RE = re.compile(r"([A-Za-z0-9_]+)__c|^([A-Za-z]+)\.")


def extract_object_and_field(qualified_name: str) -> tuple[str, str] | None:
    """
    Best-effort parse of strings like 'Account.npe01__SYSTEM_AccountType__c' or
    'npsp__General_Accounting_Unit__c.Name' into (object_api_name, field_api_name).
    Returns None for rows that are prose ("n/a", "Not confirmed...", etc.) rather
    than a real API reference - those are skipped, not reported as failures.
    """
    if "." not in qualified_name:
        return None
    obj, _, fld = qualified_name.partition(".")
    obj = obj.strip()
    fld = fld.split("(")[0].strip()  # drop trailing "(...)" annotations
    if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", obj):
        return None
    if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", fld):
        return None
    return obj, fld


def check_reference(cache: DescribeCache, qualified_name: str) -> str:
    """Returns one of: 'ok', 'object_missing', 'field_missing', 'skipped'."""
    parsed = extract_object_and_field(qualified_name)
    if parsed is None:
        return "skipped"
    obj, fld = parsed
    fields = cache.field_names(obj)
    if fields is None:
        return "object_missing"
    if fld not in fields:
        return "field_missing"
    return "ok"


def load_all_entries() -> list[dict]:
    entries = []
    for yaml_path in sorted(FIELD_MAP_DIR.glob("*.yaml")):
        data = yaml.safe_load(yaml_path.read_text())
        for f in data.get("fields", []):
            f["_file"] = yaml_path.name
            entries.append(f)
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side", choices=["npsp", "npc", "both"], default="both")
    args = parser.parse_args()

    instance_url = os.environ.get("SF_INSTANCE_URL")
    access_token = os.environ.get("SF_ACCESS_TOKEN")
    if not instance_url or not access_token:
        print(
            "error: set SF_INSTANCE_URL and SF_ACCESS_TOKEN environment variables "
            "(see the docstring at the top of this file for how to get them).",
            file=sys.stderr,
        )
        return 2

    cache = DescribeCache(instance_url=instance_url.rstrip("/"), access_token=access_token)
    entries = load_all_entries()

    hard_failures = 0
    for e in entries:
        checks = []
        if args.side in ("npsp", "both"):
            checks.append(("npsp_field", e.get("npsp_field", "")))
        if args.side in ("npc", "both"):
            checks.append(("nonprofit_cloud_field", e.get("nonprofit_cloud_field", "")))

        for key, value in checks:
            status = check_reference(cache, value)
            if status == "skipped":
                continue
            confidence = e.get("confidence", "unconfirmed")
            marker = {
                "ok": "OK",
                "object_missing": "OBJECT NOT FOUND",
                "field_missing": "FIELD NOT FOUND",
            }[status]
            if status != "ok":
                print(f"[{marker}] {e['_file']} :: {key}={value} (confidence={confidence})")
                if confidence == "confirmed":
                    hard_failures += 1
            else:
                print(f"[OK] {e['_file']} :: {key}={value}")

    print()
    print(f"Done. {hard_failures} failure(s) on rows marked 'confirmed' in the map.")
    if hard_failures:
        print(
            "A 'confirmed' row failing against your org usually means either your org's API "
            "version differs from what this map assumes, or the map needs an update - please "
            "open an issue either way."
        )
    return 1 if hard_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
