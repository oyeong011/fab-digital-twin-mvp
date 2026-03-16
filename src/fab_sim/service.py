from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import List

from fab_sim.models import EventRecord


def build_event_records(snapshot: dict) -> List[dict]:
    return [
        EventRecord(
            tool_id=tool["tool_id"],
            process_step=tool["process_step"],
            severity=tool["severity"],
            risk_score=tool["risk_score"],
            triggered_metrics=tool["triggered_metrics"],
            recommended_action=tool["recommended_action"],
            predicted_yield=tool["predicted_yield"],
            timestamp=tool["timestamp"],
        ).model_dump()
        for tool in snapshot["tools"]
    ]


def save_event_jsonl(records: List[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")


def save_tool_csv(snapshot: dict, path: Path) -> None:
    if not snapshot["tools"]:
        path.write_text("", encoding="utf-8")
        return

    fieldnames = [
        "tool_id",
        "process_step",
        "temperature",
        "pressure",
        "vibration",
        "throughput_wph",
        "defect_rate",
        "queue_size",
        "utilization",
        "health_score",
        "risk_score",
        "severity",
        "predicted_yield",
        "recommended_action",
        "triggered_metrics",
        "timestamp",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for tool in snapshot["tools"]:
            row = {key: tool.get(key) for key in fieldnames}
            row["triggered_metrics"] = ",".join(tool.get("triggered_metrics", []))
            writer.writerow(row)
