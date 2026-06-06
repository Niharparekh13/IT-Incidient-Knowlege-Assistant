import sqlite3
import tempfile
import unittest
import os
from pathlib import Path

from app import create_app
from app.ai_agent import recommend_solutions
from app.db import get_db
from app.ollama_client import build_prompt


class IncidentAssistantTestCase(unittest.TestCase):
    def setUp(self):
        self.original_ollama_enabled = os.environ.get("OLLAMA_ENABLED")
        os.environ["OLLAMA_ENABLED"] = "0"
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.sqlite"
        project_root = Path(__file__).resolve().parent.parent

        connection = sqlite3.connect(self.db_path)
        with connection:
            connection.executescript((project_root / "schema.sql").read_text())
            connection.executescript((project_root / "seed.sql").read_text())
        connection.close()

        self.app = create_app()
        self.app.config.update(TESTING=True, DATABASE=str(self.db_path))
        self.client = self.app.test_client()

    def tearDown(self):
        if self.original_ollama_enabled is None:
            os.environ.pop("OLLAMA_ENABLED", None)
        else:
            os.environ["OLLAMA_ENABLED"] = self.original_ollama_enabled
        self.temp_dir.cleanup()

    def test_homepage_and_management_pages_load(self):
        for path in ("/", "/knowledge", "/incidents", "/incidents/new", "/ai"):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)

    def test_ai_agent_recommends_wifi_solution(self):
        with self.app.app_context():
            results = recommend_solutions(get_db(), "wifi not connecting")

        self.assertGreaterEqual(len(results), 1)
        self.assertIn("Wi-Fi", results[0]["category_name"])
        self.assertGreater(results[0]["confidence_score"], 0)
        self.assertEqual(results[0]["ai_provider"], "Local scoring agent")

    def test_ollama_prompt_uses_issue_and_knowledge_base_match(self):
        entry = {
            "category_name": "Network and Wi-Fi",
            "title": "Cannot connect to Wi-Fi",
            "symptoms": "cannot connect wifi wireless network authentication failed",
            "resolution_steps": "Check that Wi-Fi is enabled and reconnect.",
            "escalation_required": 0,
        }
        prompt = build_prompt("wifi not connecting", entry)

        self.assertIn("wifi not connecting", prompt)
        self.assertIn("Cannot connect to Wi-Fi", prompt)
        self.assertIn("Use only the knowledge base", prompt)

    def test_search_save_incident_and_feedback_flow(self):
        search_response = self.client.post(
            "/search",
            data={"issue": "account locked after password attempts"},
        )
        self.assertEqual(search_response.status_code, 200)
        self.assertIn(b"AI confidence", search_response.data)

        save_response = self.client.post(
            "/incidents",
            data={
                "issue": "account locked after password attempts",
                "category_id": "1",
                "matched_kb_id": "1",
                "confidence_score": "0.82",
                "recommended_text": "AI test recommendation",
            },
            follow_redirects=True,
        )
        self.assertEqual(save_response.status_code, 200)

        incident_id = self.fetch_one("SELECT id FROM incidents ORDER BY id DESC")[0]
        detail_response = self.client.get(f"/incidents/{incident_id}")
        self.assertEqual(detail_response.status_code, 200)
        self.assertIn(b"AI test recommendation", detail_response.data)

        feedback_response = self.client.post(
            f"/incidents/{incident_id}/feedback",
            data={"is_helpful": "1", "comments": "Helpful for testing."},
            follow_redirects=True,
        )
        self.assertEqual(feedback_response.status_code, 200)
        self.assertEqual(self.fetch_one("SELECT COUNT(*) FROM feedback")[0], 1)

    def test_unknown_issue_gets_general_guidance(self):
        response = self.client.post(
            "/search",
            data={"issue": "webcam image is purple"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"General AI Guidance", response.data)
        self.assertIn(b"Local fallback guidance", response.data)

    def test_bluetooth_issue_gets_specific_knowledge_match(self):
        response = self.client.post(
            "/search",
            data={"issue": "bluetooth not working"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bluetooth device not connecting", response.data)
        self.assertIn(b"Best match", response.data)

    def test_knowledge_crud_flow(self):
        create_response = self.client.post(
            "/knowledge/new",
            data={
                "category_id": "2",
                "title": "VPN client cannot connect",
                "symptoms": "vpn client cannot connect network secure access",
                "resolution_steps": "Restart VPN, verify MFA, and reconnect.",
            },
            follow_redirects=True,
        )
        self.assertEqual(create_response.status_code, 200)

        entry_id = self.fetch_one(
            "SELECT id FROM knowledge_base WHERE title = ?",
            ("VPN client cannot connect",),
        )[0]

        update_response = self.client.post(
            f"/knowledge/{entry_id}/edit",
            data={
                "category_id": "2",
                "title": "VPN client cannot connect after MFA",
                "symptoms": "vpn client cannot connect mfa network secure access",
                "resolution_steps": "Restart VPN, confirm MFA, and reconnect.",
                "escalation_required": "on",
            },
            follow_redirects=True,
        )
        self.assertEqual(update_response.status_code, 200)

        delete_response = self.client.post(
            f"/knowledge/{entry_id}/delete",
            follow_redirects=True,
        )
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(
            self.fetch_one(
                "SELECT COUNT(*) FROM knowledge_base WHERE id = ?",
                (entry_id,),
            )[0],
            0,
        )

    def test_incident_update_and_delete_flow(self):
        self.client.post(
            "/incidents",
            data={
                "issue": "email is not syncing",
                "category_id": "4",
                "matched_kb_id": "6",
                "status": "new",
                "notes": "Initial incident.",
            },
            follow_redirects=True,
        )
        incident_id = self.fetch_one("SELECT id FROM incidents ORDER BY id DESC")[0]

        update_response = self.client.post(
            f"/incidents/{incident_id}/edit",
            data={
                "issue": "email is not syncing",
                "category_id": "4",
                "matched_kb_id": "6",
                "status": "resolved",
                "notes": "Resolved after restarting Outlook.",
            },
            follow_redirects=True,
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(
            self.fetch_one("SELECT status FROM incidents WHERE id = ?", (incident_id,))[0],
            "resolved",
        )

        delete_response = self.client.post(
            f"/incidents/{incident_id}/delete",
            follow_redirects=True,
        )
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(
            self.fetch_one("SELECT COUNT(*) FROM incidents WHERE id = ?", (incident_id,))[0],
            0,
        )

    def fetch_one(self, query, params=()):
        connection = sqlite3.connect(self.db_path)
        row = connection.execute(query, params).fetchone()
        connection.close()
        return row


if __name__ == "__main__":
    unittest.main()
