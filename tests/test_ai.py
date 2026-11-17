import os
import unittest
from types import SimpleNamespace
from unittest import mock

from clipbot import bot


class NepStream:
    def __init__(self, kwargs):
        self.kwargs = kwargs
        self.text_stream = iter(["Meld je ", "aan op Whop."])

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def get_final_message(self):
        return SimpleNamespace(stop_reason="end_turn",
                               content=[SimpleNamespace(type="text", text="Meld je aan op Whop.")])


class TestAIChat(unittest.TestCase):
    def test_chat_loop(self):
        try:
            import anthropic
        except ImportError:
            self.skipTest("anthropic niet geinstalleerd")
        aanroepen = []

        class NepClient:
            def __init__(self):
                self.beta = SimpleNamespace(messages=SimpleNamespace(stream=self._stream))

            def _stream(self, **kwargs):
                aanroepen.append({**kwargs, "messages": list(kwargs["messages"])})
                return NepStream(kwargs)

        vragen = iter(["waar begin ik?", "en daarna?", "stop"])
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test"}), \
             mock.patch.object(anthropic, "Anthropic", NepClient):
            bot.ai_chat(invoer=lambda _p="": next(vragen), uitvoer=lambda *_: None)

        self.assertEqual(len(aanroepen), 2)
        eerste = aanroepen[0]
        self.assertEqual(eerste["model"], "claude-opus-5-5")
        self.assertIn("Stappenplan A-Z", eerste["system"])
        self.assertEqual(eerste["fallbacks"], "default")
        # tweede beurt bevat de volledige geschiedenis
        rollen = [m["role"] for m in aanroepen[1]["messages"]]
        self.assertEqual(rollen, ["user", "assistant", "user"])

    def test_zonder_sleutel(self):
        uit = []
        with mock.patch.dict(os.environ, {}, clear=True):
            bot.ai_chat(invoer=lambda _p="": "stop", uitvoer=uit.append)
        self.assertTrue(any("API" in u or "pip" in u for u in uit))


if __name__ == "__main__":
    unittest.main()
