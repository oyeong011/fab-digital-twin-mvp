from __future__ import annotations

from collections import Counter


def summarize_snapshot(snapshot: dict) -> dict:
    tools = snapshot["tools"]
    severity_counts = Counter(tool["severity"] for tool in tools)
    action_counts = Counter(tool["recommended_action"] for tool in tools)
    avg_yield = round(sum(tool["predicted_yield"] for tool in tools) / len(tools), 2) if tools else 0.0
    avg_health = round(sum(tool["health_score"] for tool in tools) / len(tools), 2) if tools else 0.0
    highest_risk = max(tools, key=lambda t: t["risk_score"], default=None)

    return {
        "tool_count": len(tools),
        "severity_counts": dict(severity_counts),
        "action_counts": dict(action_counts),
        "avg_predicted_yield": avg_yield,
        "avg_health_score": avg_health,
        "highest_risk_tool": highest_risk["tool_id"] if highest_risk else None,
        "highest_risk_score": highest_risk["risk_score"] if highest_risk else None,
    }


def build_dashboard(snapshot: dict) -> str:
    summary = summarize_snapshot(snapshot)
    rows = []
    for row in snapshot["tools"]:
        color = {
            "critical": "#3b0d0d",
            "warning": "#3a2a06",
            "normal": "#0f2f1c",
        }[row["severity"]]
        badge = {
            "critical": "#ef4444",
            "warning": "#f59e0b",
            "normal": "#22c55e",
        }[row["severity"]]
        rows.append(
            f"<tr><td><strong>{row['tool_id']}</strong></td><td>{row['process_step']}</td>"
            f"<td>{row['temperature']}</td><td>{row['pressure']}</td><td>{row['vibration']}</td>"
            f"<td>{row['throughput_wph']}</td><td>{row['defect_rate']}</td><td>{row['queue_size']}</td>"
            f"<td>{row['health_score']}</td><td>{row['risk_score']}</td>"
            f"<td><span class='pill' style='background:{badge}'>{row['severity']}</span></td>"
            f"<td>{row['recommended_action']}</td><td>{row['predicted_yield']}</td>"
            f"<td>{', '.join(row['triggered_metrics']) or '-'}</td></tr>"
        )

    action_cards = ''.join(
        f"<div class='mini-card'><strong>{name}</strong><br>{count}</div>"
        for name, count in sorted(summary['action_counts'].items())
    ) or "<div class='mini-card'><strong>none</strong><br>0</div>"

    return f"""
<!doctype html>
<html>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>Fab Digital Twin Portfolio Demo</title>
  <style>
    :root {{
      --bg:#020617; --panel:#0f172a; --panel2:#111827; --line:#334155;
      --text:#e5e7eb; --muted:#94a3b8; --accent:#38bdf8;
    }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif; background:linear-gradient(180deg,#020617,#0f172a); color:var(--text); }}
    .wrap {{ max-width: 1380px; margin: 0 auto; padding: 32px 20px 48px; }}
    .hero {{ display:grid; grid-template-columns: 1.6fr 1fr; gap:20px; margin-bottom:20px; }}
    .panel {{ background: rgba(15,23,42,.92); border:1px solid var(--line); border-radius:20px; padding:20px; box-shadow: 0 20px 50px rgba(0,0,0,.25); }}
    h1 {{ margin:0 0 8px; font-size: 34px; }}
    p {{ margin:0; line-height:1.6; }}
    .muted {{ color:var(--muted); }}
    .cards {{ display:grid; grid-template-columns: repeat(5, minmax(140px,1fr)); gap:16px; margin:20px 0; }}
    .card, .mini-card {{ background:var(--panel2); border:1px solid var(--line); border-radius:18px; padding:16px; }}
    .mini-grid {{ display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; margin-top:16px; }}
    .label {{ color:var(--muted); font-size:13px; margin-bottom:8px; text-transform:uppercase; letter-spacing:.08em; }}
    .value {{ font-size:28px; font-weight:700; }}
    .pills {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:14px; }}
    .pill {{ display:inline-block; color:white; border-radius:999px; padding:6px 10px; font-size:12px; font-weight:700; text-transform:uppercase; }}
    .grid2 {{ display:grid; grid-template-columns: 1.2fr .8fr; gap:20px; margin-bottom:20px; }}
    ul {{ margin:10px 0 0 18px; color:var(--text); }}
    li {{ margin:8px 0; }}
    table {{ width:100%; border-collapse:separate; border-spacing:0 10px; }}
    th {{ color:var(--muted); text-align:left; font-size:12px; font-weight:700; padding:0 12px 8px; text-transform:uppercase; letter-spacing:.08em; }}
    td {{ background:rgba(15,23,42,.98); padding:14px 12px; border-top:1px solid #1e293b; border-bottom:1px solid #1e293b; font-size:14px; }}
    td:first-child {{ border-left:1px solid #1e293b; border-radius:12px 0 0 12px; }}
    td:last-child {{ border-right:1px solid #1e293b; border-radius:0 12px 12px 0; }}
    .footer {{ margin-top:20px; color:var(--muted); font-size:14px; }}
    code {{ background:#1e293b; color:#e2e8f0; padding:2px 6px; border-radius:6px; }}
    @media (max-width: 980px) {{
      .hero, .grid2, .cards {{ grid-template-columns: 1fr; }}
      .mini-grid {{ grid-template-columns: 1fr; }}
      h1 {{ font-size:28px; }}
    }}
  </style>
</head>
<body>
  <div class='wrap'>
    <div class='hero'>
      <section class='panel'>
        <div class='label'>Portfolio Demo</div>
        <h1>Fab Digital Twin & Autonomous Factory Decision Support</h1>
        <p class='muted'>Generated at {snapshot['generated_at']} · Fab: {snapshot['fab_name']} · Schema: {snapshot['schema_version']}</p>
        <div class='pills'>
          <span class='pill' style='background:#0ea5e9'>virtual fab simulation</span>
          <span class='pill' style='background:#8b5cf6'>yield analytics</span>
          <span class='pill' style='background:#10b981'>data governance</span>
          <span class='pill' style='background:#f59e0b'>decision support</span>
        </div>
      </section>
      <aside class='panel'>
        <div class='label'>Top Risk</div>
        <div class='value'>{summary['highest_risk_tool'] or '-'}</div>
        <p class='muted'>Highest risk score: {summary['highest_risk_score'] if summary['highest_risk_score'] is not None else '-'}</p>
        <div class='mini-grid'>{action_cards}</div>
      </aside>
    </div>

    <div class='cards'>
      <div class='card'><div class='label'>Total Tools</div><div class='value'>{summary['tool_count']}</div></div>
      <div class='card'><div class='label'>Critical</div><div class='value'>{summary['severity_counts'].get('critical', 0)}</div></div>
      <div class='card'><div class='label'>Warning</div><div class='value'>{summary['severity_counts'].get('warning', 0)}</div></div>
      <div class='card'><div class='label'>Avg Predicted Yield</div><div class='value'>{summary['avg_predicted_yield']}%</div></div>
      <div class='card'><div class='label'>Avg Health Score</div><div class='value'>{summary['avg_health_score']}</div></div>
    </div>

    <div class='grid2'>
      <section class='panel'>
        <div class='label'>How to explain this project</div>
        <ul>
          <li>설비 상태 데이터를 가상 생성하고, 이상 감지 후 운영 액션을 추천하는 Digital Twin MVP입니다.</li>
          <li>실제 ML 대신 rule-based pipeline으로 시작해서 explainability를 확보했습니다.</li>
          <li>운영 조회용 snapshot과 적재 친화적인 JSONL event log를 분리했습니다.</li>
        </ul>
      </section>
      <section class='panel'>
        <div class='label'>Run</div>
        <p><code>PYTHONPATH=src python3 -m fab_sim.app --seed 7 --tools 12</code></p>
        <p class='footer'>API server: <code>uvicorn fab_sim.api:app --reload</code></p>
      </section>
    </div>

    <section class='panel'>
      <div class='label'>Tool Snapshot Table</div>
      <table>
        <thead>
          <tr>
            <th>Tool</th><th>Step</th><th>Temp</th><th>Pressure</th><th>Vibration</th><th>Throughput</th>
            <th>Defect</th><th>Queue</th><th>Health</th><th>Risk</th><th>Severity</th><th>Action</th><th>Yield</th><th>Triggers</th>
          </tr>
        </thead>
        <tbody>
          {''.join(rows)}
        </tbody>
      </table>
      <p class='footer'>This HTML is generated statically, so you can attach it to a portfolio without additional frontend build steps.</p>
    </section>
  </div>
</body>
</html>
"""
