# 어떻게 검토하는가 — ICE ORCA DRAGON

새 주장은 먼저 공개 README와 관련 연구·결정·보고서를 읽고, 기존 결과가 어느 프로그램 경계에 속하는지 확인한다. 공개 CLI와 검사는 [SCIENTIFIC_CLI_MANUAL](SCIENTIFIC_CLI_MANUAL.md)을 따른다. 결과는 계산 워크벤치의 관측으로 기록하며, 물리적 타당성은 별도 근거와 반증 절차가 필요하다.

1. `research/README`에서 해당 영역과 기존 결과 파일의 위치를 확인한다.
2. CLI manual의 입력·출력·검사 조건을 읽고, 명령 결과를 독립적인 관측으로 보존한다.
3. 결과가 기존 claim·report와 연결될 때는 어떤 계산, 어느 입력, 어떤 한계인지 함께 적는다.
4. 수치 부합을 물리적 결론으로 바꾸지 않는다. 반증 가능성·외부 근거는 별도 상태로 둔다.

새 계산을 설계할 때는 [lean research rules](decisions/ICE_LEAN_RESEARCH_RULES_2026-08-31.md)의 최소 형식을 사용한다. 하나의 질문과 하나의 산출물을 정하고, 그 산출물만으로 주장하지 않는 범위를 함께 적는다. 주된 실패 위험에 맞는 control만 선택하며, 같은 runner 재실행은 repeatability이지 독립 evidence가 아니다.
