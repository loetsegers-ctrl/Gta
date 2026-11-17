import json
import re
import tempfile
import unittest
from pathlib import Path

from clipbot import kennis, web


class TestWeb(unittest.TestCase):
    def test_bouw(self):
        with tempfile.TemporaryDirectory() as d:
            pad = web.bouw(Path(d) / "x.html")
            html = pad.read_text(encoding="utf-8")
        self.assertNotIn("/*__DATA__*/", html)
        self.assertIn("<title>ClipBot GTA</title>", html)
        blob = re.search(r"const DATA = (\{.*?\});\n", html, re.S).group(1)
        data = json.loads(blob.replace("<\\/", "</"))
        self.assertEqual(len(data["stappenplan"]), len(kennis.STAPPENPLAN))
        self.assertEqual(set(data["onderwerpen"]), set(kennis.ONDERWERPEN))


if __name__ == "__main__":
    unittest.main()
