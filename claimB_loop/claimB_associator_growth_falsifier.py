#!/usr/bin/env python3
"""Claim B cheapest decisive falsifier (PROM 16 proof-path, 2026-06-08).

질문: 무한 CD tower의 "결합법칙 깨짐"이 레벨마다 *심해지는가*? (사용자 직관 "무한히
새로운/강해지는 법칙붕괴 history의 경로적분 = 중력"의 정량적 핵심 동력)

시험: 결합자 [x,y,z] = (xy)z - x(yz) 의 노름이 CD 레벨 n (dim 2^n) 에서
어떻게 변하는가. 만약 norm 이 지수증가하면 path integral Σ w_n S_n 수렴에
지수감쇠 가중 w_n=e^{-λn} 이 강제되고 λ가 자유 파라미터가 되어 예측력 0.
만약 포화(flat)면 "무한히 심해지는 history" 자체가 부재.

결과 (직접 실행): basis-element 결합자 노름 = **flat 2.0** at dim 8/16/32.
늘어나는 것은 노름 *크기*가 아니라 비영 결합자 *개수*(168→1848→15960)뿐.
→ 정량적 "무한 history" 부재. ICE KG `associator_mass_verification_result`
   (2026-02-02, 가설 기각, "모든 비영 결합자 노름=2") 와 독립 일치.

이는 Claim B 의 path-integral 동력 가설에 대한 NEGATIVE (FALSIFIES the
"increasing breaking" quantitative engine). Wilmot 2025 안정화 정리(n>=4
질적 포화)의 계산적 확증이기도 하다. 신화 layer(USER_PRIMARY)와 독립.
"""
import itertools, math


def conj(x):
    if len(x) == 1:
        return [x[0]]
    h = len(x) // 2
    return conj(x[:h]) + [-v for v in x[h:]]


def cd_mul(a, b):
    """Cayley-Dickson product via recursive doubling: (a1,a2)(b1,b2)
       = (a1 b1 - conj(b2) a2, b2 a1 + a2 conj(b1))."""
    n = len(a)
    if n == 1:
        return [a[0] * b[0]]
    m = n // 2
    a1, a2, b1, b2 = a[:m], a[m:], b[:m], b[m:]
    add = lambda x, y: [p + q for p, q in zip(x, y)]
    sub = lambda x, y: [p - q for p, q in zip(x, y)]
    z1 = sub(cd_mul(a1, b1), cd_mul(conj(b2), a2))
    z2 = add(cd_mul(b2, a1), cd_mul(a2, conj(b1)))
    return z1 + z2


def assoc(x, y, z):
    return [p - q for p, q in zip(cd_mul(cd_mul(x, y), z), cd_mul(x, cd_mul(y, z)))]


def basis(n, i):
    v = [0.0] * n
    v[i] = 1.0
    return v


def norm(v):
    return math.sqrt(sum(t * t for t in v))


def main():
    print("CD level (dim) | nonzero-assoc basis triples | distinct nonzero ||assoc|| values")
    for k, dim in [(3, 8), (4, 16), (5, 32)]:
        vals, nz = set(), 0
        for i, j, m in itertools.product(range(dim), repeat=3):
            a = assoc(basis(dim, i), basis(dim, j), basis(dim, m))
            nm = norm(a)
            if nm > 1e-9:
                nz += 1
                vals.add(round(nm, 6))
        print(f"  level {k} (dim {dim:2d}) | {nz:6d} | {sorted(vals)}")
    print("\nVERDICT: ||associator|| is FLAT (=2.0) across levels — no growth mode.")
    print("Only the COUNT of nonzero associators grows. No quantitative 'infinite")
    print("intensifying breaking history' → Claim B path-integral engine FALSIFIED.")
    print("Concurs with KG associator_mass_verification_result (2026-02-02, rejected).")


if __name__ == "__main__":
    main()
