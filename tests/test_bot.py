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
        antwoorden = iter(["1", "", "15", "10000", "2", "1.5", "300", "", "19", "tiktok account", "", "16", "2", "8000", "50", "65", "100", "", "17", "Lysium", "", "", "0"])
        uit = []
        bot.menu(invoer=lambda _p="": next(antwoorden), uitvoer=uit.append)
        alles = "\n".join(uit)
        self.assertIn("STAPPENPLAN", alles)
        self.assertIn("Per maand", alles)
        self.assertIn("Succes met clippen", alles)
        self.assertIn("Score:", alles)
        self.assertIn("HOOK-IDEE", alles)

    def test_kennis_tekst(self):
        self.assertIn("Stappenplan A-Z", kennis.volledige_kennis_als_tekst())


if __name__ == "__main__":
    unittest.main()


class TestNieuweFuncties(unittest.TestCase):
    def test_score_voorbeeld(self):
        # $2 CPM, 65%, $8000 moet beter scoren dan $4 CPM, 10%, $200 (zelfde aantal clippers)
        self.assertGreater(bot.campagne_score(2, 8000, 50, 65), bot.campagne_score(4, 200, 50, 10))

    def test_advies_cap(self):
        t = bot.campagne_advies(2, 8000, 50, 65, cap=5, verwachte_views=100_000)
        self.assertIn("Cap bereikt", t)

    def test_advies_klein_budget(self):
        self.assertIn("klein resterend budget", bot.campagne_advies(4, 200, 50, 10))

    def test_hooks(self):
        t = bot.hooks_en_caption("Lysium")
        self.assertIn("Lysium had dit NOOIT", t)
        self.assertIn("#lysium", t)

    def test_gta6_zoeken(self):
        r = bot.zoek("wanneer komt gta 6 uit?")
        self.assertEqual(r[0]["titel"], kennis.ONDERWERPEN["gta6_kans"]["titel"])

    def test_scam_zoeken(self):
        r = bot.zoek("is deze discord cursus een scam?")
        self.assertEqual(r[0]["titel"], kennis.ONDERWERPEN["scams"]["titel"])


class TestExport(unittest.TestCase):
    def test_markdown(self):
        md = bot.markdown_export()
        self.assertIn("**A. Begrijp het model**", md)
        self.assertIn("**N. Opschalen**", md)
        for o in kennis.ONDERWERPEN.values():
            self.assertIn(f"## {o['titel']}", md)
        self.assertNotIn("{streamer}", md)
