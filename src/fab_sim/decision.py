from __future__ import annotations

from typing import Dict, List


def recommend_actions(states: List[Dict], anomalies: List[Dict]) -> List[Dict]:
    indexed = {a["tool_id"]: a for a in anomalies}
    actions = []

    for state in states:
        anomaly = indexed[state["tool_id"]]
        predicted_yield = round(
            max(
                82.0,
                99.4
                - state["defect_rate"] * 100
                - max(0, state["temperature"] - 84) * 0.12
                - state["vibration"] * 9,
            ),
            2,
        )

        if anomaly["severity"] == "critical":
            action = "maintenance"
            reason = "Multiple abnormal signals detected; protect yield and equipment health."
        elif anomaly["severity"] == "warning" or predicted_yield < 95.5:
            action = "inspect"
            reason = "Operator inspection recommended before lot progression."
        else:
            action = "continue"
            reason = "Operating within acceptable process window."

        actions.append(
            {
                "tool_id": state["tool_id"],
                "predicted_yield": predicted_yield,
                "recommended_action": action,
                "reason": reason,
            }
        )
    return actions
