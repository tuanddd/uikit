import argparse
import json
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


def drift_rows(path):
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


def main():
    parser = argparse.ArgumentParser(description="Tally drift from the design system across flow files.")
    parser.add_argument("flows_dir")
    parser.add_argument("--all", action="store_true", help="include reviewed drift, not only open rows")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    tally = {}
    for path in sorted(Path(args.flows_dir).glob("*.html")):
        for row in drift_rows(path):
            key = row["class"] if row["class"] not in ("", "—") else row["name"]
            entry = tally.setdefault(key, {"name": row["name"], "class": row["class"], "kinds": set(), "proposals": set(), "statuses": set(), "files": []})
            entry["kinds"].add(row["kind"])
            entry["proposals"].add(row["proposal"])
            entry["statuses"].add(row["status"])
            if path.name not in entry["files"]:
                entry["files"].append(path.name)

    entries = [e for e in tally.values() if args.all or "open" in e["statuses"]]
    entries.sort(key=lambda e: (-len(e["files"]), e["name"].lower()))

    if args.json:
        print(json.dumps([{**e, "kinds": sorted(e["kinds"]), "proposals": sorted(e["proposals"]), "statuses": sorted(e["statuses"])} for e in entries], indent=2, ensure_ascii=False))
        return

    print("| Drift | Class | Kind | Files | Proposal | Status | Used in |")
    print("|---|---|---|---|---|---|---|")
    for e in entries:
        print(f"| {e['name']} | `{e['class']}` | {', '.join(sorted(e['kinds']))} | {len(e['files'])} | {', '.join(sorted(e['proposals']))} | {', '.join(sorted(e['statuses']))} | {', '.join(e['files'])} |")
    shared = sum(1 for e in entries if len(e["files"]) > 1)
    print(f"\n{len(entries)} drift(s); {shared} used by two or more flow files")


if __name__ == "__main__":
    main()
