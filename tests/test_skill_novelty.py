from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest

SCRIPT = Path(__file__).parents[1] / '.agents/skills/skill-novelty-audit/scripts/novelty.py'
spec = spec_from_file_location('novelty', SCRIPT)
novelty = module_from_spec(spec)
spec.loader.exec_module(novelty)

SKILL = '''---
name: "x"
---

# X

A cache is a store that helps to improve performance in general.

- Set the retry ceiling to 5 attempts in `config/retry.json`.

```text
run --limit 30
```
'''


class NoveltyTests(unittest.TestCase):
    def test_decompose_skips_frontmatter_and_splits_kinds(self):
        items = novelty.decompose(SKILL)
        self.assertEqual(['prose', 'list', 'code'], [i['kind'] for i in items])

    def test_classify_separates_generic_from_specific(self):
        prose, listed, code = novelty.decompose(SKILL)
        self.assertEqual('generic', novelty.classify(prose))
        self.assertEqual('specific', novelty.classify(listed))
        self.assertEqual('specific', novelty.classify(code))

    def test_quadrants_follow_grading_strictness(self):
        g = novelty.GRADES
        self.assertEqual('novel', novelty.quadrant(g['wrong'], g['correct'], 1))
        self.assertEqual('harmful', novelty.quadrant(g['correct'], g['wrong'], 2))
        self.assertEqual('already-known', novelty.quadrant(g['concept'], g['concept'], 1))
        self.assertEqual('missed', novelty.quadrant(g['concept'], g['concept'], 2))


if __name__ == '__main__':
    unittest.main()
