import argparse
import json
import sys
from html.parser import HTMLParser
from pathlib import Path


class Tables(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables = []
        self.open = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.open.append([])
        elif tag == "tr" and self.open:
            self.row = {"attrs": dict(attrs), "cells": [], "head": False}
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []
            self.row["head"] = self.row["head"] or tag == "th"

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None and self.row is not None:
            self.row["cells"].append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None and self.open:
            self.open[-1].append(self.row)
            self.row = None
        elif tag == "table" and self.open:
            self.tables.append(self.open.pop())

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)


def html_rows(path):
    """Legacy flow files: the ledger table, or the components table's Proposed rows."""
    parser = Tables()
    parser.feed(path.read_text(encoding="utf-8"))
    ledger, legacy = [], []
    for table in parser.tables:
        for row in table:
            attrs = row["attrs"]
            if "data-drift" in attrs:
                ledger.append({
                    "name": attrs["data-drift"],
                    "class": attrs.get("data-class") or "—",
                    "kind": attrs.get("data-kind") or "component",
                    "proposal": attrs.get("data-proposal") or "—",
                    "status": attrs.get("data-status") or "open",
                })
        head = next((row["cells"] for row in table if row["head"]), [])
        if "Component" not in head or "From" not in head:
            continue
        name_at, from_at = head.index("Component"), head.index("From")
        class_at = head.index("Class") if "Class" in head else None
        for row in table:
            cells = row["cells"]
            if row["head"] or len(cells) <= from_at or not cells[from_at].startswith("Proposed"):
                continue
            legacy.append({
                "name": cells[name_at],
                "class": cells[class_at] if class_at is not None and len(cells) > class_at else "—",
                "kind": "component",
                "proposal": "—",
                "status": "open",
            })
    return ledger or legacy


def json_rows(path):
    """Flow definitions: the ledger array; rows carry name, class, kind, proposal, status."""
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for row in data.get("ledger", []):
        rows.append({
            "name": row.get("name") or "—",
            "class": row.get("class") or "—",
            "kind": row.get("kind") or "component",
            "proposal": row.get("proposal") or "—",
            "status": row.get("status") or "open",
        })
    return rows


def drift_rows(path):
    return json_rows(path) if path.suffix == ".json" else html_rows(path)


def main():
    parser = argparse.ArgumentParser(description="Tally drift from the design system across flow definitions and legacy flow files.")
    parser.add_argument("flows_dir")
    parser.add_argument("--all", action="store_true", help="include reviewed drift, not only open rows")
    parser.add_argument("--file", action="append", default=[], help="only drift used by this flow (a .json definition or a legacy .html file), still counting every flow that uses it; repeat for several")
    parser.add_argument("--new", action="store_true", help="with --file: only new drift, open in a named flow and open in at most one other flow, or an open guideline")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.new and not args.file:
        parser.error("--new needs at least one --file")

    flows = Path(args.flows_dir)
    paths = sorted([*flows.glob("*.json"), *flows.glob("*.html")])
    names = {path.name for path in paths}
    scope, unknown = set(), []
    for given in args.file:
        path = Path(given)
        inside = path.parent == Path(".") or path.resolve().parent == flows.resolve()
        if inside and path.name in names:
            scope.add(path.name)
        else:
            unknown.append(given)
    if unknown:
        sys.exit(f"not a flow in {args.flows_dir}: {', '.join(unknown)}")

    tally = {}
    for path in paths:
        for row in drift_rows(path):
            key = row["class"] if row["class"] not in ("", "—") else row["name"]
            entry = tally.setdefault(key, {"name": row["name"], "class": row["class"], "kinds": set(), "proposals": set(), "statuses": set(), "files": [], "open_in": [], "guidelines_open": []})
            entry["kinds"].add(row["kind"])
            entry["proposals"].add(row["proposal"])
            entry["statuses"].add(row["status"])
            if path.name not in entry["files"]:
                entry["files"].append(path.name)
            if row["status"] == "open" and path.name not in entry["open_in"]:
                entry["open_in"].append(path.name)
            if row["kind"] == "guideline" and row["status"] == "open" and path.name not in entry["guidelines_open"]:
                entry["guidelines_open"].append(path.name)

    def is_new(entry):
        open_in = set(entry["open_in"])
        return bool(scope & open_in) and (bool(scope & set(entry["guidelines_open"])) or len(open_in - scope) <= 1)

    entries = [
        e for e in tally.values()
        if (args.all or "open" in e["statuses"])
        and (not scope or scope & set(e["files"]))
        and (not args.new or is_new(e))
    ]
    entries.sort(key=lambda e: (-len(e["files"]), e["name"].lower()))

    if args.json:
        out = []
        for e in entries:
            row = {k: v for k, v in e.items() if k != "guidelines_open"}
            row.update(kinds=sorted(e["kinds"]), proposals=sorted(e["proposals"]), statuses=sorted(e["statuses"]))
            out.append(row)
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    print("| Drift | Class | Kind | Flows | Proposal | Status | Used in |")
    print("|---|---|---|---|---|---|---|")
    for e in entries:
        print(f"| {e['name']} | `{e['class']}` | {', '.join(sorted(e['kinds']))} | {len(e['files'])} | {', '.join(sorted(e['proposals']))} | {', '.join(sorted(e['statuses']))} | {', '.join(e['files'])} |")
    shared = sum(1 for e in entries if len(e["files"]) > 1)
    print(f"\n{len(entries)} drift(s); {shared} used by two or more flows")


if __name__ == "__main__":
    main()
