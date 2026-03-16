from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

from simulator import generate_tool_states, states_as_dicts
from anomaly import detect_anomalies
from decision import recommend_actions


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output"


def build_dashboard(snapshot: dict) -> str:
    rows = []
    for row in snapshot["tools"]:
        color = {
            "critical": "#fee2e2",
            "warning": "#fef3c7",
            "normal": "#dcfce7",
        }[row["severity"]]
        rows.append(
            f"<tr style='background:{color}'><td>{row['tool_id']}</td><td>{row['process_step']}</td>"
            f"<td>{row['temperature']}</td><td>{row['pressure']}</td><td>{row['vibration']}</td>"
            f"<td>{row['throughput_wph']}</td><td>{row['defect_rate']}</td><td>{row['queue_size']}</td>"
            f"<td>{row['health_score']}</td><td>{row['severity']}</td><td>{row['recommended_action']}</td>"
            f"<td>{row['predicted_yield']}</td></tr>"
        )

    critical_count = sum(1 for t in snapshot["tools"] if t["severity"] == "critical")
    warning_count = sum(1 for t in snapshot["tools"] if t["severity"] == "warning")
    avg_yield = round(sum(t["predicted_yield"] for t in snapshot["tools"]) / len(snapshot["tools"]), 2)

    return f"""
<!doctype html>
<html>
<head>
  <meta charset='utf-8'>
  <title>Fab Digital Twin MVP</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 32px; background:#0f172a; color:#e2e8f0; }}
    .cards {{ display:grid; grid-template-columns: repeat(4, minmax(140px, 1fr)); gap:16px; margin-bottom:24px; }}
    .card {{ background:#111827; padding:16px; border-radius:16px; border:1px solid #334155; }}
    table {{ width:100%; border-collapse:collapse; background:white; color:#111827; border-radius:12px; overflow:hidden; }}
    th, td {{ padding:10px; border-bottom:1px solid #e5e7eb; text-align:left; font-size:14px; }}
    th {{ background:#e2e8f0; }}
    .muted {{ color:#94a3b8; }}
  </style>
</head>
<body>
  <h1>Fab Digital Twin MVP</h1>
  <p class='muted'>Generated at {snapshot['generated_at']}</p>
  <div class='cards'>
    <div class='card'><strong>Total Tools</strong><br>{len(snapshot['tools'])}</div>
    <div class='card'><strong>Critical</strong><br>{critical_count}</div>
    <div class='card'><strong>Warning</strong><br>{warning_count}</div>
    <div class='card'><strong>Avg Predicted Yield</strong><br>{avg_yield}%</div>
  </div>
  <table>
    <thead>
      <tr>
        <th>Tool</th><th>Step</th><th>Temp</th><th>Pressure</th><th>Vibration</th>
        <th>Throughput</th><th>Defect</th><th>Queue</th><th>Health</th><th>Severity</th><th>Action</th><th>Yield</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
</body>
</html>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    states = states_as_dicts(generate_tool_states())
    anomalies = detect_anomalies(states)
    actions = recommend_actions(states, anomalies)

    anomaly_map = {a["tool_id"]: a for a in anomalies}
    action_map = {a["tool_id"]: a for a in actions}

    tools = []
    for state in states:
        merged = {
            **state,
            **{k: v for k, v in anomaly_map[state["tool_id"]].items() if k != "tool_id"},
            **{k: v for k, v in action_map[state["tool_id"]].items() if k != "tool_id"},
        }
        tools.append(merged)

    snapshot = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "schema_version": "1.0.0",
        "fab_name": "virtual-fab-alpha",
        "tools": tools,
    }

    (OUT / "snapshot.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    with (OUT / "events.jsonl").open("w", encoding="utf-8") as f:
        for tool in tools:
            f.write(json.dumps({
                "event_type": "tool_snapshot",
                "tool_id": tool["tool_id"],
                "severity": tool["severity"],
                "recommended_action": tool["recommended_action"],
                "predicted_yield": tool["predicted_yield"],
                "timestamp": tool["timestamp"],
            }) + "\n")

    (OUT / "dashboard.html").write_text(build_dashboard(snapshot), encoding="utf-8")

    critical = [t for t in tools if t["severity"] == "critical"]
    print("Fab Digital Twin MVP generated.")
    print(f"Tools: {len(tools)}, critical: {len(critical)}")
    for tool in critical:
        print(f"- {tool['tool_id']}: action={tool['recommended_action']}, yield={tool['predicted_yield']}%")


if __name__ == "__main__":
    main()
