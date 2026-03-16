from __future__ import annotations

import argparse
import json
from pathlib import Path
from datetime import datetime

from fab_sim.simulator import generate_tool_states, states_as_dicts
from fab_sim.anomaly import detect_anomalies
from fab_sim.decision import recommend_actions
from fab_sim.config import DEFAULT_FAB_NAME, DEFAULT_SCHEMA_VERSION, DEFAULT_SEED, DEFAULT_TOOL_COUNT


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = ROOT / "output"


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
            f"<td>{row['predicted_yield']}</td><td>{', '.join(row['triggered_metrics']) or '-'}</td></tr>"
        )

    critical_count = sum(1 for t in snapshot["tools"] if t["severity"] == "critical")
    warning_count = sum(1 for t in snapshot["tools"] if t["severity"] == "warning")
    inspect_count = sum(1 for t in snapshot["tools"] if t["recommended_action"] == "inspect")
    avg_yield = round(sum(t["predicted_yield"] for t in snapshot["tools"]) / len(snapshot["tools"]), 2)

    return f"""
<!doctype html>
<html>
<head>
  <meta charset='utf-8'>
  <title>Fab Digital Twin MVP</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 32px; background:#0f172a; color:#e2e8f0; }}
    .cards {{ display:grid; grid-template-columns: repeat(5, minmax(140px, 1fr)); gap:16px; margin-bottom:24px; }}
    .card {{ background:#111827; padding:16px; border-radius:16px; border:1px solid #334155; }}
    table {{ width:100%; border-collapse:collapse; background:white; color:#111827; border-radius:12px; overflow:hidden; }}
    th, td {{ padding:10px; border-bottom:1px solid #e5e7eb; text-align:left; font-size:14px; vertical-align:top; }}
    th {{ background:#e2e8f0; }}
    .muted {{ color:#94a3b8; }}
    .footer {{ margin-top: 16px; color:#cbd5e1; font-size:14px; }}
    code {{ background:#1e293b; color:#e2e8f0; padding:2px 6px; border-radius:6px; }}
  </style>
</head>
<body>
  <h1>Fab Digital Twin MVP</h1>
  <p class='muted'>Generated at {snapshot['generated_at']} · Fab: {snapshot['fab_name']} · Schema: {snapshot['schema_version']}</p>
  <div class='cards'>
    <div class='card'><strong>Total Tools</strong><br>{len(snapshot['tools'])}</div>
    <div class='card'><strong>Critical</strong><br>{critical_count}</div>
    <div class='card'><strong>Warning</strong><br>{warning_count}</div>
    <div class='card'><strong>Inspect Action</strong><br>{inspect_count}</div>
    <div class='card'><strong>Avg Predicted Yield</strong><br>{avg_yield}%</div>
  </div>
  <table>
    <thead>
      <tr>
        <th>Tool</th><th>Step</th><th>Temp</th><th>Pressure</th><th>Vibration</th>
        <th>Throughput</th><th>Defect</th><th>Queue</th><th>Health</th><th>Severity</th><th>Action</th><th>Yield</th><th>Triggers</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
  <p class='footer'>Run again with <code>python3 -m fab_sim.app --seed 7 --tools 12</code> to generate a different fab snapshot.</p>
</body>
</html>
"""


def generate_snapshot(seed: int, n_tools: int, fab_name: str) -> dict:
    states = states_as_dicts(generate_tool_states(seed=seed, n_tools=n_tools))
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

    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "schema_version": DEFAULT_SCHEMA_VERSION,
        "fab_name": fab_name,
        "tools": tools,
    }


def save_outputs(snapshot: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "snapshot.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    with (output_dir / "events.jsonl").open("w", encoding="utf-8") as f:
        for tool in snapshot["tools"]:
            f.write(json.dumps({
                "event_type": "tool_snapshot",
                "tool_id": tool["tool_id"],
                "process_step": tool["process_step"],
                "severity": tool["severity"],
                "risk_score": tool["risk_score"],
                "triggered_metrics": tool["triggered_metrics"],
                "recommended_action": tool["recommended_action"],
                "predicted_yield": tool["predicted_yield"],
                "timestamp": tool["timestamp"],
            }) + "\n")

    (output_dir / "dashboard.html").write_text(build_dashboard(snapshot), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a fab digital twin snapshot.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Random seed for deterministic snapshot generation")
    parser.add_argument("--tools", type=int, default=DEFAULT_TOOL_COUNT, help="Number of virtual tools to simulate")
    parser.add_argument("--fab-name", default=DEFAULT_FAB_NAME, help="Logical fab name")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory for JSONL/HTML artifacts")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    snapshot = generate_snapshot(seed=args.seed, n_tools=args.tools, fab_name=args.fab_name)
    output_dir = Path(args.output_dir)
    save_outputs(snapshot, output_dir)

    critical = [t for t in snapshot["tools"] if t["severity"] == "critical"]
    warning = [t for t in snapshot["tools"] if t["severity"] == "warning"]
    print("Fab Digital Twin MVP generated.")
    print(f"Tools: {len(snapshot['tools'])}, critical: {len(critical)}, warning: {len(warning)}")
    print(f"Artifacts: {output_dir / 'snapshot.json'}, {output_dir / 'events.jsonl'}, {output_dir / 'dashboard.html'}")
    for tool in critical:
        print(f"- {tool['tool_id']}: action={tool['recommended_action']}, yield={tool['predicted_yield']}%")


if __name__ == "__main__":
    main()
