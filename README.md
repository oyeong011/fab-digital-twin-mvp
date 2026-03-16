# Fab Digital Twin MVP

반도체 생산/설비 소프트웨어 직무 키워드를 한 번에 보여주는 데모 프로젝트입니다.

## What it shows
- 생산설비 telemetry 시뮬레이션
- 실시간 이상 감지(z-score 기반)
- 간단한 수율/품질 영향 분석
- 예측 의사결정(continue / inspect / maintenance)
- Virtual Fab 스타일의 디지털 트윈 대시보드 HTML 생성
- 생산 Data 거버넌스용 이벤트 로그(JSONL)

## Architecture
1. `simulator.py` : 설비/공정 상태 데이터 생성
2. `anomaly.py` : rolling baseline 기반 이상 감지
3. `decision.py` : 품질/리스크 기반 의사결정
4. `app.py` : 전체 파이프라인 실행 + dashboard/export 생성

## Run
```bash
python3 src/fab_sim/app.py
```

실행 후 생성물:
- `output/snapshot.json`
- `output/events.jsonl`
- `output/dashboard.html`

## Why this project fits the JD
- **Autonomous Factory 향 S/W 개발**: 설비 데이터 기반 이상 감지/의사결정 자동화
- **실시간 공정제어/수율 품질 분석**: step별 sensor drift와 predicted yield 계산
- **Virtual Fab Simulation**: 여러 장비를 가진 가상 fab 상태 시뮬레이션
- **Data governance**: schema-conscious JSON snapshot + append-only event log
- **요구사항→설계→구현**: 모듈 분리, 재현 가능한 seed, 설명 가능한 규칙 기반 판단

## Next upgrades
- Kafka / MQTT ingest
- FastAPI endpoint + WebSocket streaming
- ML-based predictive maintenance
- Discrete-event simulation with queue/transport optimization
- Docker + CI
