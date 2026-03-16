# Fab Digital Twin MVP

반도체/스마트팩토리 소프트웨어 직무를 겨냥한 **포트폴리오형 프로젝트**입니다.

이 프로젝트는 가상의 반도체 fab 설비 데이터를 생성하고, 이상 징후를 감지하고, 수율 영향을 추정한 뒤, `continue / inspect / maintenance` 형태의 운영 의사결정을 내려서 **Digital Twin 스타일 대시보드, API, 이벤트 로그, CSV export**로 출력합니다.

## 현재 수준
이제 이 프로젝트는 단순 예제가 아니라 아래까지 포함합니다.
- 시뮬레이션 엔진
- 이상 감지 / 의사결정 로직
- 정적 HTML 대시보드
- FastAPI 기반 API 서버
- CSV / JSON / JSONL 산출물
- unittest 기반 검증
- Dockerfile
- GitHub Actions CI
- 아키텍처 문서 / 면접 가이드

## 핵심 포인트
- **Autonomous Factory 향 S/W 개발** 느낌의 end-to-end 흐름
- **실시간 공정제어/수율·품질 분석**을 흉내 낸 rule-based 엔진
- **Virtual Fab Simulation** 형태의 복수 설비 상태 시뮬레이션
- **Data Governance**를 의식한 JSON snapshot + JSONL event log + CSV export
- **API / HTML / 문서 / CI**가 모두 있어서 포트폴리오/면접 대응이 쉬움

## 프로젝트 구조
```text
fab-digital-twin-mvp/
├─ .github/workflows/ci.yml
├─ .gitignore
├─ ARCHITECTURE.md
├─ Dockerfile
├─ INTERVIEW_GUIDE.md
├─ Makefile
├─ README.md
├─ requirements.txt
├─ output/
│  ├─ dashboard.html
│  ├─ events.jsonl
│  ├─ snapshot.json
│  └─ tools.csv
├─ src/
│  └─ fab_sim/
│     ├─ __init__.py
│     ├─ api.py
│     ├─ app.py
│     ├─ anomaly.py
│     ├─ config.py
│     ├─ dashboard.py
│     ├─ decision.py
│     ├─ models.py
│     ├─ service.py
│     └─ simulator.py
└─ tests/
   └─ test_engine.py
```

## API
- `GET /health`
- `GET /api/snapshot`
- `GET /api/summary`
- `GET /api/events`
- `GET /dashboard`

## 실행 방법
### A. 정적 산출물 생성
```bash
cd /Users/young/.openclaw/workspace/projects/fab-digital-twin-mvp
PYTHONPATH=src python3 -m fab_sim.app --seed 7 --tools 12 --fab-name fab-beta --output-dir ./output
```

생성물:
- `output/snapshot.json`
- `output/events.jsonl`
- `output/tools.csv`
- `output/dashboard.html`

### B. API 서버 실행
```bash
cd /Users/young/.openclaw/workspace/projects/fab-digital-twin-mvp
python3 -m pip install -r requirements.txt
PYTHONPATH=src python3 -m uvicorn fab_sim.api:app --reload
```

열어볼 주소:
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/api/snapshot?seed=7&tools=12&fab_name=fab-beta`
- `http://127.0.0.1:8000/api/summary?seed=7&tools=12&fab_name=fab-beta`
- `http://127.0.0.1:8000/api/events?seed=7&tools=12&fab_name=fab-beta`
- `http://127.0.0.1:8000/dashboard?seed=7&tools=12&fab_name=fab-beta`

### C. Makefile 사용
```bash
make install
make test
make run
make api
```

### D. Docker 실행
```bash
docker build -t fab-digital-twin-mvp .
docker run --rm -p 8000:8000 fab-digital-twin-mvp
```

## 테스트
```bash
cd /Users/young/.openclaw/workspace/projects/fab-digital-twin-mvp
python3 -m unittest discover -s tests -v
```

테스트 범위:
- anomaly detection
- decision recommendation
- snapshot generation
- output export
- FastAPI endpoint 동작

## 문서
- 아키텍처 설명: `ARCHITECTURE.md`
- 면접 답변 가이드: `INTERVIEW_GUIDE.md`

## 이 프로젝트가 JD와 맞는 이유
### Autonomous Factory 향 S/W 개발
- 설비 상태 데이터 생성 → 이상 감지 → 액션 추천의 자동화 흐름 구현
- 생산시스템 운영 관점의 `monitoring + decision support` 구조를 보여줌

### 반도체 설비 실시간 공정제어 및 수율/품질 분석
- 공정 메트릭 변동을 사용해 defect/yield impact를 계산
- 설비 health 및 queue 상태가 운영 품질에 미치는 영향 반영

### 자율/예측 의사결정 모델링 + Virtual Fab Simulation
- 복수 장비를 가진 가상의 fab snapshot 생성
- rule-based지만 explainable한 의사결정 로직 포함

### 생산 Data 거버넌스
- 구조화된 snapshot schema
- append-friendly event log(JSONL)
- 분석/공유 친화적인 CSV export

## 면접에서 이렇게 한 줄로 설명 가능
> “가상의 반도체 fab 데이터를 기반으로 이상 감지, 수율 영향 분석, 운영 의사결정을 연결한 Digital Twin MVP를 Python/FastAPI로 구현했고, API·대시보드·CSV/JSONL export·CI까지 포함해 포트폴리오 수준으로 고도화했습니다.”

## 이력서 bullet 예시
- Python/FastAPI 기반 **Fab Digital Twin MVP** 구현: 설비 상태 시뮬레이션, 이상 감지, 수율 영향 분석, 운영 의사결정 자동화 파이프라인 개발
- 반도체 생산 시스템을 가정한 **Virtual Fab dashboard / REST API / JSONL·CSV export** 설계로 모니터링 및 데이터 거버넌스 구조 시연
- unittest, Dockerfile, GitHub Actions CI를 추가해 **설명 가능한 데모를 재현 가능한 엔지니어링 결과물**로 고도화

## 다음에 더 붙일 수 있는 것
- WebSocket 기반 near real-time dashboard
- Kafka/MQTT 기반 telemetry ingest
- AMR / 반송 로직 시뮬레이션 추가
- SRE 관점 alerting / SLO / retry-fallback 설계
- discrete-event simulation 기반 lot flow / dispatching 최적화
- ML 기반 predictive maintenance
