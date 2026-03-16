from __future__ import annotations

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

from fab_sim.app import generate_snapshot
from fab_sim.dashboard import build_dashboard, summarize_snapshot
from fab_sim.config import DEFAULT_FAB_NAME, DEFAULT_SEED, DEFAULT_TOOL_COUNT

app = FastAPI(
    title="Fab Digital Twin API",
    version="1.0.0",
    description="Portfolio demo API for virtual fab simulation, anomaly detection, and decision support.",
)


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.get("/api/snapshot")
def snapshot(
    seed: int = Query(DEFAULT_SEED, ge=0),
    tools: int = Query(DEFAULT_TOOL_COUNT, ge=1, le=100),
    fab_name: str = Query(DEFAULT_FAB_NAME),
) -> dict:
    snapshot = generate_snapshot(seed=seed, n_tools=tools, fab_name=fab_name)
    return {
        "summary": summarize_snapshot(snapshot),
        "snapshot": snapshot,
    }


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    seed: int = Query(DEFAULT_SEED, ge=0),
    tools: int = Query(DEFAULT_TOOL_COUNT, ge=1, le=100),
    fab_name: str = Query(DEFAULT_FAB_NAME),
) -> str:
    snapshot = generate_snapshot(seed=seed, n_tools=tools, fab_name=fab_name)
    return build_dashboard(snapshot)
