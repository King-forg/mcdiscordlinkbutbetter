import unittest

from mcdiscordlinkbutbetter import BotService


class BotServiceTests(unittest.TestCase):
    def test_link_then_profile(self) -> None:
        service = BotService()
        self.assertEqual(
            service.run_command("link", "u123", "Alex"),
            "Linked u123 to Alex.",
        )
        self.assertEqual(service.run_command("profile", "u123"), "u123 is linked to Alex.")

    def test_unlink_missing_user(self) -> None:
        service = BotService()
        self.assertEqual(
            service.run_command("unlink", "u404"),
            "No linked Minecraft account found for u404.",
        )

    def test_advanced_linkchannel_command(self) -> None:
        service = BotService()
        self.assertEqual(
            service.run_command("linkchannel", "guild-1", "channel-9"),
            "Guild guild-1 linked to channel channel-9.",
        )

    def test_unknown_command(self) -> None:
        service = BotService()
        self.assertIn("Unknown command", service.run_command("ping"))


if __name__ == "__main__":
    unittest.main()
