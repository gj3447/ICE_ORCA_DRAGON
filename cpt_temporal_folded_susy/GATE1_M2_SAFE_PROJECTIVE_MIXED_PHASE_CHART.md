# Gate-1 m=2 safe-projective mixed phase chart

## 실행 요약

정본은 raw result인
`GATE1_M2_SAFE_PROJECTIVE_MIXED_PHASE_CHART_RESULT.json`이다. 이 보고서는 그
결과를 사람이 읽을 수 있게 요약할 뿐, 추가 계산이나 물리 해석을 더하지 않는다.

실행 명령은 `./ice run gate1_m2_safe_projective_mixed_phase_chart`였고,
2026-09-03T02:36:46Z에 `VALID_RUN` 및
`KEEP_SCOPED_SAFE_PROJECTIVE_MIXED_PHASE_SIGN_CHART`가 기록됐다. source commit은
`57e978fc8f81c2f371dfd990b7f74c9a3da21809`이다.

## 선언한 chart와 정확한 결론

여기서 “compact ratio/phase chart”는 \((r,\alpha,\theta)\)라는 **좌표비와 위상**의
선언된 compact parameter domain을 뜻한다. 이는 compactification, boundary divisor,
relative homology component를 뜻하지 않는다. 반지름 \(s\)는 여전히 무한대로 가는
unbounded radial tail이다. 여기서 projective는 좌표비를 뜻할 뿐, projective
compactification을 구성했다는 뜻이 아니다.

\[
T=\rho e^{i\psi},\quad x=s e^{i\alpha},\quad
q=r s e^{i(\psi/2+\theta)},
\]

범위는

\[
\frac15\le\rho\le\frac65,\qquad |\psi|\le\frac\pi2,
\qquad \frac12\le r\le2,\qquad |\theta|\le\frac\pi{12}
\]

이다. 정확한 leading real-action coefficient는

\[
L=\frac{\pi^2 r^2}{2\rho}\cos(3\alpha+2\theta).
\]

finite chart의 label은

\[
G:\cos\Theta\ge\frac12,\qquad
B:\cos\Theta\le-\frac12,\qquad
Z:|\cos\Theta|<\frac12
\]

이다. 결과는 \(G\)에서 \(\operatorname{Re}S_2\to+\infty\), 즉
\(|e^{-S_2}|\)의 decay를 증명한다. \(B\)에서는
\(\operatorname{Re}S_2\to-\infty\)여서 \(|e^{-S_2}|\)가 growth한다.
따라서 \(B\)는 같은 positive-\(\operatorname{Re}q\) sector에서 부호를 구분하는
false-signal control이지 admissible end가 아니다.

\(Z\)는 `UNRESOLVED_LEADING_TRANSITION_BAND`로 남겼다. 정확한 \(L\) 식은
그 안에서 양수·0·음수를 모두 취하므로 이 띠 전체에 하나의 uniform sign을 붙일 수 없다.
이는 Stokes wall 판정이 아니다. critical value, flow, singularity를 포함한 Stokes data는
계산하지 않았다.

uniform remainder ledger는

\[
C=\frac{1315433}{160},\qquad
|R|\le\pi^2 C s^4,
\]

여기에는 correction component
\(240+1920+5120=7280\), 선행 nonleading bound \(150633/160\),
그리고 \(|A|<9s/2\)가 사용됐다. \(S_0=157852\)일 때 normalized strict
margin은 \(1/75768960\)이다. 따라서 선언된 cell 전체에서 \(s\ge S_0\)이면
\(G/B\)의 부호가 균일하게 고정된다.

## 독립 수치 control

raw result는 원래 두 element를 직접 다시 합한 action을 66번 평가했다. 54개 chart
sample과
\((\psi,\alpha,\theta)\mapsto(-\psi,-\alpha,-\theta)\) 아래 별도로 평가한
12개 conjugate partner로 구성된다. 독립 read-only 감사 결과는 다음과 같다.

- (G) minimum: `4.11244517712733092914286`
- (B) maximum: `-4.11239017106762003796487`
- minimum certified-bound margin: `3.69977642616300379434887`
- maximum final leading-coefficient error: `0.0000267512624915577388678245`
- conjugation residual: `0`
- records/sequences/partners/calls: `27/54/12/66`
- fail-closed null fields: `18`

이 control들은 선언된 action algebra와 부호를 검사한다. finite chart를 source cycle,
global intersection 계산 또는 physics 결과로 바꾸지는 않는다.

## Provenance

- Raw result SHA-256: `7c8ee7416b9837d52f3d21c152c5d78a109706c4949125cc94473cf7cfdf9124`
- Input SHA-256: `2dcab3066903a855bdb85ead8add9e0f46defdaeb9e3171939f5f1bf9d694fec`
- Runner SHA-256: `377c671e89ac7b956e9153b02d12de29152640328a2b25f56d648553e8c21996`
- Raw canonical payload digest (excluding digest and timestamp):
  `aadb0a4521c6e35b6196b08d6d06a763505a7ccca397ff28b3796864483d650c`

## 해석 경계와 다음 미해결 항목

계산된 사실: 선언된 compact coordinate-ratio/phase chart 하나에서 exact \(G/B\)
action-sign bound가 성립하며, \(Z\)는 하나의 uniform sign으로 분류되지 않았다.

해석: 이는 incomplete mixed-end census에 들어갈 scoped action-sign chart 기록 하나다.
connector나 relative boundary component가 아니다.

열린 경계: compactification과 singular/Stokes data, 다른 ratio/phase/face end,
별도로 명시된 source-defined regulated cycle, 그 attachment/homotopy, orientation 및
complete signed global intersection vector는 여전히 없다. spectral, RAQ, physical,
TOE output은 모두 null이다.

[Witten](https://arxiv.org/abs/1001.2933)은 one-tail exponential-decay가 필요한
relative good-end 언어에만 사용했다. 이는 relative-cycle certificate의 충분조건이 아니다.
[Hien](https://arxiv.org/abs/math/0505474)은 아직 구성하지 않은 compactification/divisor
전제의 비교 기준으로만 사용했다. 어느 문헌도 이 model, chart, original cycle 또는 global
intersection vector를 제공하지 않는다.
