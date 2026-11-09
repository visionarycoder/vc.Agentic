#!/usr/bin/env python3
"""Validate the extended skill frontmatter profile without changing files."""
import argparse
import json
from pathlib import Path

from skills import Library


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    library = Library(args.root)
    errors = library.validate_frontmatter()
    print(json.dumps({'skills': len(library.entrypoints()), 'errors': errors}, indent=2))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
