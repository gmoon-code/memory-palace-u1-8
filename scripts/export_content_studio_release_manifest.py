from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REF = "cdf4bb2a1ea91415dd1634323ac5ab40ccba863f"


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def manifest(ref: str) -> dict:
    commit = git("rev-parse", f"{ref}^{{commit}}")
    tree = git("rev-parse", f"{commit}^{{tree}}")
    rows: list[dict[str, object]] = []
    raw = git("ls-tree", "-r", "-l", "--full-tree", commit)
    for line in raw.splitlines():
        metadata, path = line.split("\t", 1)
        mode, object_type, object_sha, size_text = metadata.split()
        size = None if size_text == "-" else int(size_text)
        rows.append(
            {
                "path": path,
                "mode": mode,
                "type": object_type,
                "git_object": object_sha,
                "size": size,
            }
        )
    rows.sort(key=lambda item: str(item["path"]))
    return {
        "schema": "story-method-content-studio-exact-git-manifest-1.0",
        "ref": ref,
        "commit": commit,
        "tree": tree,
        "file_count": len(rows),
        "files": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Expand the frozen Content Studio candidate into an exact tracked-file manifest.")
    parser.add_argument("--ref", default=DEFAULT_REF)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest(args.ref), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"CONTENT STUDIO EXACT MANIFEST WRITTEN: {output}")


if __name__ == "__main__":
    main()
