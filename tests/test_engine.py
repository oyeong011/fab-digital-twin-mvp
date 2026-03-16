import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from fastapi.testclient import TestClient

from fab_sim.anomaly import detect_anomalies
from fab_sim.decision import recommend_actions
from fab_sim.app import generate_snapshot, save_outputs
from fab_sim.api import app


class FabEngineTests(unittest.TestCase):
    def setUp(self):
        self.states = [{
            "tool_id": "EQP-99",
            "process_step": "etch",
            "temperature": 95.0,
            "pressure": 1.9,
            "vibration": 0.36,
            "throughput_wph": 27.0,
            "defect_rate": 0.061,
            "queue_size": 24,
            "utilization": 0.51,
            "health_score": 41.0,
            "timestamp": "2026-03-16T00:00:00Z",
        }]
        self.client = TestClient(app)

    def test_critical_anomaly_detection(self):
        anomalies = detect_anomalies(self.states)
        self.assertEqual(anomalies[0]["severity"], "critical")
        self.assertIn("health_score", anomalies[0]["triggered_metrics"])

    def test_recommend_maintenance_for_critical_tool(self):
        anomalies = detect_anomalies(self.states)
        actions = recommend_actions(self.states, anomalies)
        self.assertEqual(actions[0]["recommended_action"], "maintenance")

    def test_snapshot_generation_tool_count(self):
        snapshot = generate_snapshot(seed=7, n_tools=12, fab_name="fab-beta")
        self.assertEqual(snapshot["fab_name"], "fab-beta")
        self.assertEqual(len(snapshot["tools"]), 12)

    def test_save_outputs_writes_csv(self):
        snapshot = generate_snapshot(seed=5, n_tools=6, fab_name="fab-delta")
        out_dir = ROOT / "tmp_test_output"
        save_outputs(snapshot, out_dir)
        self.assertTrue((out_dir / "snapshot.json").exists())
        self.assertTrue((out_dir / "events.jsonl").exists())
        self.assertTrue((out_dir / "tools.csv").exists())
        self.assertTrue((out_dir / "dashboard.html").exists())

    def test_api_snapshot_endpoint(self):
        response = self.client.get("/api/snapshot", params={"seed": 7, "tools": 12, "fab_name": "fab-beta"})
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("summary", body)
        self.assertEqual(body["snapshot"]["fab_name"], "fab-beta")
        self.assertEqual(len(body["snapshot"]["tools"]), 12)

    def test_api_events_endpoint(self):
        response = self.client.get("/api/events", params={"seed": 3, "tools": 5, "fab_name": "fab-zeta"})
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(len(body["events"]), 5)
        self.assertIn("recommended_action", body["events"][0])


if __name__ == "__main__":
    unittest.main()
