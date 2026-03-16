import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from fab_sim.anomaly import detect_anomalies
from fab_sim.decision import recommend_actions
from fab_sim.app import generate_snapshot


def test_critical_anomaly_detection():
    states = [{
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
    anomalies = detect_anomalies(states)
    assert anomalies[0]["severity"] == "critical"
    assert "health_score" in anomalies[0]["triggered_metrics"]


def test_recommend_maintenance_for_critical_tool():
    states = [{
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
    anomalies = detect_anomalies(states)
    actions = recommend_actions(states, anomalies)
    assert actions[0]["recommended_action"] == "maintenance"


def test_snapshot_generation_tool_count():
    snapshot = generate_snapshot(seed=7, n_tools=12, fab_name="fab-beta")
    assert snapshot["fab_name"] == "fab-beta"
    assert len(snapshot["tools"]) == 12
