# Fab Digital Twin MVP

반도체/스마트팩토리 소프트웨어 직무를 겨냥한 **포트폴리오형 미니 프로젝트**입니다.

이 프로젝트는 가상의 반도체 fab 설비 데이터를 생성하고, 이상 징후를 감지하고, 수율 영향을 추정한 뒤, `continue / inspect / maintenance` 형태의 운영 의사결정을 내려서 **Digital Twin 스타일 대시보드와 이벤트 로그**로 출력합니다.

## 핵심 포인트
- **Autonomous Factory 향 S/W 개발** 느낌의 end-to-end 흐름
- **실시간 공정제어/수율·품질 분석**을 흉내 낸 rule-based 엔진
- **Virtual Fab Simulation** 형태의 복수 설비 상태 시뮬레이션
- **Data Governance**를 의식한 JSON snapshot + append-friendly JSONL event log
- Python 표준 라이브러리 중심이라 **실행/설명/면접 대응이 쉬움**

## 프로젝트 구조
```text
fab-digital-twin-mvp/
├─ README.md
├─ requirements.txt
├─ output/
│  ├─ dashboard.html
│  ├─ events.jsonl
│  └─ snapshot.json
├─ src/
│  └─ fab_sim/
│     ├─ __init__.py
│     ├─ app.py
│     ├─ anomaly.py
│     ├─ config.py
│     ├─ decision.py
│     └─ simulator.py
└─ tests/
   └─ test_engine.py
```

## 기능
### 1) 설비 상태 시뮬레이션
- 공정 step: deposition / etch / clean / inspection
- 메트릭:
  - temperature
  - pressure
  - vibration
  - throughput_wph
  - defect_rate
  - queue_size
  - utilization
  - health_score

### 2) 이상 감지
- baseline mean/std 기반 z-score 계산
- high-is-bad / low-is-bad 메트릭 분리
- queue congestion, health score 저하도 리스크로 반영
- severity를 `normal / warning / critical`로 분류

### 3) 운영 의사결정
- 이상 severity + 예측 수율 기반으로
  - `continue`
  - `inspect`
  - `maintenance`
  추천

### 4) 결과물 생성
- `snapshot.json`: 전체 상태 스냅샷
- `events.jsonl`: 생산 데이터 거버넌스용 이벤트 로그
- `dashboard.html`: 브라우저에서 바로 볼 수 있는 대시보드

## 실행 방법
### 기본 실행
```bash
cd /Users/young/.openclaw/workspace/projects/fab-digital-twin-mvp
PYTHONPATH=src python3 -m fab_sim.app
```

### 옵션 사용
```bash
PYTHONPATH=src python3 -m fab_sim.app --seed 7 --tools 12 --fab-name fab-beta --output-dir ./output
```

## 테스트
```bash
cd /Users/young/.openclaw/workspace/projects/fab-digital-twin-mvp
python3 -m pytest -q
```

pytest가 없다면:
```bash
python3 -m unittest discover -s tests
```

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
- downstream ingest/Kafka 적재를 상상하기 쉬운 형태

## 면접에서 이렇게 설명 가능
- “실제 fab 전체를 구현한 건 아니고, **설비 상태·수율·이상 감지·운영 의사결정의 연결 구조**를 보여주는 디지털 트윈 MVP를 만들었습니다.”
- “모델이 블랙박스면 설명이 어려워서, 먼저 **rule-based / explainable pipeline**으로 구성했습니다.”
- “JSON snapshot과 JSONL 로그로 분리해서 **운영 상태 조회와 데이터 적재 흐름을 분리**했습니다.”
- “추후에는 Kafka, FastAPI, discrete-event simulation, ML 기반 predictive maintenance로 확장 가능하게 설계했습니다.”

## 이력서 bullet 예시
- Python 기반 **Fab Digital Twin MVP** 구현: 설비 상태 시뮬레이션, 이상 감지, 수율 영향 분석, 운영 의사결정 자동화 파이프라인 개발
- 반도체 생산 시스템을 가정한 **Virtual Fab dashboard / JSONL event logging** 설계로 모니터링 및 데이터 거버넌스 구조 시연
- z-score 기반 anomaly detection과 rule-based maintenance recommendation을 통해 **explainable decision support** 프로토타입 구현

## 확장 아이디어
- FastAPI REST API + WebSocket 실시간 스트리밍
- Kafka/MQTT 기반 telemetry ingest
- AMR / 반송 로직 시뮬레이션 추가
- SRE 관점의 alerting, SLO, retry/fallback 설계
- Docker, GitHub Actions CI, containerized demo
- discrete-event simulation 기반 lot flow / dispatching 최적화

## 현재 한계
- 실제 반도체 공정 모델이 아니라 simplified demo
- ML 예측모델 대신 rule-based 엔진 사용
- 실시간 stream processing 대신 batch snapshot 생성

그래도 **짧은 시간 안에 직무 키워드를 코드로 연결해서 보여주는 포트폴리오 프로젝트**로는 꽤 강한 편입니다.
