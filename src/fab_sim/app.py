from __future__ import annotations

import argparse
import json
from pathlib import Path
from datetime import datetime

from fab_sim.simulator import generate_tool_states, states_as_dicts
from fab_sim.anomaly import detect_anomalies
from fab_sim.decision import recommend_actions
from fab_sim.dashboard import build_dashboard
from fab_sim.config import DEFAULT_FAB_NAME, DEFAULT_SCHEMA_VERSION, DEFAULT_SEED, DEFAULT_TOOL_COUNT
from fab_sim.service import build_event_records, save_event_jsonl, save_tool_csv


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = ROOT / "output"


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
    save_event_jsonl(build_event_records(snapshot), output_dir / "events.jsonl")
    save_tool_csv(snapshot, output_dir / "tools.csv")
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
    print(
        f"Artifacts: {output_dir / 'snapshot.json'}, {output_dir / 'events.jsonl'}, "
        f"{output_dir / 'tools.csv'}, {output_dir / 'dashboard.html'}"
    )
    for tool in critical:
        print(f"- {tool['tool_id']}: action={tool['recommended_action']}, yield={tool['predicted_yield']}%")


if __name__ == "__main__":
    main()
