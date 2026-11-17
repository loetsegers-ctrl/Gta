import unittest

from clipbot import bot, kennis


class TestZoeken(unittest.TestCase):
    def test_download_vraag(self):
        r = bot.zoek("hoe kan ik een twitch vod downloaden?")
        self.assertEqual(r[0]["titel"], kennis.ONDERWERPEN["content_halen"]["titel"])

    def test_platform_vraag(self):
        r = bot.zoek("op welke site meld ik me aan, whop of vyro?")
        self.assertEqual(r[0]["titel"], kennis.ONDERWERPEN["platformen"]["titel"])

    def test_accenten(self):
        self.assertTrue(bot.zoek("content kopiëren en plakken"))

    def test_afwijzing(self):
        r = bot.zoek("mijn clip is afgewezen")
        self.assertEqual(r[0]["titel"], kennis.ONDERWERPEN["regels_afwijzing"]["titel"])

    def test_onbekend(self):
        self.assertIn("geen specifiek antwoord", bot.beantwoord("pizza recept"))


class TestCalculator(unittest.TestCase):
    def test_verdiensten(self):
        self.assertEqual(bot.bereken_verdiensten(100_000, 1.5), 135.0)

    def test_views_nodig(self):
        self.assertEqual(bot.views_nodig(135, 1.5), 100_000)

    def test_ongeldig(self):
        with self.assertRaises(ValueError):
            bot.views_nodig(100, 0)


class TestWeergave(unittest.TestCase):
    def test_stappenplan(self):
        t = bot.stappenplan_tekst()
        self.assertIn("A. ", t)
        self.assertEqual(len(kennis.STAPPENPLAN), 14)

    def test_menu_loopt(self):
        antwoorden = iter(["1", "", "11", "10000", "2", "1.5", "300", "", "13", "tiktok account", "", "0"])
        uit = []
        bot.menu(invoer=lambda _p="": next(antwoorden), uitvoer=uit.append)
        alles = "\n".join(uit)
        self.assertIn("STAPPENPLAN", alles)
        self.assertIn("Per maand", alles)
        self.assertIn("Succes met clippen", alles)

    def test_kennis_tekst(self):
        self.assertIn("Stappenplan A-Z", kennis.volledige_kennis_als_tekst())


if __name__ == "__main__":
    unittest.main()
