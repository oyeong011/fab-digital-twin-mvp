from __future__ import annotations

DEFAULT_SEED = 42
DEFAULT_TOOL_COUNT = 8
DEFAULT_FAB_NAME = "virtual-fab-alpha"
DEFAULT_SCHEMA_VERSION = "1.1.0"

PROCESS_STEPS = ["deposition", "etch", "clean", "inspection"]

BASELINES = {
    "temperature": {"mean": 77.0, "std": 6.5},
    "pressure": {"mean": 1.45, "std": 0.16},
    "vibration": {"mean": 0.19, "std": 0.05},
    "throughput_wph": {"mean": 38.0, "std": 5.0},
    "defect_rate": {"mean": 0.012, "std": 0.01},
}

HIGH_IS_BAD = {"temperature", "pressure", "vibration", "defect_rate"}
LOW_IS_BAD = {"throughput_wph"}
