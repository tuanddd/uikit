import argparse
import re
import sys
from pathlib import Path

LOCAL = "flow-local"
BLOCK = re.compile(r'<style id="([^"]+)">.*?</style>', re.S)


def blocks(text):
    return {m.group(1): m.group(0) for m in BLOCK.finditer(text)}


def main():
    parser = argparse.ArgumentParser(
        description="Copy shared <style id> blocks from one flow file into every other flow file."
    )
    parser.add_argument("flows_dir")
    parser.add_argument("--from", dest="source", required=True, help="the flow file whose blocks are current")
    parser.add_argument("--block", action="append", default=[], help="block id to sync; repeat; default: every block except flow-local")
    parser.add_argument("--check", action="store_true", help="report differences and exit 1, write nothing")
    args = parser.parse_args()

    source = Path(args.source)
    wanted = blocks(source.read_text(encoding="utf-8"))
    names = args.block or [name for name in wanted if name != LOCAL]
    unknown = [name for name in names if name not in wanted]
    if unknown:
        sys.exit(f"{source}: no <style id> block named {', '.join(unknown)}")

    problems, changed = [], []
    for path in sorted(Path(args.flows_dir).glob("*.html")):
        if path.resolve() == source.resolve():
            continue
        text = path.read_text(encoding="utf-8")
        have = blocks(text)
        updated = text
        for name in names:
            if name not in have:
                problems.append(f"{path.name}: missing block {name}")
            elif have[name] != wanted[name]:
                if args.check:
                    problems.append(f"{path.name}: block {name} differs")
                else:
                    updated = updated.replace(have[name], wanted[name], 1)
        if not args.check and updated != text:
            path.write_text(updated, encoding="utf-8")
            changed.append(path.name)

    for line in problems:
        print(line)
    if args.check:
        print(f"{len(problems)} difference(s) in {', '.join(names)}" if problems else f"in sync: {', '.join(names)}")
    else:
        print(f"updated {len(changed)} file(s){': ' + ', '.join(changed) if changed else ''}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
