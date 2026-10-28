import tempfile
from pathlib import Path
import unittest
from update_records import update_html, update_readme

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

if __name__ == '__main__':
    unittest.main()
