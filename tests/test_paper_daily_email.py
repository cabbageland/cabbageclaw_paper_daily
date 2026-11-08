import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("paper_daily_email", ROOT / "paper_daily_email.py")
email = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(email)


class PaperEmailCompatibilityTests(unittest.TestCase):
    def load_digest(self, day):
        digest = email.parse_digest(ROOT / "daily_papers" / f"{day}.md")
        items = email.build_items(digest)
        email.validate_digest_structure(digest, items)
        return digest, items

    def test_current_digest_includes_lighter_picks_without_claiming_full_notes(self):
        digest, items = self.load_digest("2026-11-07")
        self.assertEqual(len(items), 5)
        self.assertEqual(sum(bool(item["notes_path"]) for item in items), 2)
        self.assertEqual(items[1]["paper_url"], "https://arxiv.org/abs/2611.08240")
        self.assertIn("single run", items[1]["body"])
        self.assertIn("no detailed note", items[1]["notes_label"])
        self.assertEqual(items[1]["notes_url"], email.public_app_route(digest["digest_path"]))

    def test_legacy_why_it_matters_digest_remains_valid(self):
        _, items = self.load_digest("2026-10-13")
        self.assertEqual(len(items), 5)
        self.assertTrue(all(item["notes_path"] for item in items))

    def test_missing_source_for_a_lighter_pick_blocks_email(self):
        digest = email.parse_digest(ROOT / "daily_papers" / "2026-11-07.md")
        digest["ranked_details"][digest["ranked_titles"][1]].pop("source")
        with self.assertRaisesRegex(ValueError, "Missing paper link"):
            email.build_items(digest)

    def test_missing_mechanism_and_why_still_blocks_email(self):
        digest = email.parse_digest(ROOT / "daily_papers" / "2026-11-07.md")
        digest["ranked_details"][digest["ranked_titles"][1]].pop("mechanism")
        with self.assertRaisesRegex(ValueError, "missing Why it matters"):
            email.validate_digest_structure(digest, email.build_items(digest))

    def test_mixed_digest_renders_private_redacted_messages(self):
        digest, items = self.load_digest("2026-11-07")
        recipients = ["first@example.invalid", "second@example.invalid"]
        with patch.object(email, "smtp_settings", return_value=("localhost", 465, "sender@example.invalid", "unused")):
            messages = [email.build_message(digest, items, recipient) for recipient in recipients]
        for message in messages:
            email.validate_rendered_message(message, [message["To"]], expected_item_count=5)
        email.validate_recipient_privacy(messages, recipients)
        preview = email.serialized_redacted_messages(messages)
        self.assertIsNone(email.EMAIL_RE.search(preview))


if __name__ == "__main__":
    unittest.main()
