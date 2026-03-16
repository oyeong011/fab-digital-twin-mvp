from __future__ import annotations

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

from fab_sim.app import generate_snapshot
from fab_sim.dashboard import build_dashboard, summarize_snapshot
from fab_sim.config import DEFAULT_FAB_NAME, DEFAULT_SEED, DEFAULT_TOOL_COUNT
from fab_sim.models import SnapshotResponse
from fab_sim.service import build_event_records

app = FastAPI(
    title="Fab Digital Twin API",
    version="1.1.0",
    description="Portfolio demo API for virtual fab simulation, anomaly detection, and decision support.",
    openapi_tags=[
        {"name": "system", "description": "Health and service metadata"},
        {"name": "simulation", "description": "Snapshot and event generation endpoints"},
        {"name": "ui", "description": "HTML dashboard rendering"},
    ],
)


@app.get("/health", tags=["system"])
def health() -> dict:
    return {"ok": True}


@app.get("/api/snapshot", response_model=SnapshotResponse, tags=["simulation"])
def snapshot(
    seed: int = Query(DEFAULT_SEED, ge=0),
    tools: int = Query(DEFAULT_TOOL_COUNT, ge=1, le=100),
    fab_name: str = Query(DEFAULT_FAB_NAME),
) -> dict:
    data = generate_snapshot(seed=seed, n_tools=tools, fab_name=fab_name)
    return {
        "summary": summarize_snapshot(data),
        "snapshot": data,
    }


@app.get("/api/summary", tags=["simulation"])
def summary(
    seed: int = Query(DEFAULT_SEED, ge=0),
    tools: int = Query(DEFAULT_TOOL_COUNT, ge=1, le=100),
    fab_name: str = Query(DEFAULT_FAB_NAME),
) -> dict:
    data = generate_snapshot(seed=seed, n_tools=tools, fab_name=fab_name)
    return summarize_snapshot(data)


@app.get("/api/events", tags=["simulation"])
def events(
    seed: int = Query(DEFAULT_SEED, ge=0),
    tools: int = Query(DEFAULT_TOOL_COUNT, ge=1, le=100),
    fab_name: str = Query(DEFAULT_FAB_NAME),
) -> dict:
    data = generate_snapshot(seed=seed, n_tools=tools, fab_name=fab_name)
    return {"events": build_event_records(data)}


@app.get("/dashboard", response_class=HTMLResponse, tags=["ui"])
def dashboard(
    seed: int = Query(DEFAULT_SEED, ge=0),
    tools: int = Query(DEFAULT_TOOL_COUNT, ge=1, le=100),
    fab_name: str = Query(DEFAULT_FAB_NAME),
) -> str:
    data = generate_snapshot(seed=seed, n_tools=tools, fab_name=fab_name)
    return build_dashboard(data)
