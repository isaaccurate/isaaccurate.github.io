import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('sync', Path(__file__).resolve().parents[1] / 'scripts/sync_obsidian.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)

class PublishingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.site = self.root / 'site'
        self.dest = self.site / '_knowledge'
        self.dest.mkdir(parents=True)
        self.vault = self.root / 'vault'
        (self.vault / 'Publish').mkdir(parents=True)
        (self.vault / 'PublishAssets').mkdir()
        self.cfg = self.root / 'config.yml'
        self.cfg.write_text('notes_dir: Publish\nassets_dir: PublishAssets\n')
        self.old_root, self.old_manifest = sync.ROOT, sync.MANIFEST
        sync.ROOT, sync.MANIFEST = self.site, self.site / '.obsidian-sync-manifest.json'
        self.addCleanup(self.restore)
    def restore(self):
        sync.ROOT, sync.MANIFEST = self.old_root, self.old_manifest
    def note(self, name, body='', publish='true', slug=None):
        (self.vault / 'Publish' / f'{name}.md').write_text(f'---\npublish: {publish}\nslug: {slug or name.lower()}\ntitle: {name}\ndescription: A useful note\ndate: 2026-10-30\ntags: [systems]\n---\n{body}')
    def run_sync(self, dry=False):
        sync.sync(self.vault, self.cfg, self.dest, dry)
    def test_opt_in_and_private_link_rejected_without_writes(self):
        self.note('Public', '[[Private]]')
        self.note('Private', publish='false')
        with self.assertRaises(ValueError): self.run_sync()
        self.assertEqual(list(self.dest.iterdir()), [])
    def test_wikilinks_and_referenced_assets_only(self):
        self.note('One', '[[Two|Read two]]\n![[chart.png|A chart]]')
        self.note('Two')
        (self.vault / 'PublishAssets/chart.png').write_bytes(b'image')
        (self.vault / 'PublishAssets/private.png').write_bytes(b'private')
        self.run_sync()
        self.assertIn("'/knowledge/two/' | relative_url", (self.dest / 'one.md').read_text())
        self.assertEqual(len(list((self.site / 'assets/notes').iterdir())), 1)
        self.assertNotIn('publish:', (self.dest / 'one.md').read_text())
    def test_unpublish_removes_generated_files(self):
        self.note('One')
        self.run_sync()
        self.note('One', publish='false')
        self.run_sync()
        self.assertFalse((self.dest / 'one.md').exists())
    def test_manual_edits_are_preserved(self):
        self.note('One')
        self.run_sync()
        (self.dest / 'one.md').write_text('manual edit')
        with self.assertRaises(ValueError): self.run_sync()
        self.assertEqual((self.dest / 'one.md').read_text(), 'manual edit')
    def test_attachment_traversal_and_symlink_blocked(self):
        self.note('One', '![[../secret.png|Secret]]')
        with self.assertRaises(ValueError): self.run_sync()
        (self.vault / 'PublishAssets/escape.png').symlink_to(self.root / 'secret.png')
        (self.root / 'secret.png').write_bytes(b'private')
        self.note('One', '![[escape.png|Secret]]')
        with self.assertRaises(ValueError): self.run_sync()
    def test_dry_run_writes_nothing(self):
        self.note('One')
        self.run_sync(True)
        self.assertFalse(sync.MANIFEST.exists())
        self.assertEqual(list(self.dest.iterdir()), [])
    def test_duplicate_slugs_and_ambiguous_links(self):
        self.note('One', slug='same')
        self.note('Two', slug='same')
        with self.assertRaises(ValueError): self.run_sync()
    def test_arbitrary_frontmatter_is_not_exported(self):
        self.note('One')
        source = self.vault / 'Publish/One.md'
        source.write_text(source.read_text().replace('publish: true', 'publish: true\npermalink: /private/\nsecret: do-not-export'))
        self.run_sync()
        self.assertNotIn('secret', (self.dest / 'one.md').read_text())
        self.assertNotIn('permalink', (self.dest / 'one.md').read_text())
    def test_comments_and_unapproved_links_fail(self):
        for body in ['%%private comment%%', '[private](../Secret.md)', '<!-- secret -->', '{{ site.secret }}']:
            self.note('One', body)
            with self.assertRaises(ValueError): self.run_sync()

if __name__ == '__main__':
    unittest.main()
