from pathlib import Path
import tempfile
import unittest

from tools.skills import Library, META, parse, render


class SkillMaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'tools').mkdir()
        (self.root / 'tools/README.md').write_text('# Maintenance\n', encoding='utf-8', newline='\n')
        self.library = Library(self.root, '2026-11-08')

    def new(self, name='example-skill', collection='optional'):
        self.library.new(name, 'Perform a bounded example task.', collection, apply=True)
        return self.library.skills / name / 'SKILL.md'

    def test_scaffold_uses_supported_extended_metadata(self):
        path = self.new()
        data, _ = parse(path.read_text())
        self.assertEqual({'name', 'description', 'metadata'}, set(data))
        self.assertEqual(set(META), set(data['metadata']))
        self.assertEqual([], self.library.validate())

    def test_duplicate_header_fields_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate field'):
            parse('---\nname: "a"\nname: "b"\n---\n\n# Test\n')

    def test_nonstring_metadata_and_ambiguous_yaml_are_rejected(self):
        for value in ['true', '20261108', 'unquoted']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse('---\nname: "a"\nmetadata:\n  updated: ' + value + '\n---\n\n# Test\n')

    def test_missing_metadata_and_bad_date_are_reported(self):
        path = self.new()
        data, body = parse(path.read_text())
        data['metadata']['updated'] = '2026-99-88'
        path.write_text(render(data, body))
        self.assertTrue(self.library.validate_frontmatter())
        data['metadata'].pop('collection')
        path.write_text(render(data, body))
        self.assertIn('Missing metadata', self.library.validate_frontmatter()[0])

    def test_normalization_preflights_and_is_idempotent(self):
        folder = self.library.skills / 'legacy'
        folder.mkdir(parents=True)
        path = folder / 'SKILL.md'
        path.write_text('---\nname: "legacy"\ndescription: "Legacy example."\nmetadata:\n  last_updated: "2026-01-01"\n---\n\nExisting guidance.\n')
        original = path.read_bytes()
        self.assertEqual(1, len(self.library.normalize()))
        self.assertEqual(original, path.read_bytes())
        self.library.normalize(apply=True)
        self.assertEqual([], self.library.normalize())
        self.assertEqual([], self.library.validate_frontmatter())

    def test_normalization_never_changes_license_text(self):
        path = self.new()
        license_file = path.parent / 'LICENSE'
        original = b'Third-party terms\r\nRemain unchanged.\r\n'
        license_file.write_bytes(original)
        self.library.normalize(apply=True)
        self.assertEqual(original, license_file.read_bytes())

    def test_normalization_does_not_partially_write_when_a_later_header_is_invalid(self):
        path = self.new('a-valid')
        data, body = parse(path.read_text())
        data['metadata']['updated'] = '2026-01-01'
        path.write_text(render(data, body), encoding='utf-8', newline='\n')
        original = path.read_bytes()
        invalid = self.library.skills / 'z-invalid'
        invalid.mkdir()
        (invalid / 'SKILL.md').write_text('Missing frontmatter\n')
        with self.assertRaises(ValueError):
            self.library.normalize(apply=True)
        self.assertEqual(original, path.read_bytes())

    def test_rename_updates_references_and_inventory(self):
        self.new('old-skill')
        self.root.joinpath('README.md').write_text('[Skill](.agents/skills/old-skill/SKILL.md)\n')
        preview = self.library.rename('old-skill', 'new-skill')
        self.assertIn('from', preview)
        self.assertTrue((self.library.skills / 'old-skill').exists())
        self.library.rename('old-skill', 'new-skill', apply=True)
        self.assertIn('skills/new-skill/', self.root.joinpath('README.md').read_text())
        self.assertFalse((self.library.skills / 'old-skill').exists())
        self.assertEqual([], self.library.validate())

    def test_remove_is_bounded_and_refresh_does_not_restore_deleted_skills(self):
        self.new('keep-me')
        self.new('remove-me')
        self.root.joinpath('README.md').write_text('[Removed](.agents/skills/remove-me/SKILL.md)\n')
        for name in ['../outside', '..', '/absolute', 'UPPER']:
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.library.remove([name], apply=True)
        self.library.remove(['remove-me'], apply=True)
        self.library.refresh()
        self.assertEqual(['keep-me'], [row['name'] for row in self.library.rows()])
        self.assertFalse((self.library.skills / 'remove-me').exists())
        self.assertEqual('Removed\n', self.root.joinpath('README.md').read_text())

    def test_rename_preserves_third_party_license_bytes(self):
        path = self.new('old-skill')
        notice = path.parent / 'LICENSE.txt'
        original = b'Copyright old-skill contributors\r\nOriginal terms.\r\n'
        notice.write_bytes(original)
        self.library.rename('old-skill', 'new-skill', apply=True)
        self.assertEqual(original, (self.library.skills / 'new-skill/LICENSE.txt').read_bytes())

    def test_rename_rejects_an_invalid_source_header_before_moving(self):
        path = self.new('old-skill')
        path.write_text('Invalid header\n')
        with self.assertRaises(ValueError):
            self.library.rename('old-skill', 'new-skill', apply=True)
        self.assertTrue(path.exists())
        self.assertFalse((self.library.skills / 'new-skill').exists())

    def test_link_cleanup_preserves_fenced_examples_and_external_urls(self):
        self.new()
        path = self.root / 'README.md'
        original = '[Gone](gone.md)\n[Web](https://example.org)\n\n```markdown\n[Example](missing.md)\n```\n'
        path.write_text(original)
        self.assertEqual(1, len(self.library.fix_links()))
        self.assertEqual(original, path.read_text())
        self.library.fix_links(apply=True)
        self.assertTrue(path.read_text().startswith('Gone\n[Web]'))
        self.assertIn('[Example](missing.md)', path.read_text())

    def test_stale_inventory_and_resource_count_are_detected(self):
        path = self.new()
        (path.parent / 'reference.txt').write_text('New required resource\n')
        self.assertIn('Inventory is stale', '\n'.join(self.library.validate()))
        self.library.refresh()
        self.assertEqual([], self.library.validate())

    def test_generated_inventory_uses_portable_lf_line_endings(self):
        self.new()
        inventory = self.root / '.agents/inventory.csv'
        self.assertNotIn(b'\r', inventory.read_bytes())

    def test_overlap_candidates_do_not_remove_distinct_skills(self):
        self.new('one')
        self.new('two')
        report = self.library.audit()
        self.assertEqual(1, len(report['review_candidates']))
        self.assertEqual(2, len(self.library.entrypoints()))

    def test_new_and_remove_reject_existing_or_duplicate_targets(self):
        self.new()
        with self.assertRaises(ValueError):
            self.new()
        with self.assertRaises(ValueError):
            self.library.remove(['example-skill', 'example-skill'], apply=True)
        self.assertTrue((self.library.skills / 'example-skill').is_dir())


if __name__ == '__main__':
    unittest.main()
