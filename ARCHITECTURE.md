# Architecture Notes

## 목표
이 프로젝트는 반도체/스마트팩토리 직무에서 자주 나오는 키워드인
- Autonomous Factory
- Digital Twin
- 이상 감지
- 수율/품질 분석
- 생산 Data 거버넌스
를 **작게 하지만 연결된 형태**로 보여주는 포트폴리오용 MVP다.

## 흐름
```text
Virtual Tool Telemetry
    ↓
Simulation Engine (simulator.py)
    ↓
Anomaly Detection (anomaly.py)
    ↓
Decision Support (decision.py)
    ↓
Snapshot Builder (app.py)
    ├─ snapshot.json
    ├─ events.jsonl
    └─ dashboard.html
          ↓
      FastAPI (api.py)
      ├─ GET /health
      ├─ GET /api/snapshot
      └─ GET /dashboard
```

## 설계 의도
### 1. Simulation
실제 장비 데이터를 확보하기 어렵기 때문에, deterministic seed 기반으로 가상의 telemetry를 생성한다.
이렇게 하면 시연할 때마다 같은 결과를 재현할 수 있다.

### 2. Anomaly Detection
처음부터 복잡한 ML 모델을 넣기보다 z-score 기반 rule engine을 사용했다.
장점은 다음과 같다.
- 설명 가능성 높음
- 면접에서 reasoning 설명 쉬움
- baseline tuning 구조를 보여주기 좋음

### 3. Decision Support
severity, yield, health score를 바탕으로 continue / inspect / maintenance를 추천한다.
즉, 단순 모니터링이 아니라 **운영 의사결정까지 연결**한다.

### 4. Data Governance
운영 조회용 데이터와 적재용 데이터를 분리했다.
- `snapshot.json`: 조회/디버깅/대시보드용
- `events.jsonl`: downstream pipeline 적재 상상용

### 5. Delivery Surface
별도 프론트엔드 빌드 체인 없이도:
- 정적 HTML 대시보드 생성 가능
- FastAPI로 API/HTML 서빙 가능

이 구조 덕분에 로컬 실행, GitHub 업로드, 포트폴리오 첨부, 면접 시연이 모두 쉽다.

## 확장 방향
- Kafka/MQTT telemetry ingest
- FastAPI + WebSocket push
- ML 기반 predictive maintenance
- Discrete-event simulation for lot dispatching
- AMR / 반송 로직과 SRE 관점 alerting 추가
