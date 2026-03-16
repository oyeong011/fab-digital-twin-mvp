from __future__ import annotations

from typing import Dict, List

from fab_sim.config import BASELINES, HIGH_IS_BAD, LOW_IS_BAD


def z_score(value: float, mean: float, std: float) -> float:
    if std == 0:
        return 0.0
    return (value - mean) / std


def detect_anomalies(states: List[Dict]) -> List[Dict]:
    results: List[Dict] = []
    for state in states:
        signals = {}
        risk = 0.0
        triggered = []

        for metric, baseline in BASELINES.items():
            score = z_score(state[metric], baseline["mean"], baseline["std"])
            signals[metric] = round(score, 2)

            if metric in HIGH_IS_BAD and score >= 1.8:
                triggered.append(metric)
                risk += min(abs(score) * 10, 35)
            elif metric in LOW_IS_BAD and score <= -1.5:
                triggered.append(metric)
                risk += min(abs(score) * 10, 30)

        if state["queue_size"] >= 20:
            triggered.append("queue_size")
            risk += 12
        if state["health_score"] <= 55:
            triggered.append("health_score")
            risk += 18

        severity = "normal"
        if risk >= 50:
            severity = "critical"
        elif risk >= 25:
            severity = "warning"

        results.append(
            {
                "tool_id": state["tool_id"],
                "signals": signals,
                "triggered_metrics": sorted(set(triggered)),
                "risk_score": round(min(risk, 100), 2),
                "severity": severity,
            }
        )
    return results
