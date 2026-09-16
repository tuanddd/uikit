import argparse
import json
import re
import sys
from pathlib import Path

STEP_ID = re.compile(r"^step-(\d+)$")
KINDS = {"component", "variant", "detail", "guideline"}
PROPOSALS = {"promote", "one-off"}
STATUSES = {"open", "promoted", "folded", "one-off"}
CONFIDENCE = {"reference", "principle"}


def check(path):
    errors = []

    def err(msg):
        errors.append(msg)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"not valid JSON: {exc}"]
    if not isinstance(data, dict):
        return ["top level must be an object"]

    for key in ("feature", "slug", "group", "requirement", "drawnOn"):
        if not data.get(key):
            err(f"missing `{key}`")
    if not isinstance(data.get("frameWidth"), int):
        err("`frameWidth` must be an integer")
    requirement = data.get("requirement") or {}
    if not isinstance(requirement, dict) or not requirement.get("text") or not requirement.get("source"):
        err("`requirement` needs `text` and `source`")
    if data.get("slug") and data["slug"] != path.stem:
        err(f"`slug` ({data['slug']}) does not match the file name ({path.stem})")

    steps = data.get("steps")
    if not isinstance(steps, list) or not steps:
        err("`steps` must be a non-empty list")
        steps = []
    numbers, ids = set(), set()
    for step in steps:
        sid = step.get("id")
        match = STEP_ID.match(sid or "")
        if not match:
            err(f"step id `{sid}` must look like step-N")
        elif sid in ids:
            err(f"duplicate step id `{sid}`")
        else:
            ids.add(sid)
        if isinstance(step.get("n"), int):
            numbers.add(step["n"])
            if match and int(match.group(1)) != step["n"]:
                err(f"`{sid}` has number {step['n']}, which does not match its id")
        else:
            err(f"`{sid}` needs an integer `n`")
        for key in ("title",):
            if not step.get(key):
                err(f"`{sid}` needs `{key}`")
        linked = step.get("linkedTo")
        if linked is None:
            for key in ("state", "route", "restsOn"):
                if not step.get(key):
                    err(f"`{sid}` is drawn, so it needs `{key}`")
        elif not re.match(r"^[a-z0-9-]+#step-\d+$", str(linked)):
            err(f"`{sid}` linkedTo must be `<other-slug>#step-N`, or null")

    for i, row in enumerate(data.get("why") or []):
        if not row.get("decision") or not row.get("restsOn"):
            err(f"why[{i}] needs `decision` and `restsOn`")
        if row.get("confidence") not in CONFIDENCE:
            err(f"why[{i}] confidence must be one of {sorted(CONFIDENCE)}")

    for i, row in enumerate(data.get("components") or []):
        if not row.get("name") or not row.get("class"):
            err(f"components[{i}] needs `name` and `class`")
        source = row.get("from") or ""
        if not (source.startswith("src/") or source.startswith("candidate:") or source == "—"):
            err(f"components[{i}] `from` must be a src/ path, candidate:<Name>, or —")
        for token in re.split(r"[,\s]+", str(row.get("steps") or "")):
            if token.isdigit() and int(token) not in numbers:
                err(f"components[{i}] names step {token}, which is not a step")

    ledger = data.get("ledger")
    if not isinstance(ledger, list):
        err("`ledger` must be a list (empty when there is no drift)")
        ledger = []
    for i, row in enumerate(ledger):
        for key in ("name", "class", "nearest", "why"):
            if not row.get(key):
                err(f"ledger[{i}] needs `{key}`")
        if row.get("kind") not in KINDS:
            err(f"ledger[{i}] kind must be one of {sorted(KINDS)}")
        if row.get("proposal") not in PROPOSALS:
            err(f"ledger[{i}] proposal must be one of {sorted(PROPOSALS)}")
        if row.get("status") not in STATUSES:
            err(f"ledger[{i}] status must be one of {sorted(STATUSES)}")

    classes = {row.get("class") for row in data.get("components") or []}
    for i, row in enumerate(ledger):
        cls = row.get("class")
        if cls and cls != "—" and cls not in classes:
            err(f"ledger[{i}] class `{cls}` is not in the components table")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate flow definitions against the schema in FLOW-FILE.md.")
    parser.add_argument("flows_dir")
    args = parser.parse_args()

    flows = Path(args.flows_dir)
    paths = sorted(flows.glob("*.json"))
    if not paths:
        sys.exit(f"no flow definitions (*.json) in {flows}")

    failed = False
    for path in paths:
        errors = check(path)
        if errors:
            failed = True
            print(f"{path.name}: {len(errors)} problem(s)")
            for msg in errors:
                print(f"  - {msg}")
        else:
            print(f"{path.name}: ok")

    legacy = sorted(p.name for p in flows.glob("*.html"))
    if legacy:
        print(f"\n{len(legacy)} legacy HTML flow file(s), read by drift-report.py, not validated: {', '.join(legacy)}")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
