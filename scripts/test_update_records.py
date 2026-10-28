import tempfile
import os
from pathlib import Path
import unittest
from unittest.mock import patch
from update_records import main, update_html, update_readme

class UpdateRecordsTests(unittest.TestCase):
    def test_updates_selected_page_and_escapes_actor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ['index.html', 'member1.html']:
                (root / name).write_text('<html><body>Original</body></html>')
            update_html(root, '<script>alert(1)</script>', 'Solo learner', '2026-10-28 UTC', 'abc1234', 'member1.html')
            self.assertNotIn('Updated by', (root / 'index.html').read_text())
            result = (root / 'member1.html').read_text()
            self.assertIn('&lt;script&gt;', result)
            self.assertNotIn('<script>', result)
            self.assertLess(result.index('Updated by'), result.index('</body>'))

    def test_invalid_page_does_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                update_html(Path(directory), 'actor', 'role', 'now', 'abc1234', '../other.txt')

    def test_readme_preserves_existing_content_and_records_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').write_text('# Original\n')
            update_readme(root, 'actor\nsecond-line', 'Solo learner', '2026-10-28 UTC', 'abc1234')
            text = (root / 'README.md').read_text()
            self.assertTrue(text.startswith('# Original\n'))
            self.assertIn('[Commit: abc1234]', text)
            self.assertIn('actor second-line', text)

    def test_unconfigured_actor_skips_both_steps_before_reading_git(self):
        with patch.dict(os.environ, {'GITHUB_ACTOR': 'another-account'}), patch('update_records.metadata') as read_metadata:
            for step in ['html', 'readme']:
                with patch('sys.argv', ['update_records.py', step]):
                    main()
            read_metadata.assert_not_called()

    def test_configured_actor_updates_only_the_configured_page_and_readme(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'index.html').write_text('<html><body>Original</body></html>')
            (root / 'member1.html').write_text('Unchanged member page')
            (root / 'README.md').write_text('# Original\n')
            with patch.dict(os.environ, {'GITHUB_ACTOR': 'Sakura-zz26'}), patch('update_records.Path', return_value=root), patch('update_records.metadata', return_value=('2026-10-29 UTC', 'abc1234')):
                for step in ['html', 'readme']:
                    with patch('sys.argv', ['update_records.py', step]):
                        main()
            self.assertIn('Updated by Sakura-zz26', (root / 'index.html').read_text())
            self.assertIn('[Commit: abc1234]', (root / 'README.md').read_text())
            self.assertEqual((root / 'member1.html').read_text(), 'Unchanged member page')

if __name__ == '__main__':
    unittest.main()
