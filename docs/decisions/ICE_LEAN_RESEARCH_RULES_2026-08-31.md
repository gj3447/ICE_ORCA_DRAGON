# ICE lean research rules

> **상태:** ACTIVE — 새 번호 없는 계산의 연구 방법 정본
> **발효:** 2026-08-31
> **권한:** 계산 기록, 검산 선택, 해석 범위를 정한다.
> **비권한:** Phase 51--56 reconciliation의 재개, 새 numbered Phase, direct-Python 우회,
> 물리학 주장, 자동 후속 작업 또는 ontology/외부 KG 승격.

이 규칙은 연구를 의례적 계약으로 만들지 않으면서 가짜 신호를 줄이기 위한 최소 공통
형식이다. Ragnarok 차단기의 실행 안전 경계는 그대로 유지한다. 즉 새 core 계산은 clean
committed runner를 `./ice run`으로 실행하고 공통 runtime/output/artifact 상한을 지키며,
killed reconciliation과 새 numbered descendant는 열지 않는다.

## 여섯 규칙

1. **질문 하나, 출력 하나, 비주장 하나.** 계산 전에 무엇을 계산하는지와 이 결과만으로는
   무엇을 주장하지 않는지를 각각 짧게 적는다.
2. **원결과 하나.** primary source, 방정식, convention, 가정, 입력, 명령, 환경, 실제 출력과
   실패를 raw result 또는 인접 메모 한 곳에 남긴다. 같은 check ledger를 README나 ontology에
   복제하지 않는다.
3. **실패원인을 먼저 고른다.** 아래 메뉴에서 가장 관련된 위험 하나를 고르고 control 1--3개만
   수행한다. 모든 계산에 모든 검사를 붙이지 않는다.
4. **주장 강도에 비례해 독립 검산한다.** 같은 runner의 재실행은 repeatability이며 독립
   evidence가 아니다. 중요한 결론은 독립 유도, 다른 engine/basis, precision/refinement 또는
   새 자료 중 실제 위험을 낮추는 검산을 더한다.
5. **네 층을 분리한다.** finite calculation에서 확인된 사실, numerical error 판단,
   model/continuum 해석, physical/empirical hypothesis를 한 문장이나 verdict로 합치지 않는다.
6. **결과는 후속 작업을 자동 승인하지 않는다.** 다음 계산은 기존 evidence가 남긴 구체적
   장애물을 겨냥하는 독립 질문일 때만 연다. claim/evidence/scope/open problem이 실질적으로
   바뀔 때만 ontology를 갱신하고, 장기 회귀 기준으로 승격한 결과만 repro manifest에 등록한다.

## 실패원인별 선택 메뉴

| 주된 위험 | 적절한 최소 control 예시 |
|---|---|
| algebra 또는 sign/unit | 손계산 spot check, 독립 CAS, convention/차원 검사 |
| discretization 또는 truncation | resolution/cutoff ladder, exact modal 또는 omitted-tail control |
| solver 또는 root/ODE | precision ladder, conditioning, limiting case, interval/certified enclosure |
| spectrum | basis 변화, spectral-pollution 또는 boundary-condition control |
| gauge 또는 constrained system | Jacobi/constraint residual, gauge/basis 변화, refinement |
| inference | search family와 null을 기록하고, holdout/blinding 또는 calibrated simulation을 사용 |

`PASS`는 선택한 control의 통과만 뜻한다. null, basis dependence, sign/unit error와
`INCONCLUSIVE`는 원하는 결론에 맞춰 감추지 않고 원결과에 남긴다.

## 탐색, 확인, 통계

결정론적 exact/numerical 탐색에는 사전등록, p-value 또는 FDR을 기본 요구하지 않는다. 외부
자료에 대한 confirmatory empirical claim에서만 primary observable, scan/cut/nuisance 범위와
stopping rule을 먼저 고정하고 변경은 timestamp와 이유를 남긴다. likelihood scan에는 local
excess가 아닌 정의된 search family의 global calibration을 사용하며, Bayesian 구현은 필요할 때
simulation-based calibration을 사용한다. 탐색은 허용하되 탐색이라고 표기한다.

## 설계 근거

이 정책은 채택 가능한 최소 계산 관행, 계산 재현과 독립 replication의 구별, verification과
validation의 구별, 단계별 transparency, 탐색과 확인의 분리를 조합한 repository-local 결론이다.
다음 자료는 ICE 결과의 물리적 증거가 아니라 이 방법 설계의 출처다.

- [Wilson et al., *Good Enough Practices in Scientific Computing*](https://doi.org/10.1371/journal.pcbi.1005510)
- [Sandve et al., *Ten Simple Rules for Reproducible Computational Research*](https://doi.org/10.1371/journal.pcbi.1003285)
- [NASEM, *Reproducibility and Replicability in Science*](https://nap.nationalacademies.org/read/25303/chapter/3)
- [Roy, code and solution verification](https://doi.org/10.1016/j.jcp.2004.10.036)
- [TOP Guidelines](https://pmc.ncbi.nlm.nih.gov/articles/PMC4550299/)
- [Nosek et al., *The Preregistration Revolution*](https://doi.org/10.1073/pnas.1708274114)
- [Gross and Vitells, look-elsewhere effect](https://arxiv.org/abs/1005.1891)
- [Talts et al., simulation-based calibration](https://arxiv.org/abs/1804.06788)

이 문서는 historical contract, one-shot receipt, replay receipt, ordered-gate map 또는 recursive
audit map을 지우지 않는다. 그것들은 당시의 provenance 또는 선택적 분석 도구이며 새 번호 없는
계산의 기본 gate가 아니다.
