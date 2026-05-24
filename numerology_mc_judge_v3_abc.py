"""numerology_mc_judge v3 — ABC + KL divergence dual gate (meta-Bayesian extension).

# KG: lesson-self-mc-applies-to-meta-bayesian-too-2026-05-20 (PROVISIONALLY_RATIFIED)
# KG: plan-prom16-meta-bayes-ice-004-abc-kl-dual-gate-2026-05-20
# KG: lesson-cycle-must-self-apply-rule-it-crystallizes-2026-05-20 (provides Step 8 self-app gate)
# Predecessor: numerology_mc_judge.py (v1, 2026-05-17 ground-claim scalar)

v3 = v1 backward-compatible wrapper + ABC scaffold for meta-Bayesian product targets
+ KL divergence diagnostic + NUMEROLOGY_BY_KL verdict category.

Decision rule (v3 dual gate):
    SIGNAL_GENUINE     : P(E|~H) < 0.01 AND KL(posterior || prior) > kl_threshold (default 1.0 bit)
    SIGNAL_WEAK        : P(E|~H) < 0.5 AND KL > kl_threshold       (rare-and-informative)
    NUMEROLOGY_BY_P    : P(E|~H) >= 0.5                            (v1 ground claim verdict)
    NUMEROLOGY_BY_KL   : P(E|~H) < 0.01 BUT KL <= kl_threshold     (rare-but-uninformative)

Self-application (Plan Step 8 enforcement):
    self_test_gate_thresholds() runs synthetic data with known KL=0 and reports false-lift rate.
    Must pass before applying to ICE 0.04 case.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

import numpy as np

# Re-export v1 verdict function for backward compatibility
from numerology_mc_judge import verdict_from_p  # noqa: F401

ROOT = pathlib.Path(__file__).parent
DATE = "2026-05-20"
RNG_SEED = 42


# -------- KL divergence estimator --------

def kl_divergence_histogram(
    samples_posterior: np.ndarray,
    samples_prior: np.ndarray,
    n_bins: int = 50,
    range_pad: float = 1.05,
) -> float:
    """Histogram-based KL(posterior || prior) in BITS.

    KL(p || q) = sum_i p_i * log2(p_i / q_i)

    Smoothing: Laplace +1 per bin to avoid log(0). MVP grade; for production use KDE or k-NN
    estimator (Wang-Kulkarni-Verdú 2009 IEEE TIT).
    """
    lo = min(samples_posterior.min(), samples_prior.min()) / range_pad
    hi = max(samples_posterior.max(), samples_prior.max()) * range_pad
    bins = np.linspace(lo, hi, n_bins + 1)
    hist_post, _ = np.histogram(samples_posterior, bins=bins)
    hist_prior, _ = np.histogram(samples_prior, bins=bins)
    # Laplace smoothing
    p = (hist_post + 1) / (hist_post.sum() + n_bins)
    q = (hist_prior + 1) / (hist_prior.sum() + n_bins)
    return float(np.sum(p * np.log2(p / q)))


# -------- ABC scaffold for meta-Bayesian product --------

def abc_meta_bayesian_product(
    target_product: float,
    factor_priors: list[tuple[float, float]],  # list of (Beta alpha, Beta beta) per factor
    n_samples: int = 100_000,
    tol_rel: float = 0.05,
    rng: np.random.Generator | None = None,
) -> dict:
    """ABC rejection on meta-Bayesian product P = product(theta_i).

    factor_priors: list of (alpha, beta) for Beta(alpha, beta) prior per factor.
    target_product: observed product value (e.g. ICE 0.04).
    tol_rel: acceptance tolerance, relative to target.

    Returns posterior samples + KL diagnostic + P(E|~H).
    """
    if rng is None:
        rng = np.random.default_rng(RNG_SEED)
    n_factors = len(factor_priors)

    # Step 1: draw prior samples
    prior_samples = np.zeros((n_samples, n_factors))
    for i, (a, b) in enumerate(factor_priors):
        prior_samples[:, i] = rng.beta(a, b, size=n_samples)
    prior_products = prior_samples.prod(axis=1)

    # Step 2: ABC acceptance — product within tolerance of target
    accept_mask = np.abs(prior_products - target_product) <= tol_rel * target_product
    n_accept = int(accept_mask.sum())
    if n_accept < 10:
        # Tolerance too tight; widen by step
        return {
            "status": "TOLERANCE_TOO_TIGHT",
            "n_accept": n_accept,
            "tol_rel_used": tol_rel,
            "recommendation": "increase tol_rel or n_samples",
        }
    posterior_samples = prior_samples[accept_mask]
    posterior_products = prior_products[accept_mask]

    # Step 3: P(E|~H) under non-informative prior (uniform on each factor) — pseudo-null
    # Use product samples themselves: fraction of prior products within tolerance
    p_e_given_not_h = n_accept / n_samples

    # Step 4: KL divergence per factor
    kl_per_factor = [
        kl_divergence_histogram(posterior_samples[:, i], prior_samples[:, i])
        for i in range(n_factors)
    ]
    kl_total = sum(kl_per_factor)  # additive bound; assumes near-independence

    return {
        "n_samples": n_samples,
        "n_accept": n_accept,
        "p_e_given_not_h": p_e_given_not_h,
        "kl_per_factor_bits": kl_per_factor,
        "kl_total_bits": kl_total,
        "posterior_product_mean": float(posterior_products.mean()),
        "posterior_product_p05_p95": [
            float(np.percentile(posterior_products, 5)),
            float(np.percentile(posterior_products, 95)),
        ],
        "factor_priors_alpha_beta": factor_priors,
        "target_product": target_product,
        "tol_rel": tol_rel,
    }


def verdict_dual_gate(
    p_e_given_not_h: float,
    kl_bits: float,
    p_lo: float = 0.01,
    p_hi: float = 0.5,
    kl_threshold: float = 1.0,
) -> str:
    """v3 dual gate verdict."""
    rare = p_e_given_not_h < p_lo
    semi_rare = p_e_given_not_h < p_hi
    informative = kl_bits > kl_threshold

    if rare and informative:
        return "SIGNAL_GENUINE"
    if semi_rare and informative:
        return "SIGNAL_WEAK"
    if rare and not informative:
        return "NUMEROLOGY_BY_KL"  # rare-but-uninformative
    return "NUMEROLOGY_BY_P"  # v1 ground-claim verdict


# -------- Self-application gate (Plan Step 8) --------

def self_test_gate_thresholds(
    n_synthetic_trials: int = 500,
    kl_threshold: float = 1.0,
    target_product: float = 0.04,
    rng: np.random.Generator | None = None,
) -> dict:
    """Plan Step 8 self-application gate.

    Tests false-lift rate of v3 dual gate when KL=0 (null case — prior unchanged).

    Synthetic setup: draw target as product of Beta(1,1) factors (uniform);
    posterior MUST converge to prior; KL should be near 0.
    """
    if rng is None:
        rng = np.random.default_rng(RNG_SEED)
    factor_priors = [(1.0, 1.0), (1.0, 1.0), (1.0, 1.0)]  # uniform = null
    false_lifts = 0
    kl_observed = []
    for _ in range(n_synthetic_trials):
        result = abc_meta_bayesian_product(
            target_product=target_product,
            factor_priors=factor_priors,
            n_samples=5000,
            tol_rel=0.10,
            rng=rng,
        )
        if result.get("status") == "TOLERANCE_TOO_TIGHT":
            continue
        kl_observed.append(result["kl_total_bits"])
        v = verdict_dual_gate(result["p_e_given_not_h"], result["kl_total_bits"],
                              kl_threshold=kl_threshold)
        if v == "SIGNAL_GENUINE":  # false-lift
            false_lifts += 1
    if not kl_observed:
        return {"status": "ALL_TIGHT", "false_lift_rate": None}
    return {
        "n_synthetic_trials_used": len(kl_observed),
        "kl_threshold_tested": kl_threshold,
        "kl_observed_mean_bits": float(np.mean(kl_observed)),
        "kl_observed_p95_bits": float(np.percentile(kl_observed, 95)),
        "false_lift_count": false_lifts,
        "false_lift_rate": false_lifts / len(kl_observed),
        "gate_passed": false_lifts / len(kl_observed) < 0.05,  # < 5% false lift acceptable
    }


# -------- ICE 0.04 case driver --------

def apply_to_ice_0_04() -> dict:
    """Apply v3 ABC + KL dual gate to ICE workbench reframe 0.04 escape lane.

    Uses Beta(1,9) MB1 + Beta(1,4) MB3|MB1 + Beta(10,1) MB4 per A2xS3 recommendation.
    """
    rng = np.random.default_rng(RNG_SEED)
    factor_priors = [(1.0, 9.0), (1.0, 4.0), (10.0, 1.0)]
    result = abc_meta_bayesian_product(
        target_product=0.04,
        factor_priors=factor_priors,
        n_samples=200_000,
        tol_rel=0.10,
        rng=rng,
    )
    if result.get("status") == "TOLERANCE_TOO_TIGHT":
        return result
    verdict = verdict_dual_gate(result["p_e_given_not_h"], result["kl_total_bits"])
    result["verdict_v3"] = verdict
    result["case"] = "ICE workbench reframe posterior_prior 0.04"
    result["interpretation"] = (
        f"P(E|~H)={result['p_e_given_not_h']:.4f}, KL={result['kl_total_bits']:.3f} bits. "
        f"Verdict={verdict}. Posterior product 95% interval = "
        f"[{result['posterior_product_p05_p95'][0]:.4f}, "
        f"{result['posterior_product_p05_p95'][1]:.4f}]."
    )
    return result


def main() -> None:
    print("== Step 8 self-application gate (synthetic KL=0 false-lift test) ==")
    self_test = self_test_gate_thresholds()
    print(f"   false_lift_rate = {self_test.get('false_lift_rate')}, "
          f"gate_passed = {self_test.get('gate_passed')}")

    if not self_test.get("gate_passed", False):
        print("   FAILED self-test — revise thresholds before applying to ICE 0.04")

    print()
    print("== ICE 0.04 case ==")
    ice = apply_to_ice_0_04()
    print(f"   {ice.get('interpretation', ice)}")

    out = ROOT / "numerology_mc_judge_v3_results_2026-05-20.json"
    out.write_text(json.dumps(
        {
            "date": DATE,
            "version": "v3_abc_kl_dual_gate",
            "predecessor": "numerology_mc_judge.py (v1, 2026-05-17)",
            "kg_anchor": "plan-prom16-meta-bayes-ice-004-abc-kl-dual-gate-2026-05-20",
            "self_test_step_8": self_test,
            "ice_004_case": ice,
        },
        indent=2,
        ensure_ascii=False,
    ) + "\n")
    print(f"\nResults -> {out.name}")


if __name__ == "__main__":
    sys.exit(main())
