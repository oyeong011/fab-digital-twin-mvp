from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import random
from typing import List, Dict

from fab_sim.config import PROCESS_STEPS


@dataclass
class ToolState:
    tool_id: str
    process_step: str
    temperature: float
    pressure: float
    vibration: float
    throughput_wph: float
    defect_rate: float
    queue_size: int
    utilization: float
    health_score: float
    timestamp: str


def _bounded(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def generate_tool_states(seed: int = 42, n_tools: int = 8) -> List[ToolState]:
    rng = random.Random(seed)
    now = datetime.utcnow()
    states: List[ToolState] = []

    for i in range(n_tools):
        step = PROCESS_STEPS[i % len(PROCESS_STEPS)]
        base_temp = 70 + (i % 3) * 8
        base_pressure = 1.2 + (i % 4) * 0.15
        base_vibration = 0.15 + (i % 3) * 0.03
        base_throughput = 42 - (i % 4) * 3

        drift = rng.uniform(-1.0, 1.0)
        anomaly_boost = 1 if i in (2, 6) else 0

        temperature = base_temp + drift * 4 + anomaly_boost * rng.uniform(8, 14)
        pressure = base_pressure + drift * 0.08 + anomaly_boost * rng.uniform(0.18, 0.35)
        vibration = base_vibration + abs(drift) * 0.04 + anomaly_boost * rng.uniform(0.08, 0.18)
        throughput = base_throughput - anomaly_boost * rng.uniform(5, 11) + rng.uniform(-2, 2)
        defect_rate = _bounded(0.007 + anomaly_boost * rng.uniform(0.018, 0.05) + abs(drift) * 0.003, 0.001, 0.12)
        queue_size = int(_bounded(rng.randint(2, 18) + anomaly_boost * rng.randint(5, 15), 0, 40))
        utilization = _bounded(0.68 + rng.uniform(-0.08, 0.2) - anomaly_boost * 0.12, 0.2, 0.99)
        health_score = _bounded(100 - vibration * 120 - defect_rate * 600 - max(0, temperature - 84) * 0.8, 20, 99)

        states.append(
            ToolState(
                tool_id=f"EQP-{i+1:02d}",
                process_step=step,
                temperature=round(temperature, 2),
                pressure=round(pressure, 3),
                vibration=round(vibration, 3),
                throughput_wph=round(throughput, 2),
                defect_rate=round(defect_rate, 4),
                queue_size=queue_size,
                utilization=round(utilization, 3),
                health_score=round(health_score, 2),
                timestamp=(now + timedelta(seconds=i * 5)).isoformat() + "Z",
            )
        )

    return states


def states_as_dicts(states: List[ToolState]) -> List[Dict]:
    return [asdict(s) for s in states]
