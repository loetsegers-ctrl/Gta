import unittest

from clipbot import maak_clip as mc


class TestMaakClip(unittest.TestCase):
    def test_tijd(self):
        self.assertEqual(mc.tijd_naar_sec("1:23:05"), 4985)
        self.assertEqual(mc.tijd_naar_sec("2:30"), 150)
        self.assertEqual(mc.tijd_naar_sec("12.5"), 12.5)
        with self.assertRaises(ValueError):
            mc.tijd_naar_sec("1:2:3:4")

    def test_emoji_weg(self):
        self.assertEqual(mc._zonder_emoji("Wacht tot het einde 😭 echt"), "Wacht tot het einde echt")

    def test_hoogtepunt_gevonden(self):
        # 180 s rustig (-30 LUFS) met een luid stuk op 100-125 s
        luid = [-30.0] * 180
        for i in range(100, 125):
            luid[i] = -12.0
        top = mc.vind_hoogtepunten(luid, duur=25, aantal=3)
        self.assertEqual(top[0][0], 100)
        starts = [s for s, _ in top]
        for a in starts:
            for b in starts:
                if a != b:
                    self.assertGreaterEqual(abs(a - b), 25)

    def test_hoogtepunt_leeg(self):
        self.assertEqual(mc.vind_hoogtepunten([]), [])

    def test_fmt(self):
        self.assertEqual(mc._fmt(4985), "1:23:05")

    def test_filter(self):
        f = mc.ffmpeg_filter("/x/hook.txt", "/x/credit.txt")
        self.assertIn("1080:1920", f)
        self.assertIn("textfile=/x/hook.txt", f)
        self.assertTrue(f.endswith("[v]"))


if __name__ == "__main__":
    unittest.main()
