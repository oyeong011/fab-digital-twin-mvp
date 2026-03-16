# Interview Guide

## 30초 소개
반도체/스마트팩토리 직무를 염두에 두고, 가상의 fab 설비 데이터를 생성한 뒤 이상 감지와 수율 영향 분석을 수행하고, 마지막으로 운영 의사결정까지 추천하는 Digital Twin MVP를 Python으로 구현했습니다. 결과는 JSON snapshot, JSONL event log, HTML dashboard, 그리고 FastAPI endpoint로 제공해서 운영/분석/시연 포인트를 모두 보여줄 수 있게 했습니다.

## 1분 소개
이 프로젝트의 핵심은 단순히 데이터를 보여주는 게 아니라, 설비 상태 시뮬레이션부터 anomaly detection, decision support까지 end-to-end 흐름을 하나로 엮었다는 점입니다. 실제 fab 데이터를 쓰진 못했기 때문에 deterministic seed 기반 시뮬레이터를 만들었고, z-score 기반 rule engine으로 이상 여부를 판단했습니다. 이후 severity, defect rate, health score를 조합해 continue, inspect, maintenance 액션을 추천하게 했습니다. 또 운영 조회용 snapshot과 downstream 적재를 상정한 JSONL 로그를 분리해서 data governance 관점도 반영했습니다.

## 왜 ML 대신 rule-based인가?
- 초기 MVP 단계에서 explainability가 중요했기 때문
- 데이터가 적거나 fake data일 때 과한 ML은 설득력이 떨어질 수 있기 때문
- baseline tuning, thresholding, 운영 룰 연결 구조를 먼저 보여주는 게 더 직무 친화적이기 때문

## 이 프로젝트의 강점
- 직무 키워드를 코드 구조로 연결했다
- 설명 가능한 anomaly detection을 구현했다
- monitoring에서 끝나지 않고 decision support까지 갔다
- API/정적 대시보드/로그 산출물까지 있어서 시연이 쉽다

## 한계
- 실제 공정 물리 모델은 아니다
- 실시간 stream이 아니라 snapshot 중심이다
- ML predictive maintenance는 아직 미구현이다

## 다음 확장 계획
- FastAPI WebSocket으로 near real-time dashboard
- Kafka/MQTT ingestion
- 장비 dispatching / lot flow discrete-event simulation
- ML 기반 predictive maintenance 추가

## 예상 질문과 답변
### Q1. 왜 이 프로젝트를 만들었나요?
반도체/스마트팩토리 직무 설명을 보면 생산 시스템, 이상 감지, 수율/품질, 디지털 트윈, 데이터 거버넌스가 반복적으로 나와서, 이 키워드를 따로따로 공부하기보다 하나의 작은 프로젝트로 연결해서 보여주고 싶었습니다.

### Q2. 가장 신경 쓴 설계 포인트는?
설명 가능성과 시연 가능성입니다. 면접에서 빠르게 보여줄 수 있어야 해서 HTML dashboard와 FastAPI endpoint를 넣었고, 로직은 rule-based로 구성해서 왜 그런 판단이 나왔는지 설명할 수 있게 했습니다.

### Q3. 실무로 가면 무엇을 바꾸겠나요?
실제 telemetry schema와 설비 로그 포맷을 먼저 맞추고, batch snapshot 대신 streaming pipeline으로 바꾸겠습니다. 그 다음에는 threshold rule과 ML 모델을 혼합한 하이브리드 구조로 확장할 것 같습니다.
