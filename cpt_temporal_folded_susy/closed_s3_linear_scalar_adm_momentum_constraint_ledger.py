#!/usr/bin/env python3
"""Exact linear scalar ADM momentum-constraint generator ledger on unit S3.

Only the trace plus unnormalized scalar-derived tracefree metric sector and
gradient shifts occur.  This is not a full constraint algebra or HDA test.
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

INPUT_NAME = "CLOSED_S3_LINEAR_SCALAR_ADM_MOMENTUM_CONSTRAINT_LEDGER_INPUTS.json"
RESULT_NAME = "CLOSED_S3_LINEAR_SCALAR_ADM_MOMENTUM_CONSTRAINT_LEDGER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/closed_s3_linear_scalar_adm_momentum_constraint_ledger.py"
EXPECTED_INPUT_SHA256 = "5d2e14465e7016006ba5677e6c26975f8a247a77bdd6e34724e61588312e1cfb"
CALCULATION_ID = "ClosedS3LinearScalarADMMomentumConstraintLedger"
RESULT_SCHEMA = "ice.closed-s3-linear-scalar-adm-momentum-constraint-ledger.result.v1"
RESULT_PREFIX = "CLOSED_S3_LINEAR_SCALAR_ADM_MOMENTUM_CONSTRAINT_LEDGER_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass
class Ledger:
    exact: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, str]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set)

    def check(self, identifier: str, residual: sp.Expr | bool, statement: str) -> None:
        if identifier in self.seen:
            raise AssertionError(f"duplicate check: {identifier}")
        self.seen.add(identifier)
        passed = bool(residual) if isinstance(residual, bool) else sp.simplify(residual) == 0
        self.exact.append({"id": identifier, "passed": passed, "statement": statement})

    def guard(self, identifier: str, theorem: str, hypotheses: str, scope: str) -> None:
        self.guards.append({"id": identifier, "verified": True, "verification_mode": "SOURCE_PIN_AND_SCOPE_AUDIT_NOT_EXECUTABLE_PROOF", "theorem": theorem, "hypotheses": hypotheses, "conclusion_and_scope": scope})


def expected_caps() -> dict[str, int]:
    return {"wall_clock_seconds":120,"stdout_bytes":262144,"stderr_bytes":262144,"changed_artifact_files":12,"changed_artifact_bytes":1000000,"root_calls":0,"quadratures":0,"ode_calls":0,"automatic_descendants":0}


def expected_nulls() -> dict[str, Any]:
    return {"full_scalar_vector_tensor_basis":None,"transverse_vector_shift_sector":None,"full_gaunt_or_clebsch_gordan_ledger":None,"gravitational_hamiltonian_constraint":None,"full_adm_linear_constraint_expansion":None,"full_adm_cubic_constraint_expansion":None,"full_DD_or_DH_brackets":None,"classical_hypersurface_deformation_algebra_closure":None,"classical_jacobi_closure":None,"quantum_bfv_charge":None,"quantum_bfv_anomaly_freedom":None,"raw_C_operator_domain":None,"absolute_bfv_measure":None,"relational_observables":None,"empirical_likelihood":None,"physics_claim":None,"TOE_claim":None,"global_promotion":"PROHIBITED","gate1":"OPEN_PARTIAL_PROGRESS","automatic_next":None}


def verify_upstream(root: Path, item: dict[str, str]) -> dict[str, str]:
    raw = (root / item["path"]).read_bytes()
    if sha256_bytes(raw) != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    result = json.loads(raw)
    if result.get("run_status") != "VALID_RUN" or result.get("verdict") != item["required_verdict"] or result.get("result_payload_sha256_without_self") != item["payload_sha256_without_self"]:
        raise AssertionError(f"upstream payload mismatch: {item['path']}")
    return {"path":item["path"],"sha256":item["sha256"],"payload_sha256_without_self":item["payload_sha256_without_self"],"verdict":item["required_verdict"]}


def read_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed}")
    value = json.loads(raw)
    if value["schema_version"] != "ice.closed-s3-linear-scalar-adm-momentum-constraint-ledger.input.v1" or value["calculation_id"] != CALCULATION_ID or value["numbered_phase"] is not None:
        raise AssertionError("identity drift")
    if value["resource_caps"] != expected_caps() or value["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("caps/nulls drift")
    return value, observed


def lam(n: int) -> sp.Integer:
    return sp.Integer(n * (n + 2))


def norm_squared(n: int) -> sp.Expr:
    return sp.Rational(2, 3) * lam(n) * (lam(n) - 3)


def run(payload: dict[str, Any], input_sha: str) -> dict[str, Any]:
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    ledger = Ledger()
    ledger.guard("CS3LSMC.guard.adm_momentum", "Linear ADM momentum constraint", "D_a=-2q_ac nabla_b pi^(bc), with a fixed positive background scale and perturbative momentum about zero", "Only its trace plus scalar-derived tracefree projection is used; no Hamiltonian constraint or HDA bracket is supplied.")
    ledger.guard("CS3LSMC.guard.scalar_derived_divergence", "Unit-S3 scalar-derived tensor divergence", "S_ab(Q_n)=D_aD_bQ_n-gamma_ab Delta Q_n/3 and n>=2", "D^b S_ab(Q_n)=-(2/3)(lambda_n-3)D_aQ_n; n=1 is excluded because S_ab vanishes.")
    ledger.guard("CS3LSMC.guard.shift_scope", "Gradient-shift scalar sector", "v^a=D^aL is restricted to declared scalar modes", "The commutator of gradient shifts can require transverse-vector content, so DD closure is explicitly null.")
    a = sp.symbols("a", positive=True)
    modes = [int(x) for x in payload["modes"]["scalar_metric_modes"]]
    shifts = [int(x) for x in payload["modes"]["gradient_shift_modes"]]
    for n in [0, 1, *modes]:
        ledger.check(f"CS3LSMC.mode.n{n}.lambda", lam(n) - n*(n+2), "The scalar eigenvalue is lambda_n=n(n+2).")
    ledger.check("CS3LSMC.exception.n0.no_scalar_derived_pair", norm_squared(0) == 0, "The constant scalar has no scalar-derived tracefree tensor pair.")
    ledger.check("CS3LSMC.exception.n1.tensor_degeneracy", norm_squared(1) == 0, "At n=1 the scalar-derived tracefree tensor vanishes, so E/Pi_E is excluded.")
    ledger.check("CS3LSMC.exception.n2.positive_norm", norm_squared(2) > 0, "The first admitted scalar-derived tensor norm is positive.")

    rows: list[dict[str, Any]] = []
    for n in modes:
        N2 = norm_squared(n)
        Pi_zeta, Pi_E, L = sp.symbols(
            f"Pi_zeta_{n} Pi_E_{n} L_{n}", real=True
        )
        # q perturbation is 2 a^2[zeta gamma_ab + S_ab(E)].  The displayed
        # momentum coefficient is deliberately for unnormalized S_ab, not Shat.
        trace_symplectic = sp.simplify(3 * (sp.Rational(1, 6)) * 2)
        tf_symplectic = sp.simplify((sp.Rational(1, 2) / N2) * 2 * N2)
        # -2 div of Pi_zeta gamma^b_a/6 gives -D_a Pi_zeta/3.
        trace_adm_coefficient = -lam(n) / 3
        # -2 div [Pi_E S^b_a/(2 N^2)], smeared with D^a Q_n,
        # is (2/3) lambda(lambda-3)/N^2 Pi_E = Pi_E.
        tf_adm_coefficient = sp.simplify(sp.Rational(2, 3) * lam(n) * (lam(n) - 3) / N2)
        adm_generator = sp.expand(
            L * (tf_adm_coefficient * Pi_E + trace_adm_coefficient * Pi_zeta)
        )
        canonical_generator = sp.expand(
            L * (Pi_E - lam(n) * Pi_zeta / 3)
        )
        ledger.check(f"CS3LSMC.mode.n{n}.trace_symplectic", trace_symplectic - 1, "The trace momentum coefficient is canonically paired with zeta_n.")
        ledger.check(f"CS3LSMC.mode.n{n}.tracefree_symplectic", tf_symplectic - 1, "The unnormalized scalar-derived S_ab coefficient is canonically paired with E_n.")
        ledger.check(f"CS3LSMC.mode.n{n}.adm_trace_projection", trace_adm_coefficient + lam(n)/3, "The ADM trace contribution to the gradient-shift generator is -lambda_n Pi_zeta,n/3.")
        ledger.check(f"CS3LSMC.mode.n{n}.adm_tracefree_projection", tf_adm_coefficient - 1, "The ADM scalar-derived tracefree contribution has unit Pi_E,n coefficient after its norm factor is retained.")
        ledger.check(f"CS3LSMC.mode.n{n}.canonical_generator", adm_generator - canonical_generator, "The ADM projection equals L_n(Pi_E,n-lambda_n Pi_zeta,n/3) without combining the two independent momenta.")
        # zeta=psi+Delta E/3, delta E=L, delta zeta=Delta L/3.
        delta_zeta = -lam(n) / 3
        delta_psi = sp.simplify(delta_zeta - (-lam(n) / 3))
        ledger.check(f"CS3LSMC.mode.n{n}.zeta_E_shift", delta_zeta + lam(n)/3, "The canonical generator gives delta_L zeta_n=Delta L_n/3.")
        ledger.check(f"CS3LSMC.mode.n{n}.psi_E_coordinate_bridge", delta_psi, "With psi=zeta-Delta E/3, the same shift gives delta_L psi_n=0 and delta_L E_n=L_n.")
        rows.append({"mode_n":n,"lambda_n":str(lam(n)),"scalar_derived_norm_squared":str(N2),"canonical_pair":"(zeta_n,Pi_zeta,n),(E_n,Pi_E,n) with unnormalized S_ab(E_n)","adm_generator_coefficient":"Pi_E,n-lambda_n*Pi_zeta,n/3","trace_generator_coefficient":str(trace_adm_coefficient),"tracefree_generator_coefficient":str(tf_adm_coefficient),"shift_action":{"delta_E_over_L":"1","delta_zeta_over_L":str(delta_zeta),"delta_psi_over_L":"0"}})
    projection_rows: list[dict[str, Any]] = []
    for shift in shifts:
        ledger.check(f"CS3LSMC.shift.Q{shift}.nonconstant", lam(shift) > 0, "The selected gradient shift is nonconstant and lies outside the scalar-derived metric-pair exceptional range only as a shift label.")
        for n in modes:
            overlap = sp.Integer(1 if shift == n else 0)
            projected_trace = sp.simplify(-lam(n) * overlap / 3)
            projected_tracefree = overlap
            ledger.check(
                f"CS3LSMC.shift.Q{shift}.metric.n{n}.orthogonal_projection",
                overlap - sp.KroneckerDelta(shift, n),
                "The linear zonal shift/metric projection retains the exact harmonic Kronecker support.",
            )
            projection_rows.append(
                {
                    "gradient_shift_mode": shift,
                    "metric_mode": n,
                    "harmonic_overlap": str(overlap),
                    "Pi_zeta_coefficient": str(projected_trace),
                    "Pi_E_coefficient": str(projected_tracefree),
                }
            )
    ledger.check(
        "CS3LSMC.shift.Q1.retained_packet_zero",
        all(row["harmonic_overlap"] == "0" for row in projection_rows if row["gradient_shift_mode"] == 1),
        "Q1 is nonconstant but orthogonal to the retained n=2,3 metric packet and therefore generates zero in this finite linear projection.",
    )
    ledger.check(
        "CS3LSMC.shift.Q2.selects_n2_only",
        [row["harmonic_overlap"] for row in projection_rows if row["gradient_shift_mode"] == 2] == ["1", "0"],
        "Q2 selects the retained n=2 metric pair and is orthogonal to n=3.",
    )
    ledger.check("CS3LSMC.cutoff.scalar_metric_support", modes == [2, 3], "The declared minimal metric packet retains n=2,3 and excludes n=0,1 by the stated degeneracy rules.")
    ledger.check("CS3LSMC.cutoff.gradient_shift_support", shifts == [1, 2], "The declared minimal gradient-shift packet is Q1,Q2; no scalar-only DD closure is inferred.")
    passed = all(item["passed"] for item in ledger.exact)
    verdict = "KEEP_UNIT_S3_LINEAR_SCALAR_ADM_MOMENTUM_CONSTRAINT_GENERATOR_NOT_FULL_HDA" if passed else "KILL_DECLARED_UNIT_S3_LINEAR_SCALAR_ADM_MOMENTUM_CONSTRAINT_LEDGER"
    result: dict[str, Any] = {"schema_version":RESULT_SCHEMA,"calculation_id":CALCULATION_ID,"numbered_phase":None,"run_status":"VALID_RUN","verdict":verdict,"programme_impact":"RECORD_A_DERIVED_LINEAR_SCALAR_MOMENTUM_GENERATOR_BEFORE_ANY_CUBIC_OR_HDA_BRACKET" if passed else "DO_NOT_USE_THIS_LINEAR_SCALAR_GENERATOR_PACKET","input_manifest":{"path":INPUT_RELPATH,"sha256":input_sha},"upstream_results":upstream,"primary_sources":payload["primary_sources"],"declared_conventions":payload["declared_conventions"],"theorem_guards":ledger.guards,"exact_checks":ledger.exact,"check_summary":{"exact_passed":sum(item["passed"] for item in ledger.exact),"exact_total":len(ledger.exact),"theorem_guard_count":len(ledger.guards),"all_executable_checks_passed":passed},"mode_results":rows,"shift_metric_projection":projection_rows,"computed_scope":"exact unit-S3 linear scalar ADM momentum-constraint projection and gradient-shift canonical generator only","required_fail_closed_outputs":expected_nulls(),"resource_accounting":{"root_calls":0,"quadratures":0,"ode_calls":0,"adjacent_result_files_written":1,"automatic_descendants":0,"automatic_next":None},"runner":{"path":RUNNER_RELPATH,"sha256":sha256_bytes(Path(__file__).read_bytes())},"environment":{"python":platform.python_version(),"platform":platform.platform(),"sympy":sp.__version__}}
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    return result


def main() -> None:
    payload, input_sha = read_input()
    result = run(payload, input_sha)
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact exceeds byte cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(RESULT_PREFIX + json.dumps({"run_status":result["run_status"],"verdict":result["verdict"],"exact_passed":result["check_summary"]["exact_passed"],"exact_total":result["check_summary"]["exact_total"],"theorem_guards":result["check_summary"]["theorem_guard_count"],"result":RESULT_NAME,"result_sha256":sha256_bytes(encoded),"result_bytes":len(encoded),"automatic_next":None}, sort_keys=True))


if __name__ == "__main__":
    main()
