from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ToolSnapshot(BaseModel):
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
    signals: Dict[str, float]
    triggered_metrics: List[str]
    risk_score: float
    severity: str
    predicted_yield: float
    recommended_action: str
    reason: str


class SnapshotSummary(BaseModel):
    tool_count: int
    severity_counts: Dict[str, int]
    action_counts: Dict[str, int]
    avg_predicted_yield: float
    avg_health_score: float
    highest_risk_tool: Optional[str] = None
    highest_risk_score: Optional[float] = None


class FabSnapshot(BaseModel):
    generated_at: str
    schema_version: str
    fab_name: str
    tools: List[ToolSnapshot]


class SnapshotResponse(BaseModel):
    summary: SnapshotSummary
    snapshot: FabSnapshot


class EventRecord(BaseModel):
    event_type: str = Field(default="tool_snapshot")
    tool_id: str
    process_step: str
    severity: str
    risk_score: float
    triggered_metrics: List[str]
    recommended_action: str
    predicted_yield: float
    timestamp: str
