# Gate 1 — densitized \(V=0\) RAQ의 \(p=0\) 경계

## 결과

이미 선택된 densitized \(\widehat H\)의 양의 \(p>0\) group average는 \(p=0\)에서
0이 아닌 진폭을 포함하는 순진한 폐경계 테스트 공간으로 자동 연장되지 않는다.
정확한 cutoff 계산에서 그 진폭의 norm은 로그 발산하고, 유한부를 택하려면 기준
운동량을 추가로 골라야 한다. 반면 \(p\)에 비례해 사라지는 witness는 같은 양의
측도에서 유한하다.

고정 판정은 다음과 같다.

```text
NARROW_V0_P_ZERO_STANDARD_GROUP_AVERAGE_REQUIRES_EXTRA_EDGE_DATA
```

이는 하나의 선택된 densitized \(H\) 스펙트럴 모델에 대한 경계 판정이다. raw
\(C\)의 양자 연산자·domain·inner product, \(C\leftrightarrow H\) 양자 동치, endpoint
transform, lapse contour, full BFV measure, 물리학 또는 TOE 주장을 만들지 않는다.

## 고정된 입력과 cutoff 유도

상류 결과가 고정한 Fourier--Kontorovich--Lebedev multiplier는

\[
h(\kappa,p)=3p^2-2\hbar^2\kappa^2,
\qquad
\kappa_0(p)=\sqrt{\frac32}\frac p\hbar,
\]

이며, open \(p>0\) component에서의 shell measure는

\[
\frac{dp}{2\sqrt6\,\hbar p}.
\]

이를 경계에서 부당하게 distribution으로 연장하지 않도록, 먼저 \(p\geq
\epsilon>0\)로 자른다. \(x=\sqrt3p\), \(y=\sqrt2\hbar\kappa\) 및
\(u=x+y\), \(v=x-y\)이면

\[
h=x^2-y^2=uv,
\qquad dx\,dy=\sqrt6\hbar\,dp\,d\kappa,
\qquad dx\,dy=\tfrac12du\,dv.
\]

이는 원점에서 \(\delta(uv)\) 항등식을 주장하는 계산이 아니다. cutoff된 양의
zero ray에서만 coarea를 적용해 위 \(dp/p\) 측도를 얻는다. 따라서 원점 문제는
좌표 변환의 형식적 산물이 아니라, 이미 선택된 interior measure의 실제 경계 거동이다.

## 계산된 사실

비영 edge witness \(A_0(p)=e^{-p}\)에 대해

\[
\eta_\epsilon[A_0,A_0]
=\frac{E_1(2\epsilon)}{2\sqrt6\,\hbar}
=\frac{\log(1/\epsilon)-\gamma-\log 2+o(1)}
       {2\sqrt6\,\hbar}.
\]

따라서 \(\epsilon\to0^+\)에서 coefficient
\(1/(2\sqrt6\hbar)\)의 로그 발산이 있다. 정확한 \(E_1\) 항등식과 독립
80-decimal quadrature는 \(\epsilon=10^{-2},10^{-4},10^{-6}\)에서 일치했다.
6-decade 증가율도 이 coefficient로 수렴했다.

대조적으로 선형 소멸 witness \(A_1(p)=pe^{-p}\)는

\[
\eta[A_1,A_1]
=\int_0^\infty\frac{p^2e^{-2p}}{2\sqrt6\,\hbar p}\,dp
=\frac1{8\sqrt6\,\hbar}>0
\]

로 유한하다. 일반적으로 \(A=O(p^\alpha)\)이면 integrand는
\(O(p^{2\alpha-1})\)이므로 \(\alpha>0\)가 이 국소 criterion을 만족한다.

유한부도 자동으로 정해지지 않는다. 양의 기준 운동량 \(p_\star\)로

\[
\operatorname{FP}_{p_\star}=
\lim_{\epsilon\to0^+}\left[
\eta_\epsilon[A_0,A_0]
-\frac{\log(p_\star/\epsilon)}{2\sqrt6\,\hbar}\right]
=\frac{-\gamma-\log(2p_\star)}{2\sqrt6\,\hbar}
\]

를 정의할 수 있지만, 다른 \(q_\star\)는
\(\log(q_\star/p_\star)/(2\sqrt6\hbar)\)만큼 다른 값을 준다. cutoff 자체는
그 reference scale, origin-supported sector, counterterm, 또는 superselection rule을
선택하지 않는다.

## 해석과 남은 경계

이 결과가 닫는 것은 “표준 양의 group average가 추가 선택 없이 \(p=0\)까지
포함한다”는 shortcut뿐이다. computed fact는 nonzero-edge norm의 발산, vanishing
witness의 유한성, 그리고 finite-part scale ambiguity이다. 해석상 \(p=0\) completion에는
추가 edge data가 필요하다고만 말할 수 있다.

다음은 계속 열려 있다.

- raw \(C\)의 ordering, self-adjoint domain, rigging map과 physical inner product
- raw \(C\), densitized \(H\), 선언된 \(M_c\) representation 사이의 양자 동치
- canonical \(p=0\) counterterm 또는 origin sector, \(p<0\) 및 both-branch completion
- lapse contour/modulus, zero-lapse contact term, full BFV trajectory measure와 BRST cohomology
- global cycle, quantum gravity, physics 및 TOE 주장

## 재현 기록

관측된 committed 실행은 다음과 같다.

```text
./ice run gate1_v0_densitized_raq_p_zero_boundary
VALID_RUN; 10/10 exact checks; 5/5 numerical checks; 6 theorem guards

./ice repro --only gate1_v0_densitized_raq_p_zero_boundary
REPRO; 1 checked; 0 needs-attention

npm run check
67/67 tests passed
```

입력·실행체·raw result는 각각
`GATE1_V0_DENSITIZED_RAQ_P_ZERO_BOUNDARY_INPUTS.json`,
`gate1_v0_densitized_raq_p_zero_boundary.py`,
`GATE1_V0_DENSITIZED_RAQ_P_ZERO_BOUNDARY_RESULT.json`이다.
