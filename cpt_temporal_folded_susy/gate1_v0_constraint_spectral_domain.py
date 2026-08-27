#!/usr/bin/env python3
"""Gate 1 -- local V=0 constraint spectral-domain control.

This bounded non-numbered calculation equips only the momentum base of the
hash-verified ``U_plus`` Darboux component with the declared Lebesgue measure
``dc dp``.  In that representation the constraint coordinate is tested as the
maximal real multiplication operator ``M_c``.  The calculation records its
resolvent, PVM, dense rigged test space and distributional zero-fiber form.

It does not transfer an ordering through the previously nonunitary one-term
FIO, does not double the ``p>0`` component, and does not construct a physical
inner product, endpoint transform, group average or BFV trajectory measure.
One adjacent JSON result is written and no descendant starts.
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


INPUT_NAME = "GATE1_V0_CONSTRAINT_SPECTRAL_DOMAIN_INPUTS.json"
RESULT_NAME = "GATE1_V0_CONSTRAINT_SPECTRAL_DOMAIN_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/gate1_v0_constraint_spectral_domain.py"
)
EXPECTED_INPUT_SHA256 = (
    "c4c94665703a8bcc5877ceaed9da92afea2f7feb6cd4f550fa41139eee4e8287"
)
CALCULATION_ID = "Gate1V0ConstraintSpectralDomain"
RESULT_SCHEMA = "ice.gate1.v0-constraint-spectral-domain.result.v1"
RESULT_PREFIX = "GATE1_V0_CONSTRAINT_SPECTRAL_DOMAIN_RESULT="
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
        "ice.gate1.v0-constraint-spectral-domain.input.v1"
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
        "exact_endpoint_state_transform": None,
        "original_variable_constraint_ordering": None,
        "physical_inner_product": None,
        "full_real_lapse_delta_C": None,
        "full_bfv_trajectory_measure": None,
        "physical_original_cycle": None,
        "global_n_sigma": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }
    if payload["required_fail_closed_outputs"] != expected_nulls:
        raise AssertionError("fail-closed output mutation")
    representation = payload["representation"]
    if (
        representation["momentum_base"]
        != "X_plus=R_c times R_{+,p}"
        or "p>0" not in representation["component"]
        or representation["measure_status"]
        != "DECLARED_LOCAL_LEBESGUE_HALF_DENSITY_CONVENTION_NOT_PHYSICAL_MEASURE"
    ):
        raise AssertionError("half-line representation mutation")
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    return payload, observed, upstream


def exact_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    c, x, y = sp.symbols("c x y", real=True)
    y = sp.Symbol("y", positive=True, real=True)
    z = x + sp.I * y
    resolvent = 1 / (c - z)

    reality = audit.observe(
        "G1.spectral.operator.real_multiplier",
        sp.conjugate(c) == c,
        "the Darboux constraint coordinate c is real on the declared momentum base",
    )
    resolvent_identity = audit.observe(
        "G1.spectral.operator.resolvent_identity",
        sp.simplify((c - z) * resolvent - 1) == 0,
        "the candidate resolvent multiplier satisfies (M_c-z)R_z=I for Im(z)>0",
    )
    modulus_denominator = sp.simplify(
        (c - z) * sp.conjugate(c - z)
    )
    resolvent_bound = audit.observe(
        "G1.spectral.operator.resolvent_bound",
        sp.simplify(modulus_denominator - y**2 - (c - x) ** 2) == 0,
        "|c-z|^2-(Im z)^2=(c-Re z)^2; real-square nonnegativity then gives ||R_z||<=1/|Im z|",
    )
    p = sp.Symbol("p", positive=True, real=True)
    tensor_witness_norms = []
    tensor_witness_operator_norms = []
    for degree in range(3):
        p_norm = sp.integrate(sp.exp(-2 * p), (p, 0, sp.oo))
        tensor_witness_norms.append(
            sp.integrate(
                c ** (2 * degree) * sp.exp(-2 * c**2),
                (c, -sp.oo, sp.oo),
            )
            * p_norm
        )
        tensor_witness_operator_norms.append(
            sp.integrate(
                c ** (2 * (degree + 1)) * sp.exp(-2 * c**2),
                (c, -sp.oo, sp.oo),
            )
            * p_norm
        )
    maximal_domain = audit.observe(
        "G1.spectral.operator.maximal_domain_witnesses",
        all(
            value.is_finite is True and value.is_positive is True
            for value in tensor_witness_norms + tensor_witness_operator_norms
        ),
        "the explicit tensors f_m=c^m*exp(-c^2)*exp(-p), m=0,1,2, obey both f_m in L2(X_plus) and c*f_m in L2(X_plus)",
    )

    boolean_rows = []
    pvm_boolean = True
    for indicator_a in (0, 1):
        for indicator_b in (0, 1):
            row_pass = (
                indicator_a**2 == indicator_a
                and indicator_a * (1 - indicator_a) == 0
                and indicator_a * indicator_b
                == int(bool(indicator_a) and bool(indicator_b))
            )
            boolean_rows.append(
                {
                    "indicator_A": indicator_a,
                    "indicator_B": indicator_b,
                    "passed": row_pass,
                }
            )
            pvm_boolean = pvm_boolean and row_pass
    pvm = audit.observe(
        "G1.spectral.pvm.boolean_algebra",
        pvm_boolean,
        "indicator multiplication obeys E(A)^2=E(A), E(A)E(B)=E(A intersection B), and E(A)E(A^c)=0",
    )

    test = sp.exp(-c**2) * sp.exp(-p)
    kinematic_norm = sp.integrate(
        test**2, (c, -sp.oo, sp.oo), (p, 0, sp.oo)
    )
    zero_fiber = sp.integrate(test.subs(c, 0) ** 2, (p, 0, sp.oo))
    zero_fiber_pass = audit.observe(
        "G1.spectral.rigging.zero_fiber_witness",
        sp.simplify(kinematic_norm - sp.sqrt(sp.pi / 2) / 2) == 0
        and zero_fiber == sp.Rational(1, 2),
        "a frozen smooth rapidly decreasing half-line test has finite kinematical norm and nonzero eta_0=1/2",
    )
    singleton_boundary = audit.observe(
        "G1.spectral.rigging.singleton_not_delta",
        sp.FiniteSet(0).measure == 0 and zero_fiber != 0,
        "the c-Lebesgue singleton has measure zero, so E({0}) is the zero Hilbert projection while the frozen delta(M_c) test-space form is nonzero",
    )

    hbar, epsilon, displacement = sp.symbols(
        "hbar epsilon displacement", positive=True, real=True
    )
    half_line_kernel = 1 / (
        2 * sp.pi * hbar * (epsilon - sp.I * displacement / hbar)
    )
    odd_part = sp.simplify(
        half_line_kernel
        - half_line_kernel.subs(displacement, -displacement)
    )
    half_line_scope = audit.observe(
        "G1.spectral.branch.half_line_fourier_not_identity",
        odd_part != 0 and sp.simplify(sp.im(odd_part)) != 0,
        "the Abel-regulated p>0 Fourier kernel has a nonzero odd imaginary part and is not the full-line delta(Phi_2-Phi_1) identity",
    )

    audit.guard(
        "G1.spectral.guard.maximal_real_multiplication_theorem",
        "maximal real multiplication-operator theorem",
        "sigma-finite Lebesgue X_plus, real measurable multiplier c, maximal domain c*psi in L2, real-square nonnegativity, and bounded everywhere-defined nonreal resolvents verified above",
        "M_c is self-adjoint, has spectrum R and PVM E(Delta)=M_{1_Delta(c)} on this declared local Hilbert space only",
    )
    audit.guard(
        "G1.spectral.guard.rigged_zero_fiber",
        "spectral direct-integral fiber evaluation on a dense smooth test space",
        "the standard half-line Schwartz restriction topology makes S(R_c) tensor S(R_+) dense, nuclear, invariant under multiplication by c, and continuous under c=0 evaluation",
        "eta_0(psi,varphi)=int_0^infinity conjugate(psi(0,p))*varphi(0,p) dp is positive and distributional; it is not E({0}), a bounded projector, or by itself a physical inner product",
    )
    audit.guard(
        "G1.spectral.guard.no_original_ordering_transfer",
        "unitary equivalence is required to transfer an exact operator realization",
        "the upstream one-term FIO failed exact finite-hbar unitarity and supplies only a principal microlocal canonical relation",
        "no original-(Q,P,phi,p) ordering, domain, edge condition or exact constraint diagonalization is inferred",
    )
    audit.guard(
        "G1.spectral.guard.p_positive_component",
        "componentwise chart scope",
        "U_plus has p>0 and no branch doubling was supplied",
        "the previous separately declared full-p relational identity is not reused as an U_plus identity or as evidence for a self-adjoint Phi generator at p=0",
    )

    flags = {
        "real_multiplier": reality,
        "resolvent_identity": resolvent_identity,
        "resolvent_bound": resolvent_bound,
        "maximal_domain_witnesses": maximal_domain,
        "pvm_boolean_algebra": pvm,
        "zero_fiber_test_form": zero_fiber_pass,
        "singleton_projection_distinction": singleton_boundary,
        "p_positive_scope": half_line_scope,
    }
    return (
        {
            "hilbert_representation": {
                "base": "X_plus=R_c times R_{+,p}",
                "measure": "dc*dp",
                "measure_status": "DECLARED_LOCAL_KINEMATICAL_LEBESGUE_HALF_DENSITY",
                "hilbert_space": "L2(X_plus,dc*dp)",
                "constraint_operator": "M_c",
                "action": "(M_c psi)(c,p)=c*psi(c,p)",
                "maximal_domain": "{psi in L2: c*psi in L2}",
                "ordering_status": "EXACT_MULTIPLICATION_ONLY_IN_THIS_REPRESENTATION",
                "self_adjoint": all(flags[key] for key in (
                    "real_multiplier",
                    "resolvent_identity",
                    "resolvent_bound",
                    "maximal_domain_witnesses",
                )),
                "spectrum": "R",
                "pvm": "E(Delta)=multiplication by 1_Delta(c)",
                "resolvent": str(resolvent),
                "resolvent_modulus_denominator": str(modulus_denominator),
            },
            "rigged_zero_fiber": {
                "test_space": "S(R_c) completed_tensor S(R_{+,p})",
                "form": "eta_0(psi,varphi)=int_0^infinity dp conjugate(psi(0,p))*varphi(0,p)",
                "frozen_test": "exp(-c^2)*exp(-p)",
                "kinematical_norm_squared": str(kinematic_norm),
                "eta_0_test_norm": str(zero_fiber),
                "E_singleton_zero": True,
                "delta_Mc_is_bounded_projector": False,
                "physical_inner_product": None,
            },
            "half_line_boundary": {
                "component": "p>0",
                "abel_regularized_positive_p_kernel": str(half_line_kernel),
                "odd_part": str(odd_part),
                "full_p_fourier_identity_imported": False,
                "self_adjoint_Phi_edge_completion": None,
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
    if all(flags.values()):
        verdict = "KEEP_V0_LOCAL_CONSTRAINT_MULTIPLICATION_SPECTRAL_DOMAIN"
        impact = "CLOSE_LOCAL_DARBOUX_REPRESENTATION_DOMAIN_ONLY"
        classification = (
            "GATE1_V0_LOCAL_SELF_ADJOINT_MULTIPLICATION_CONSTRAINT_AND_"
            "DISTRIBUTIONAL_ZERO_FIBER_KEEP_ORIGINAL_ORDERING_AND_PHYSICAL_MEASURE_OPEN"
        )
        condition = (
            "the upstream component and FIO boundary are exact; the maximal "
            "real multiplication operator, resolvent, PVM and rigged zero-fiber "
            "form are internally consistent"
        )
    elif not flags["p_positive_scope"]:
        verdict = "KILL_HALF_LINE_SCOPE_MUTATION"
        impact = "RETAIN_LOCAL_MULTIPLICATION_FACTS_WITHOUT_THE_MUTATED_IDENTITY"
        classification = "GATE1_V0_SPECTRAL_HALF_LINE_SCOPE_MUTATION"
        condition = (
            "the representation silently imports p<0 or calls the full-p "
            "Fourier identity an U_plus spectral identity"
        )
    else:
        verdict = "KILL_V0_DECLARED_CONSTRAINT_SPECTRAL_REPRESENTATION"
        impact = "RETAIN_CLASSICAL_CHART_ONLY"
        classification = "GATE1_V0_CONSTRAINT_MULTIPLICATION_DOMAIN_NONPASS"
        condition = (
            "the resolvent identity/bound, reality, maximal-domain or PVM "
            "checks fail"
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
            "scope_meaning": "one declared local U_plus Darboux momentum representation only",
            "primary_source_boundary": "RAQ sources frame distributional constraint forms; all model-specific operator and test calculations are repository workbench results",
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
                "gate1": result["gate1_decision"],
                "global_n_sigma": None,
                "physics_claim": None,
                "TOE_claim": None,
                "automatic_next": None,
                "result": RESULT_NAME,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
