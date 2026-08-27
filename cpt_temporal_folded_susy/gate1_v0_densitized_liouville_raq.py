#!/usr/bin/env python3
"""Gate 1 -- one densitized V=0 Liouville/KL/RAQ model.

This bounded non-numbered calculation starts from the original closed-FRW
coordinates ``(Q,phi)`` but makes an explicit extra choice before quantizing:

    H = 12*pi^2*exp(3Q/2)*C
      = -2*P^2 + 3*p^2 - 72*pi^4*exp(2Q).

It applies the flat Schrodinger ordering on ``L2(dQ dphi)``, diagonalizes the
resulting exponential Liouville operator with the normalized
Kontorovich--Lebedev transform, and computes the distributional group-average
measure on the ``p>0`` zero shell.  The result is a physical Hilbert measure
only for this selected densitized operator and compact-interior spectral test
space.  It is not an ordering of raw ``C``, a proof of constraint-rescaling
invariance, an endpoint transform, a full BFV quantization, quantum gravity,
or a physics claim.  One adjacent JSON result is written and no descendant
starts.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp


INPUT_NAME = "GATE1_V0_DENSITIZED_LIOUVILLE_RAQ_INPUTS.json"
RESULT_NAME = "GATE1_V0_DENSITIZED_LIOUVILLE_RAQ_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/gate1_v0_densitized_liouville_raq.py"
EXPECTED_INPUT_SHA256 = (
    "92f340a331fb38590d64ac2c1e273dd7b17b7f7b1c91b0f2e05c8db58d1d55cd"
)
CALCULATION_ID = "Gate1V0DensitizedLiouvilleRaq"
RESULT_SCHEMA = "ice.gate1.v0-densitized-liouville-raq.result.v1"
RESULT_PREFIX = "GATE1_V0_DENSITIZED_LIOUVILLE_RAQ_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen_ids: set[str] = field(default_factory=set, repr=False)

    def register(self, check_id: str) -> None:
        if check_id in self.seen_ids:
            raise AssertionError(f"duplicate audit id: {check_id}")
        self.seen_ids.add(check_id)

    def observe(self, check_id: str, passed: bool, statement: str) -> bool:
        self.register(check_id)
        observed = bool(passed)
        self.exact.append(
            {"id": check_id, "passed": observed, "statement": statement}
        )
        return observed

    def guard(
        self,
        guard_id: str,
        theorem: str,
        hypotheses: str,
        conclusion_and_scope: str,
    ) -> None:
        self.register(guard_id)
        self.theorem_guards.append(
            {
                "id": guard_id,
                "verified": True,
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )


def verify_upstream(root: Path, item: dict[str, Any]) -> dict[str, str]:
    path = root / item["path"]
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(
            f"upstream hash mismatch for {item['path']}: {observed}"
        )
    payload = json.loads(raw)
    if payload.get("run_status") != "VALID_RUN":
        raise AssertionError(f"upstream not valid: {item['path']}")
    if payload.get("verdict") != item["required_verdict"]:
        raise AssertionError(f"upstream verdict mutation: {item['path']}")
    if (
        payload.get("result_payload_sha256_without_self")
        != item["payload_sha256_without_self"]
    ):
        raise AssertionError(f"upstream payload mutation: {item['path']}")
    return {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": payload[
            "result_payload_sha256_without_self"
        ],
        "verdict": payload["verdict"],
    }


def load_input() -> tuple[dict[str, Any], str, list[dict[str, str]]]:
    if len(sys.argv) != 1:
        raise AssertionError("this frozen calculation accepts no arguments")
    path = Path(__file__).with_name(INPUT_NAME)
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, "
            f"observed {observed}"
        )
    payload = json.loads(raw)
    if payload["schema_version"] != (
        "ice.gate1.v0-densitized-liouville-raq.input.v1"
    ):
        raise AssertionError("unexpected input schema")
    if payload["calculation_id"] != CALCULATION_ID:
        raise AssertionError("unexpected calculation identity")
    if payload["numbered_phase"] is not None:
        raise AssertionError("numbered phase mutation")
    expected_caps = {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "root_calls": 0,
        "quadratures": 0,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }
    if payload["resource_caps"] != expected_caps:
        raise AssertionError("resource cap mutation")
    expected_nulls = {
        "raw_C_operator_and_domain": None,
        "quantum_constraint_rescaling_equivalence": None,
        "exact_endpoint_state_transform": None,
        "declared_Mc_identity_equivalence": None,
        "gauge_independent_physical_inner_product": None,
        "p_zero_edge_completion": None,
        "full_bfv_trajectory_measure": None,
        "brst_cohomology": None,
        "physical_original_cycle": None,
        "global_n_sigma": None,
        "quantum_gravity_claim": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }
    if payload["required_fail_closed_outputs"] != expected_nulls:
        raise AssertionError("fail-closed output mutation")
    model = payload["declared_model"]
    if (
        model["component"] != "p>0 only"
        or "12*pi^2*exp(3Q/2)*C" not in model["positive_rescaling"]
        or "C_c^infinity" not in model["spectral_test_space"]
    ):
        raise AssertionError("declared model or branch mutation")
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    return payload, observed, upstream


def exact_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    Q, P = sp.symbols("Q P", real=True)
    p, hbar, kappa = sp.symbols("p hbar kappa", positive=True, real=True)
    pi = sp.pi

    raw_c = (
        -sp.exp(-3 * Q / 2) * P**2 / (6 * pi**2)
        + sp.exp(-3 * Q / 2) * p**2 / (4 * pi**2)
        - 6 * pi**2 * sp.exp(Q / 2)
    )
    multiplier = 12 * pi**2 * sp.exp(3 * Q / 2)
    densitized = sp.simplify(sp.expand(multiplier * raw_c))
    expected_densitized = -2 * P**2 + 3 * p**2 - 72 * pi**4 * sp.exp(2 * Q)
    densitization = audit.observe(
        "G1.densitized.classical.identity",
        sp.simplify(densitized - expected_densitized) == 0,
        "12*pi^2*exp(3Q/2)*C equals -2P^2+3p^2-72*pi^4*exp(2Q) exactly",
    )
    positive_multiplier = audit.observe(
        "G1.densitized.classical.positive_multiplier",
        multiplier.is_positive is True,
        "the declared classical rescaling multiplier is strictly positive for real Q",
    )

    z = 6 * pi**2 * sp.exp(Q) / hbar
    potential_reduction = audit.observe(
        "G1.densitized.operator.liouville_scale",
        sp.simplify(72 * pi**4 * sp.exp(2 * Q) - 2 * hbar**2 * z**2)
        == 0,
        "with z=6*pi^2*exp(Q)/hbar the exponential potential is 2*hbar^2*z^2",
    )

    k0, k1, k2 = sp.symbols("K K_z K_zz")
    bessel_residual = z**2 * k2 + z * k1 - (z**2 - kappa**2) * k0
    liouville_residual = (
        -z**2 * k2 - z * k1 + z**2 * k0 - kappa**2 * k0
    )
    bessel_eigenvalue = audit.observe(
        "G1.densitized.spectral.bessel_eigenvalue",
        sp.simplify(liouville_residual + bessel_residual) == 0,
        "the modified-Bessel equation at nu=i*kappa gives (-d_Q^2+z^2)K_{i kappa}(z)=kappa^2 K_{i kappa}(z)",
    )

    kl_norm = sp.sqrt(2 * kappa * sp.sinh(pi * kappa)) / pi
    dlmf_forward = 2 * kappa * sp.sinh(pi * kappa) / pi**2
    kl_normalization = audit.observe(
        "G1.densitized.spectral.kl_normalization",
        sp.simplify(dlmf_forward - kl_norm**2) == 0,
        "the symmetric kernel normalization squared equals the DLMF forward-transform coefficient",
    )
    kl_inverse_cancellation = audit.observe(
        "G1.densitized.spectral.kl_inverse_cancellation",
        sp.simplify(kl_norm * (1 / kl_norm) - 1) == 0,
        "writing f_DLMF=kl_norm*A and K=chi/kl_norm converts the DLMF inverse into g=integral A*chi d kappa",
    )

    spectral_value = 3 * p**2 - 2 * hbar**2 * kappa**2
    kappa_zero = sp.sqrt(sp.Rational(3, 2)) * p / hbar
    zero_shell = audit.observe(
        "G1.densitized.raq.simple_positive_zero",
        sp.simplify(spectral_value.subs(kappa, kappa_zero)) == 0
        and kappa_zero.is_positive is True,
        "on p>0 the spectral multiplier has the unique positive zero kappa_0=sqrt(3/2)*p/hbar",
    )
    derivative_magnitude = sp.simplify(4 * hbar**2 * kappa_zero)
    coarea_denominator = 2 * sp.sqrt(6) * hbar * p
    coarea = audit.observe(
        "G1.densitized.raq.coarea_factor",
        sp.simplify(derivative_magnitude - coarea_denominator) == 0,
        "|d_kappa(3p^2-2hbar^2*kappa^2)| at the positive root is 2*sqrt(6)*hbar*p",
    )
    physical_weight = sp.simplify(1 / derivative_magnitude)
    positive_weight = audit.observe(
        "G1.densitized.raq.positive_weight",
        physical_weight.is_positive is True
        and sp.simplify(
            physical_weight - 1 / (2 * sp.sqrt(6) * hbar * p)
        )
        == 0,
        "the selected group average induces the positive measure dp/(2*sqrt(6)*hbar*p)",
    )

    amplitude_1 = p * sp.exp(-p)
    amplitude_2 = p**2 * sp.exp(-p)
    phys_norm_1 = sp.integrate(
        amplitude_1**2 * physical_weight, (p, 0, sp.oo)
    )
    phys_norm_2 = sp.integrate(
        amplitude_2**2 * physical_weight, (p, 0, sp.oo)
    )
    dp_norm_1 = sp.integrate(amplitude_1**2, (p, 0, sp.oo))
    dp_norm_2 = sp.integrate(amplitude_2**2, (p, 0, sp.oo))
    witness_norms = audit.observe(
        "G1.densitized.raq.two_positive_witness_norms",
        sp.simplify(phys_norm_1 - 1 / (8 * sp.sqrt(6) * hbar)) == 0
        and sp.simplify(phys_norm_2 - 3 / (16 * sp.sqrt(6) * hbar))
        == 0
        and phys_norm_1.is_positive is True
        and phys_norm_2.is_positive is True,
        "the amplitudes p*exp(-p) and p^2*exp(-p) have finite strictly positive physical norms",
    )
    nonconstant_dp_ratio = audit.observe(
        "G1.densitized.comparison.dp_not_identity_measure",
        sp.simplify(phys_norm_1 / dp_norm_1 - phys_norm_2 / dp_norm_2)
        != 0,
        "two witness ratios differ, so the derived dp/p measure is not the prior dp fiber up to one state-independent constant",
    )
    reweight = sp.sqrt(physical_weight)
    unitary_reweight = audit.observe(
        "G1.densitized.comparison.explicit_unitary_reweight",
        sp.simplify(reweight**2 - physical_weight) == 0,
        "J A=A/sqrt(2*sqrt(6)*hbar*p) is an isometry from the weighted physical space to abstract L2(dp)",
    )
    p_zero_edge = audit.observe(
        "G1.densitized.boundary.p_zero_singular",
        sp.limit(physical_weight, p, 0, dir="+") == sp.oo
        and sp.limit(derivative_magnitude, p, 0, dir="+") == 0,
        "the coarea root ceases to be simple at p=0 and the weight diverges, so the compact-interior result cannot include that edge",
    )

    x, y = sp.symbols("x y", real=True)
    y = sp.Symbol("y", positive=True, real=True)
    spectral_z = x + sp.I * y
    resolvent = 1 / (spectral_value - spectral_z)
    resolvent_identity = audit.observe(
        "G1.densitized.operator.real_multiplier_resolvent",
        sp.simplify((spectral_value - spectral_z) * resolvent - 1) == 0
        and sp.conjugate(spectral_value) == spectral_value,
        "the KL-Fourier spectral value is real and its nonreal resolvent satisfies the multiplication identity",
    )

    audit.guard(
        "G1.densitized.guard.kl_plancherel",
        "Kontorovich-Lebedev inversion and Plancherel theorem with the DLMF 10.43.30-31 normalization",
        "z maps R_Q bijectively to R_+, dQ=dz/z, chi_kappa=sqrt(2*kappa*sinh(pi*kappa))/pi*K_{i kappa}(z), kappa>0, and compact-interior smooth spectral tests satisfy the transform hypotheses",
        "the normalized KL transform selects a unitary spectral realization L_KL=K^{-1}M_{kappa^2}K on L2(R,dQ); this is one selected realization, not a raw-C ordering or endpoint transform",
    )
    audit.guard(
        "G1.densitized.guard.real_multiplication_self_adjoint",
        "maximal real multiplication-operator theorem",
        "the normalized KL transform and hbar-Fourier transform give L2(dkappa dp), the multiplier 3p^2-2hbar^2*kappa^2 is real measurable, and the maximal domain requires multiplier times amplitude in L2",
        "the selected densitized H_hat is self-adjoint by spectral definition on the p>0 invariant sector; no raw-C domain or rescaling equivalence follows",
    )
    audit.guard(
        "G1.densitized.guard.single_constraint_group_average",
        "spectral theorem and the distributional identity integral dN/(2*pi*hbar) exp(-i*N*lambda/hbar)=delta(lambda)",
        "test amplitudes are smooth and compactly supported inside kappa>0,p>0, the zero is simple there, and the coarea derivative was computed exactly",
        "the rigging form reduces to integral_0^infinity dp conjugate(A(kappa_0,p))*B(kappa_0,p)/(2*sqrt(6)*hbar*p), whose null quotient completes to the recorded weighted L2 space",
    )
    audit.guard(
        "G1.densitized.guard.rescaling_noninvariance",
        "constraint-rescaling boundary in refined algebraic quantization",
        "H is obtained from C by a nonconstant Q-dependent positive classical multiplier before ordering, while no self-adjoint raw-C operator or unitary intertwiner was constructed",
        "classical zero-set equality does not establish quantum equivalence; the physical measure belongs only to the selected H_hat model",
    )
    audit.guard(
        "G1.densitized.guard.not_full_quantum_gravity",
        "model-scope separation",
        "only homogeneous a/phi variables, one Hamiltonian constraint, one branch, and no inhomogeneous metric modes, constraint algebra, renormalization, gravitons, or observables were included",
        "the result is an exactly solvable constrained quantum-cosmology workbench model, not a quantization of general relativity, quantum gravity evidence, physics, or a TOE result",
    )

    flags = {
        "classical_densitization": densitization,
        "positive_multiplier": positive_multiplier,
        "liouville_scale": potential_reduction,
        "bessel_eigenvalue": bessel_eigenvalue,
        "kl_normalization": kl_normalization,
        "kl_inverse": kl_inverse_cancellation,
        "simple_positive_zero": zero_shell,
        "coarea_factor": coarea,
        "positive_weight": positive_weight,
        "positive_witness_norms": witness_norms,
        "dp_measure_distinction": nonconstant_dp_ratio,
        "unitary_reweight": unitary_reweight,
        "p_zero_excluded": p_zero_edge,
        "spectral_resolvent": resolvent_identity,
    }
    return (
        {
            "classical_and_ordering": {
                "raw_constraint_C": str(raw_c),
                "positive_multiplier": str(multiplier),
                "densitized_constraint_H": str(densitized),
                "auxiliary_space": "L2(R_Q times R_phi,dQ dphi)",
                "ordered_differential_expression": "H_hat=2*hbar^2*d_Q^2-3*hbar^2*d_phi^2-72*pi^4*exp(2Q)",
                "formal_test_core": "C_c^infinity(R_Q times R_phi)",
                "raw_C_operator_and_domain": None,
                "quantum_constraint_rescaling_equivalence": None,
            },
            "kl_spectral_realization": {
                "coordinate": "z=6*pi^2*exp(Q)/hbar",
                "measure_change": "dQ=dz/z",
                "liouville_operator": "L=-d_Q^2+z^2",
                "generalized_eigenfunction": "K_{i*kappa}(z)",
                "eigenvalue": "kappa^2",
                "normalized_kernel": "chi_kappa(z)=sqrt(2*kappa*sinh(pi*kappa))/pi*K_{i*kappa}(z)",
                "spectral_space": "L2(R_{+,kappa} times R_{+,p},d kappa dp)",
                "densitized_constraint_multiplier": str(spectral_value),
                "maximal_domain": "{A in L2: (3p^2-2hbar^2*kappa^2)A in L2}",
                "self_adjoint_selected_realization": all(
                    flags[key]
                    for key in (
                        "liouville_scale",
                        "bessel_eigenvalue",
                        "kl_normalization",
                        "kl_inverse",
                        "spectral_resolvent",
                    )
                ),
            },
            "selected_raq_physical_space": {
                "group_average": "eta(A)[B]=integral dN/(2*pi*hbar)<A,exp(-i*N*H_hat/hbar)B>",
                "zero_root": "kappa_0(p)=sqrt(3/2)*p/hbar",
                "simple_root_derivative": str(derivative_magnitude),
                "rigging_form": "integral_0^infinity dp conjugate(A(kappa_0(p),p))*B(kappa_0(p),p)/(2*sqrt(6)*hbar*p)",
                "null_space": "spectral tests whose restriction to kappa=kappa_0(p) vanishes",
                "physical_hilbert_space": "L2((0,infinity)_p,dp/(2*sqrt(6)*hbar*p))",
                "test_space_scope": "compactly supported away from p=0 and kappa=0 before quotient/completion",
                "positive": positive_weight and witness_norms,
                "witness_1_norm_squared": str(phys_norm_1),
                "witness_2_norm_squared": str(phys_norm_2),
                "p_zero_edge_completion": None,
            },
            "comparison_with_declared_Mc_fiber": {
                "prior_declared_form": "integral_0^infinity dp conjugate(psi(0,p))*varphi(0,p)",
                "derived_densitized_form_measure": "dp/(2*sqrt(6)*hbar*p)",
                "identity_normalization_equivalence": False,
                "abstract_unitary_map_to_L2_dp": "(J A)(p)=A(p)/sqrt(2*sqrt(6)*hbar*p)",
                "declared_Mc_identity_equivalence": None,
                "meaning": "abstract Hilbert-space isomorphism does not supply the missing exact endpoint transform or prove constraint-rescaling invariance",
            },
            "flags": flags,
        },
        flags,
    )


def build_result(
    frozen_input: dict[str, Any],
    input_sha256: str,
    upstream: list[dict[str, str]],
    audit: Audit,
) -> dict[str, Any]:
    exact, flags = exact_calculation(audit)
    algebra_keys = (
        "classical_densitization",
        "positive_multiplier",
        "liouville_scale",
        "bessel_eigenvalue",
        "kl_normalization",
        "kl_inverse",
        "simple_positive_zero",
        "coarea_factor",
        "positive_weight",
        "positive_witness_norms",
        "spectral_resolvent",
    )
    boundary_keys = (
        "dp_measure_distinction",
        "unitary_reweight",
        "p_zero_excluded",
    )
    if all(flags.values()):
        verdict = "KEEP_V0_ONE_DENSITIZED_LIOUVILLE_KL_RAQ_MODEL"
        impact = (
            "CLOSE_ONE_EXPLICITLY_RESCALED_ORDER_FIXED_QUANTUM_COSMOLOGY_MODEL_ONLY"
        )
        classification = (
            "GATE1_V0_ONE_DENSITIZED_ORIGINAL_COORDINATE_KL_SPECTRAL_"
            "REALIZATION_AND_WEIGHTED_RAQ_PHYSICAL_FIBER_KEEP_RAW_C_"
            "RESCALING_EQUIVALENCE_BFV_QUANTUM_GRAVITY_AND_PHYSICS_OPEN"
        )
        condition = (
            "the densitization, Bessel eigenvalue, KL normalization, spectral "
            "multiplier, positive root and coarea weight all pass under the "
            "declared test-space and theorem hypotheses"
        )
    elif all(flags[key] for key in algebra_keys) and not all(
        flags[key] for key in boundary_keys
    ):
        verdict = "KILL_V0_RAQ_MEASURE_OR_RESCALING_SHORTCUT"
        impact = (
            "RETAIN_THE_FORMAL_DIFFERENTIAL_REDUCTION_WITHOUT_A_PHYSICAL_MEASURE_CLAIM"
        )
        classification = "GATE1_V0_DENSITIZED_RAQ_MEASURE_BOUNDARY_NONPASS"
        condition = (
            "the result silently identifies the weighted measure with dp, "
            "includes p=0, or fails the explicit unitary-reweight boundary"
        )
    else:
        verdict = "KILL_V0_DENSITIZED_LIOUVILLE_RAQ_MODEL"
        impact = "RETAIN_PRIOR_LOCAL_MC_REPRESENTATION_ONLY"
        classification = "GATE1_V0_DENSITIZED_LIOUVILLE_SPECTRAL_ALGEBRA_NONPASS"
        condition = (
            "a densitization, Liouville/Bessel, KL, root, coarea, positivity "
            "or witness check fails"
        )

    promoted = dict(frozen_input["required_fail_closed_outputs"])
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "classification": classification,
        "verdict": verdict,
        "programme_impact": impact,
        "input": {"path": INPUT_RELPATH, "sha256": input_sha256},
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "upstream_provenance": upstream,
        "exact_calculation": exact,
        "exact_checks": audit.exact,
        "theorem_guards": audit.theorem_guards,
        "numerical_checks": [],
        "decision_trace": {
            "matched_predeclared_condition": condition,
            "scope_meaning": "one explicitly densitized and order-fixed homogeneous V=0 constrained quantum model on p>0 only",
            "primary_source_boundary": "DLMF supplies the special-function transform and RAQ sources supply the framework; all cosmological specialization, algebra, coarea weight and scope decisions are repository workbench results",
        },
        "computed_scope": frozen_input["computed_scope"],
        "not_computed": frozen_input["not_computed"],
        "promoted_outputs": promoted,
        "gate1_decision": promoted["gate1"],
        "global_promotion": promoted["global_promotion"],
        "automatic_next": promoted["automatic_next"],
        "resource_accounting": {
            "root_calls": 0,
            "quadratures": 0,
            "ode_calls": 0,
            "automatic_descendants": 0,
            "adjacent_result_files": 1,
            "artifact_cap_bytes": ARTIFACT_CAP_BYTES,
        },
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "platform": platform.platform(),
        },
        "frozen_input_contract": {
            "question": frozen_input["question"],
            "kind": frozen_input["kind"],
            "epistemic_scope": frozen_input["epistemic_scope"],
            "decision_table": frozen_input["decision_table"],
            "primary_sources": frozen_input["primary_sources"],
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    return result


def main() -> None:
    frozen_input, input_sha256, upstream = load_input()
    audit = Audit()
    result = build_result(frozen_input, input_sha256, upstream, audit)
    encoded = json.dumps(
        result,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8") + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact exceeds the bounded cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "classification": result["classification"],
                "verdict": result["verdict"],
                "programme_impact": result["programme_impact"],
                "exact_checks_passed": sum(item["passed"] for item in audit.exact),
                "exact_checks_total": len(audit.exact),
                "theorem_guards_verified": len(audit.theorem_guards),
                "numerical_checks_total": 0,
                "selected_physical_measure": "dp/(2*sqrt(6)*hbar*p)",
                "raw_C_operator_and_domain": None,
                "quantum_gravity_claim": None,
                "physics_claim": None,
                "TOE_claim": None,
                "gate1": result["gate1_decision"],
                "automatic_next": None,
                "result": RESULT_NAME,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
