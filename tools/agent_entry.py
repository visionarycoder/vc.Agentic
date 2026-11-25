"""Print the repository entry point for agent harness session-start hooks."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HEADING = '## Start here'


def entry_text(root: Path = ROOT) -> str:
    try:
        text = (root / 'AGENTS.md').read_text(encoding='utf-8')
    except OSError:
        return 'vc.Agentic: read AGENTS.md at the repository root for the entry point.'
    match = re.search(r'^' + re.escape(HEADING) + r'\n+(.*?)(?=^## |\Z)', text, re.M | re.S)
    if not match:
        return 'vc.Agentic: read AGENTS.md at the repository root for the entry point.'
    return 'vc.Agentic entry point (from AGENTS.md):\n\n' + match.group(1).strip()


if __name__ == '__main__':
    print(entry_text())
