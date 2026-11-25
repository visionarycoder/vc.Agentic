import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import agent_entry


class AgentEntryTests(unittest.TestCase):
    def test_extracts_only_start_here_section(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'AGENTS.md').write_text('# T\n\n## Start here\n\nGo here.\n\n## Other\n\nNo.\n', encoding='utf-8')
            text = agent_entry.entry_text(root)
        self.assertIn('Go here.', text)
        self.assertNotIn('No.', text)

    def test_falls_back_without_section(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertIn('AGENTS.md', agent_entry.entry_text(Path(folder)))

    def test_repository_entry_names_discovery_guide(self):
        self.assertIn('skill-discovery-guide', agent_entry.entry_text())


if __name__ == '__main__':
    unittest.main()
