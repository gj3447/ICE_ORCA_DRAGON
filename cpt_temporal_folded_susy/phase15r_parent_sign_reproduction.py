#!/usr/bin/env python3
"""Phase 15R — exact single-source parent-sign reproduction.

This executable is deliberately narrow.  It independently reduces the
bosonic Einstein-plus-one-canonical-chiral kinetic sector in the two primary
sources frozen by Phase 15R, and keeps a third ADM calculation as a
non-evidential regression.  It then applies the frozen source-coverage census
to two separate existence claims.

No numerical tolerance, fitting, source mixing, analytic continuation, or
result-adaptive repair is used.  The executable writes no files.  Its compact
machine record is printed for a later post-run receipt.

Contract commit: 34dd2d3fc533d94113f5ea98d3eafc3721565be4
Input packet commit: 72819da9d9c078b1f7c0d4942d8f069e9c75d656

Run only after this complete file is committed:
    uv run --with sympy python3 phase15r_parent_sign_reproduction.py
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import sympy as sp


MODULE_DIR = Path(__file__).resolve().parent
REPO_ROOT = MODULE_DIR.parent
CONTRACT_PATH = MODULE_DIR / "PHASE15R_RESEARCH_CONTRACT.json"
PACKET_PATH = MODULE_DIR / "PHASE15R_SOURCE_CONVENTION_PACKET.json"
SCRIPT_RELATIVE_PATH = Path(
    "cpt_temporal_folded_susy/phase15r_parent_sign_reproduction.py"
)
RUN_RESULT_PATH = MODULE_DIR / "PHASE15R_RUN_RESULT.json"
RUN_RESULT_RELATIVE_PATH = Path(
    "cpt_temporal_folded_susy/PHASE15R_RUN_RESULT.json"
)
REPLAY_PATH = MODULE_DIR / "PHASE15R_REPLAY_RECEIPT.json"
REPORT_PATH = MODULE_DIR / "PHASE15R_PARENT_SIGN_REPAIR.md"

CONTRACT_SHA256 = "efbd691451508f9188d487af01b99fac81edc432143ca543055f65baa16670b7"
PACKET_SHA256 = "29b43a2bc926192b860da3b3f70fde9a29eaf75f4a5b963de51498152412f3bd"
CONTRACT_COMMIT = "34dd2d3fc533d94113f5ea98d3eafc3721565be4"
PACKET_COMMIT = "72819da9d9c078b1f7c0d4942d8f069e9c75d656"
CYCLE_ID = "cpt-temporal-folded-susy-2026-08-16-phase15r"

HOHL = "HOHL_2020_V1"
KALLOSH = "KALLOSH_KOFMAN_LINDE_VAN_PROEYEN_2000_V3"
ADM = "ADM_EINSTEIN_CANONICAL_SCALAR_INTERNAL_CONTROL"
ALLOWED_SOURCE_TAGS = {HOHL, KALLOSH, ADM}

# These are the actual active inputs consumed by main.  The independent
# frozen_* functions below are the preregistered source-policy oracle.
ACTIVE_EINSTEIN_SIGNS = {HOHL: -1, KALLOSH: -1, ADM: +1}
ACTIVE_ENDPOINT_SIGNS = {HOHL: +1, KALLOSH: -1, ADM: -1}

TARGET_BOSONIC = "P15R_BOSONIC_SINGLE_SOURCE_PARENT_EXISTS_IN_FROZEN_CENSUS"
TARGET_FULL = "P15R_FULL_OFFSHELL_SINGLE_SOURCE_PARENT_EXISTS_IN_FROZEN_CENSUS"

SYMBOL_OWNER: dict[sp.Symbol, str] = {}


class Audit:
    """Exact check recorder with no floating fallback."""

    def __init__(self) -> None:
        self.passed = 0
        self.mutants_rejected = 0
        self.mutant_categories: set[str] = set()
        self.guards = 0
        self.observations = 0
        self.known_prior_matches = 0
        self._pending_integrity_failures: list[tuple[str, str, str]] | None = None

    def begin_integrity_collection(self) -> None:
        """Collect independent invalid conditions before applying precedence."""

        if self._pending_integrity_failures is not None:
            raise AuditFailure(
                "INTERNAL_INCONSISTENCY",
                "P15R.integrity_collection.reentered",
                "an integrity collection cannot be nested",
            )
        self._pending_integrity_failures = []

    def _register_failure(
        self,
        qualification: str,
        check_id: str,
        statement: str,
    ) -> None:
        if self._pending_integrity_failures is None:
            raise AuditFailure(qualification, check_id, statement)
        self._pending_integrity_failures.append(
            (qualification, check_id, statement)
        )

    def pending_qualifications(self) -> tuple[str, ...]:
        if self._pending_integrity_failures is None:
            return ()
        return tuple(item[0] for item in self._pending_integrity_failures)

    def end_integrity_collection(self) -> None:
        """Raise one invalid result using the frozen multi-failure precedence."""

        pending = self._pending_integrity_failures
        if pending is None:
            raise AuditFailure(
                "INTERNAL_INCONSISTENCY",
                "P15R.integrity_collection.not_started",
                "no integrity collection is active",
            )
        self._pending_integrity_failures = None
        if pending:
            qualifications = tuple(item[0] for item in pending)
            raise AuditFailure(
                choose_invalid_qualification(qualifications),
                ";".join(item[1] for item in pending),
                " | ".join(item[2] for item in pending),
                qualifications=qualifications,
            )

    def check(
        self,
        check_id: str,
        condition: bool,
        statement: str,
        *,
        failure_qualification: str = "INTERNAL_INCONSISTENCY",
    ) -> None:
        if not condition:
            self._register_failure(failure_qualification, check_id, statement)
            return
        self.passed += 1
        print(f"[PASS] {check_id}: {statement}")

    def observe(self, check_id: str, condition: bool, statement: str) -> bool:
        """Record a scientific comparison without forcing its outcome."""

        self.observations += 1
        if condition:
            self.known_prior_matches += 1
            print(f"[OBSERVED MATCH] {check_id}: {statement}")
        else:
            print(f"[OBSERVED REFUTATION] {check_id}: {statement}")
        return condition

    def reject(self, check_id: str, rejected: bool, statement: str) -> None:
        if not rejected:
            self._register_failure(
                "INTERNAL_INCONSISTENCY",
                check_id,
                f"mutant survived — {statement}",
            )
            return
        self.mutants_rejected += 1
        parts = check_id.split(".")
        if len(parts) > 1 and parts[1].startswith("M"):
            self.mutant_categories.add(parts[1])
        print(f"[MUTANT REJECTED] {check_id}: {statement}")

    def guard(self, check_id: str, condition: bool, statement: str) -> None:
        if not condition:
            self._register_failure(
                "SCOPE_OVERREACH",
                check_id,
                f"scope guard failed — {statement}",
            )
            return
        self.guards += 1
        print(f"[SCOPE GUARD] {check_id}: {statement}")


class SourceStackingError(ValueError):
    """Raised before a symbolic node can acquire a parent from another tag."""


class AuditFailure(AssertionError):
    """Integrity failure carrying the frozen invalid qualification."""

    def __init__(
        self,
        qualification: str,
        check_id: str,
        statement: str,
        *,
        qualifications: Iterable[str] | None = None,
    ) -> None:
        super().__init__(f"{check_id}: {statement}")
        self.qualification = qualification
        self.qualifications = tuple(qualifications or (qualification,))
        self.check_id = check_id
        self.statement = statement


ACTIVE_AUDIT: Audit | None = None


def with_pending_qualifications(*qualifications: str) -> tuple[str, ...]:
    pending = () if ACTIVE_AUDIT is None else ACTIVE_AUDIT.pending_qualifications()
    return pending + tuple(qualifications)


def register_symbols(source_tag: str, symbols: Iterable[sp.Symbol]) -> None:
    if source_tag not in ALLOWED_SOURCE_TAGS:
        raise SourceStackingError(f"unregistered symbol-owner tag: {source_tag}")
    for symbol in symbols:
        owner = SYMBOL_OWNER.get(symbol)
        if owner is not None and owner != source_tag:
            raise SourceStackingError(
                f"symbol {symbol} already belongs to {owner}, not {source_tag}"
            )
        SYMBOL_OWNER[symbol] = source_tag


@dataclass(frozen=True)
class TaggedNode:
    source_tag: str
    name: str
    expression: sp.Expr | sp.MatrixBase
    parents: tuple[str, ...]


def tagged_node(
    source_tag: str,
    name: str,
    expression: sp.Expr | sp.MatrixBase,
    parents: Iterable[TaggedNode] = (),
) -> TaggedNode:
    if source_tag not in ALLOWED_SOURCE_TAGS:
        raise SourceStackingError(f"unregistered source tag: {source_tag}")
    parent_tuple = tuple(parents)
    if any(parent.source_tag != source_tag for parent in parent_tuple):
        raise SourceStackingError(
            f"{source_tag}:{name} received a parent from another source"
        )
    foreign_or_unowned = {
        symbol
        for symbol in expression.free_symbols
        if SYMBOL_OWNER.get(symbol) != source_tag
    }
    if foreign_or_unowned:
        raise SourceStackingError(
            f"{source_tag}:{name} contains foreign or unowned symbols "
            f"{sorted(map(str, foreign_or_unowned))}"
        )
    return TaggedNode(
        source_tag=source_tag,
        name=name,
        expression=expression,
        parents=tuple(parent.name for parent in parent_tuple),
    )


@dataclass(frozen=True)
class SourceVars:
    """A tag-local, algebraically independent copy of the FLRW jet."""

    tag: str
    M_P: sp.Symbol
    V_0: sp.Symbol
    a: sp.Symbol
    N: sp.Symbol
    adot: sp.Symbol
    addot: sp.Symbol
    Ndot: sp.Symbol
    Nddot: sp.Symbol
    Tdot: sp.Symbol
    Ydot: sp.Symbol
    Xdot: sp.Symbol


def source_vars(tag: str, suffix: str) -> SourceVars:
    M_P, V_0, a, N = sp.symbols(
        f"M_P_{suffix} V_0_{suffix} a_{suffix} N_{suffix}", positive=True
    )
    adot, addot, Ndot, Nddot, Tdot, Ydot, Xdot = sp.symbols(
        " ".join(
            f"{name}_{suffix}"
            for name in (
                "adot",
                "addot",
                "Ndot",
                "Nddot",
                "Tdot",
                "Ydot",
                "Xdot",
            )
        ),
        real=True,
    )
    variables = SourceVars(
        tag=tag,
        M_P=M_P,
        V_0=V_0,
        a=a,
        N=N,
        adot=adot,
        addot=addot,
        Ndot=Ndot,
        Nddot=Nddot,
        Tdot=Tdot,
        Ydot=Ydot,
        Xdot=Xdot,
    )
    register_symbols(
        tag,
        (
            variables.M_P,
            variables.V_0,
            variables.a,
            variables.N,
            variables.adot,
            variables.addot,
            variables.Ndot,
            variables.Nddot,
            variables.Tdot,
            variables.Ydot,
            variables.Xdot,
        ),
    )
    return variables


def exact_zero(expression: sp.Expr | sp.MatrixBase) -> bool:
    simplified = sp.simplify(expression)
    if isinstance(simplified, sp.MatrixBase):
        return simplified == sp.zeros(*simplified.shape)
    return simplified == 0


def exact_equal(left: sp.Expr | sp.MatrixBase, right: sp.Expr | sp.MatrixBase) -> bool:
    return exact_zero(left - right)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def d_dt(v: SourceVars, expression: sp.Expr) -> sp.Expr:
    """Total coordinate-time derivative on the registered finite jet."""

    jet = {
        v.a: v.adot,
        v.adot: v.addot,
        v.N: v.Ndot,
        v.Ndot: v.Nddot,
    }
    return sp.expand(sum(sp.diff(expression, key) * value for key, value in jet.items()))


def d_coord(v: SourceVars, coordinate: int, expression: sp.Expr) -> sp.Expr:
    return d_dt(v, expression) if coordinate == 0 else sp.S.Zero


def q_curvature(v: SourceVars) -> sp.Expr:
    return (
        v.addot / (v.a * v.N**2)
        + v.adot**2 / (v.a**2 * v.N**2)
        - v.adot * v.Ndot / (v.a * v.N**3)
    )


def endpoint_b(v: SourceVars) -> sp.Expr:
    return 3 * v.M_P**2 * v.V_0 * v.a**2 * v.adot / v.N


def frozen_einstein_coefficient(v: SourceVars) -> sp.Expr:
    if v.tag in {HOHL, KALLOSH}:
        return -v.M_P**2 / 2
    if v.tag == ADM:
        return v.M_P**2 / 2
    raise SourceStackingError(f"no Einstein coefficient for tag {v.tag}")


def frozen_endpoint_sign(v: SourceVars) -> int:
    if v.tag == HOHL:
        return 1
    if v.tag in {KALLOSH, ADM}:
        return -1
    raise SourceStackingError(f"no endpoint sign for tag {v.tag}")


def active_einstein_coefficient(v: SourceVars) -> sp.Expr:
    try:
        sign = ACTIVE_EINSTEIN_SIGNS[v.tag]
    except KeyError as error:
        raise SourceStackingError(
            f"no active Einstein coefficient for tag {v.tag}"
        ) from error
    return sign * v.M_P**2 / 2


def active_endpoint_sign(v: SourceVars) -> int:
    try:
        return ACTIVE_ENDPOINT_SIGNS[v.tag]
    except KeyError as error:
        raise SourceStackingError(
            f"no active endpoint sign for tag {v.tag}"
        ) from error


def allowed_equivalence_policy(
    *,
    real_point_map: bool,
    positive_lapse: bool,
    positive_densitizer: bool,
) -> bool:
    return real_point_map and positive_lapse and positive_densitizer


INVALID_PRECEDENCE = (
    "PREREG_OR_PROVENANCE_INVALID",
    "INVALID_SOURCE_STACKING",
    "FORBIDDEN_SIGN_REPAIR",
    "SCOPE_OVERREACH",
    "INTERNAL_INCONSISTENCY",
)


def choose_invalid_qualification(qualifications: Iterable[str]) -> str:
    observed = set(qualifications)
    for qualification in INVALID_PRECEDENCE:
        if qualification in observed:
            return qualification
    return "INTERNAL_INCONSISTENCY"


def coframe(v: SourceVars) -> list[list[sp.Expr]]:
    return [
        [v.N, 0, 0, 0],
        [0, v.a, 0, 0],
        [0, 0, v.a, 0],
        [0, 0, 0, v.a],
    ]


def inverse_coframe(v: SourceVars) -> list[list[sp.Expr]]:
    """E[a][m], inverse to e[m][a]."""

    return [
        [1 / v.N, 0, 0, 0],
        [0, 1 / v.a, 0, 0],
        [0, 0, 1 / v.a, 0],
        [0, 0, 0, 1 / v.a],
    ]


def hohl_spin_connection(
    v: SourceVars,
) -> tuple[list[list[list[sp.Expr]]], list[list[list[sp.Expr]]]]:
    """Transcribe Hohl's bosonic coframe connection in source index order.

    The returned mixed array is omega[m][b_lower][a_upper].  It is not an
    ordinary upper-first connection matrix.
    """

    eta = (-1, 1, 1, 1)
    e = coframe(v)
    E = inverse_coframe(v)
    e_lower = [[eta[A] * e[m][A] for A in range(4)] for m in range(4)]

    omega_coord = [
        [[sp.S.Zero for _ in range(4)] for _ in range(4)] for _ in range(4)
    ]
    for m in range(4):
        for n in range(4):
            for p in range(4):
                first = sum(
                    e[m][A] * d_coord(v, n, e_lower[p][A])
                    - e[p][A] * d_coord(v, m, e_lower[n][A])
                    - e[n][A] * d_coord(v, p, e_lower[m][A])
                    for A in range(4)
                ) / 2
                second = sum(
                    e[m][A] * d_coord(v, p, e_lower[n][A])
                    - e[n][A] * d_coord(v, m, e_lower[p][A])
                    - e[p][A] * d_coord(v, n, e_lower[m][A])
                    for A in range(4)
                ) / 2
                omega_coord[m][n][p] = sp.simplify(first - second)

    omega_lower = [
        [[sp.S.Zero for _ in range(4)] for _ in range(4)] for _ in range(4)
    ]
    for m in range(4):
        for b in range(4):
            for a_index in range(4):
                omega_lower[m][b][a_index] = sp.simplify(
                    sum(
                        E[b][n] * E[a_index][p] * omega_coord[m][n][p]
                        for n in range(4)
                        for p in range(4)
                    )
                )

    omega_mixed = [
        [[sp.S.Zero for _ in range(4)] for _ in range(4)] for _ in range(4)
    ]
    for m in range(4):
        for b in range(4):
            for a_index in range(4):
                omega_mixed[m][b][a_index] = sp.simplify(
                    eta[a_index] * omega_lower[m][b][a_index]
                )
    return omega_coord, omega_mixed


def hohl_scalar_curvature(
    v: SourceVars,
    *,
    transpose_product_mutant: bool = False,
    reverse_curvature_order_mutant: bool = False,
) -> tuple[sp.Expr, list[list[list[list[sp.Expr]]]], list[list[list[sp.Expr]]]]:
    """Build the Hohl Lorentz curvature with its lower-first product order."""

    eta = (-1, 1, 1, 1)
    E = inverse_coframe(v)
    _, omega = hohl_spin_connection(v)
    curvature = [
        [
            [[sp.S.Zero for _ in range(4)] for _ in range(4)]
            for _ in range(4)
        ]
        for _ in range(4)
    ]

    for n in range(4):
        for m in range(4):
            for b in range(4):
                for a_index in range(4):
                    derivative = d_coord(v, n, omega[m][b][a_index]) - d_coord(
                        v, m, omega[n][b][a_index]
                    )
                    source_product = sum(
                        omega[m][b][c] * omega[n][c][a_index]
                        - omega[n][b][c] * omega[m][c][a_index]
                        for c in range(4)
                    )
                    if transpose_product_mutant and reverse_curvature_order_mutant:
                        raise ValueError("Hohl curvature mutants must be isolated")
                    if reverse_curvature_order_mutant:
                        derivative = -derivative
                        source_product = -source_product
                    elif transpose_product_mutant:
                        source_product = -source_product
                    curvature[n][m][b][a_index] = sp.simplify(
                        derivative + source_product
                    )

    scalar = sp.S.Zero
    for n in range(4):
        for m in range(4):
            for b in range(4):
                for a_index in range(4):
                    E_up_b_m = eta[b] * E[b][m]
                    scalar += (
                        E[a_index][n]
                        * E_up_b_m
                        * curvature[n][m][b][a_index]
                    )
    return sp.simplify(scalar), curvature, omega


def metric_and_christoffel(
    v: SourceVars,
) -> tuple[sp.Matrix, sp.Matrix, list[list[list[sp.Expr]]]]:
    metric = sp.diag(-v.N**2, v.a**2, v.a**2, v.a**2)
    inverse = sp.diag(-1 / v.N**2, 1 / v.a**2, 1 / v.a**2, 1 / v.a**2)
    gamma = [
        [[sp.S.Zero for _ in range(4)] for _ in range(4)] for _ in range(4)
    ]
    for upper in range(4):
        for left in range(4):
            for right in range(4):
                gamma[upper][left][right] = sp.simplify(
                    sum(
                        inverse[upper, sigma]
                        * (
                            d_coord(v, left, metric[sigma, right])
                            + d_coord(v, right, metric[sigma, left])
                            - d_coord(v, sigma, metric[left, right])
                        )
                        / 2
                        for sigma in range(4)
                    )
                )
    return metric, inverse, gamma


def metric_scalar_curvature(
    v: SourceVars,
    *,
    derivative_order: str,
) -> tuple[sp.Expr, list[list[list[sp.Expr]]]]:
    """Build a coordinate curvature in one explicitly selected source order."""

    _, inverse, gamma = metric_and_christoffel(v)
    riemann = [
        [
            [[sp.S.Zero for _ in range(4)] for _ in range(4)]
            for _ in range(4)
        ]
        for _ in range(4)
    ]
    for upper in range(4):
        for lower in range(4):
            for m in range(4):
                for n in range(4):
                    if derivative_order == "STANDARD_M_THEN_N":
                        component = d_coord(
                            v, m, gamma[upper][n][lower]
                        ) - d_coord(v, n, gamma[upper][m][lower])
                        component += sum(
                            gamma[upper][m][c] * gamma[c][n][lower]
                            - gamma[upper][n][c] * gamma[c][m][lower]
                            for c in range(4)
                        )
                    elif derivative_order == "KALLOSH_N_THEN_M":
                        component = d_coord(
                            v, n, gamma[upper][m][lower]
                        ) - d_coord(v, m, gamma[upper][n][lower])
                        component += sum(
                            gamma[upper][n][c] * gamma[c][m][lower]
                            - gamma[upper][m][c] * gamma[c][n][lower]
                            for c in range(4)
                        )
                    else:
                        raise ValueError(f"unknown curvature order: {derivative_order}")
                    riemann[upper][lower][m][n] = sp.simplify(component)

    ricci = sp.zeros(4, 4)
    for lower in range(4):
        for n in range(4):
            ricci[lower, n] = sp.simplify(
                sum(riemann[upper][lower][upper][n] for upper in range(4))
            )
    scalar = sp.simplify(
        sum(inverse[lower, n] * ricci[lower, n] for lower in range(4) for n in range(4))
    )
    return scalar, gamma


def source_scalar_time_kinetic(
    v: SourceVars,
) -> tuple[TaggedNode, dict[str, TaggedNode]]:
    """Reduce each tag's own scalar action coefficient and field bridge."""

    local_zdot = (v.Tdot + sp.I * v.Ydot) / sp.sqrt(2)
    local_zbar_dot = (v.Tdot - sp.I * v.Ydot) / sp.sqrt(2)
    if v.tag in {HOHL, KALLOSH}:
        source_action_scale = v.M_P**2
        source_field_scale = 1 / v.M_P
    elif v.tag == ADM:
        source_action_scale = sp.S.One
        source_field_scale = sp.S.One
    else:
        raise ValueError(f"unknown scalar source tag: {v.tag}")

    action_scale = tagged_node(v.tag, "scalar_action_scale", source_action_scale)
    field_bridge = tagged_node(v.tag, "scalar_field_bridge", source_field_scale)
    source_product = tagged_node(
        v.tag,
        "source_Zdot_Zbar_dot",
        sp.expand(
            (field_bridge.expression * local_zdot)
            * (field_bridge.expression * local_zbar_dot)
        ),
        (field_bridge,),
    )
    measure = tagged_node(v.tag, "sqrt_minus_g_V0", v.V_0 * v.N * v.a**3)
    inverse_metric_time = tagged_node(v.tag, "g_inverse_00", -1 / v.N**2)
    source_scalar_coefficient = tagged_node(
        v.tag,
        "source_scalar_coefficient",
        -action_scale.expression,
        (action_scale,),
    )
    lagrangian = tagged_node(
        v.tag,
        "L_scalar",
        sp.simplify(
            measure.expression
            * source_scalar_coefficient.expression
            * inverse_metric_time.expression
            * source_product.expression
        ),
        (measure, source_scalar_coefficient, inverse_metric_time, source_product),
    )
    return lagrangian, {
        "action_scale": action_scale,
        "field_bridge": field_bridge,
        "source_product": source_product,
        "measure": measure,
        "inverse_metric_time": inverse_metric_time,
        "coefficient": source_scalar_coefficient,
    }


def hessian_inertia(
    matrix: sp.Matrix,
    positive_prefactor: sp.Expr,
) -> tuple[int, int, int] | None:
    normalized = sp.simplify(matrix / positive_prefactor)
    if not normalized.is_diagonal():
        return None
    negative = zero = positive = 0
    for entry in normalized.diagonal():
        value = sp.simplify(entry)
        if value == 0:
            zero += 1
        elif value.is_positive:
            positive += 1
        elif value.is_negative:
            negative += 1
        else:
            return None
    return negative, zero, positive


@dataclass(frozen=True)
class TerminalRecord:
    source_tag: str
    source_role: str
    curvature_expression: str
    r_over_q_coefficient: int | str
    known_prior_curvature_match: bool
    raw_gravity_expression: str
    raw_boundary_identity: bool
    first_order_expression: str
    first_order_free_of_higher_jets: bool
    scalar_product_expression: str
    scalar_sign_check: bool
    hessian_expression: str | None
    hessian_rank: int | None
    hessian_determinant: str | None
    inertia: tuple[int, int, int] | None
    hamiltonian_expression: str | None
    target_hamiltonian_match: bool | None
    bosonic_derivation_complete: bool
    bosonic_parent_test_pass: bool | None
    source_coverage_status: str | None
    full_offshell_coverage_pass: bool | None
    evidential_weight: str


@dataclass(frozen=True)
class CandidateRecord:
    source_id: str
    candidate_role: str
    bosonic_test_complete: bool
    bosonic_inertia_matches_target: bool | None
    bosonic_parent_test_pass: bool | None
    coverage_test_complete: bool
    full_offshell_coverage_pass: bool | None
    bosonic_equivalence_class_id: str | None
    full_offshell_equivalence_class_id: str | None
    candidate_status: str
    rejection_reason: str | None


@dataclass(frozen=True)
class CoverageEvaluation:
    source_id: str
    candidate_role: str
    complete: bool
    full_offshell_pass: bool | None
    coverage_status: str
    frozen_row: dict[str, Any]


def evaluate_coverage_row(
    row: dict[str, Any],
    required_keys: set[str],
) -> CoverageEvaluation:
    field_rows = row.get("field_rows")
    keys_complete = isinstance(field_rows, dict) and set(field_rows) == required_keys
    action_available = row.get(
        "auxiliary_uneliminated_action_available",
        row.get("target_old_minimal_auxiliary_uneliminated_action_available"),
    )
    transformations_available = row.get(
        "local_transformation_family_available",
        row.get("complete_required_target_transformation_family_available"),
    )
    boolean_complete = isinstance(action_available, bool) and isinstance(
        transformations_available, bool
    )
    complete = keys_complete and boolean_complete
    if not complete:
        coverage_pass = None
    else:
        unavailable_markers = ("NOT_AVAILABLE", "MISSING", "OMITTED", "ELIMINATED")
        fields_available = all(
            not any(marker in str(value) for marker in unavailable_markers)
            for value in field_rows.values()
        )
        coverage_pass = bool(
            action_available and transformations_available and fields_available
        )
    return CoverageEvaluation(
        source_id=row["source_id"],
        candidate_role=row["candidate_role"],
        complete=complete,
        full_offshell_pass=coverage_pass,
        coverage_status=row["coverage_status"],
        frozen_row=row,
    )


def legendre_record(
    audit: Audit,
    v: SourceVars,
    source_role: str,
    curvature: TaggedNode,
    scalar_node: TaggedNode,
    einstein_coefficient: sp.Expr,
    endpoint_sign: int,
    expected_r_over_q: int,
    coverage_status: str | None,
    coverage_pass: bool | None,
    evidential_weight: str,
) -> tuple[TerminalRecord, dict[str, TaggedNode | None]]:
    tag = v.tag
    q_node = tagged_node(tag, "Q_curv", q_curvature(v))
    r_over_q = sp.simplify(curvature.expression / q_node.expression)
    ratio_resolved = bool(r_over_q.is_number and r_over_q.is_real)
    coefficient_record: int | str = (
        int(r_over_q) if isinstance(r_over_q, sp.Integer) else sp.sstr(r_over_q)
    )
    known_prior_curvature_match = audit.observe(
        f"P15R.{tag}.curvature_coefficient",
        exact_equal(curvature.expression, expected_r_over_q * q_node.expression),
        f"compare the derived Q coefficient with known prior {expected_r_over_q}",
    )
    audit.check(
        f"P15R.{tag}.curvature_no_Nddot",
        not curvature.expression.has(v.Nddot),
        "lapse second derivatives cancel from the scalar curvature",
    )

    determinant = v.V_0 * v.N * v.a**3
    coefficient_node = tagged_node(tag, "Einstein_coefficient", einstein_coefficient)
    audit.check(
        f"P15R.{tag}.frozen_Einstein_coefficient",
        exact_equal(coefficient_node.expression, frozen_einstein_coefficient(v)),
        "the source-tagged Einstein coefficient equals the frozen literal coefficient",
        failure_qualification="FORBIDDEN_SIGN_REPAIR",
    )
    audit.check(
        f"P15R.{tag}.positive_real_domain",
        bool(v.M_P.is_positive and v.V_0.is_positive and v.a.is_positive and v.N.is_positive)
        and allowed_equivalence_policy(
            real_point_map=True,
            positive_lapse=True,
            positive_densitizer=True,
        ),
        "the active source path remains on the frozen real positive-lapse and positive-densitizer domain",
        failure_qualification="FORBIDDEN_SIGN_REPAIR",
    )
    audit.check(
        f"P15R.{tag}.frozen_endpoint_sign",
        endpoint_sign == frozen_endpoint_sign(v),
        "the source-tagged endpoint removal sign equals the frozen literal policy",
        failure_qualification="FORBIDDEN_SIGN_REPAIR",
    )
    raw_gravity = tagged_node(
        tag,
        "L_gravity_raw",
        sp.simplify(determinant * coefficient_node.expression * curvature.expression),
        (coefficient_node, curvature),
    )
    b_node = tagged_node(tag, "B", endpoint_b(v))
    dot_b_node = tagged_node(tag, "dot_B", sp.simplify(d_dt(v, b_node.expression)), (b_node,))
    bulk_expected = (
        3 * v.M_P**2 * v.V_0 * v.a * v.adot**2 / v.N
        if endpoint_sign == 1
        else -3 * v.M_P**2 * v.V_0 * v.a * v.adot**2 / v.N
    )
    raw_expected = -endpoint_sign * dot_b_node.expression + bulk_expected
    raw_boundary_ok = exact_equal(raw_gravity.expression, raw_expected)
    audit.observe(
        f"P15R.{tag}.raw_boundary_identity",
        raw_boundary_ok,
        "compare the raw Einstein term with the registered endpoint-plus-bulk identity",
    )
    first_gravity = tagged_node(
        tag,
        "L_gravity_first",
        sp.simplify(raw_gravity.expression + endpoint_sign * dot_b_node.expression),
        (raw_gravity, dot_b_node),
    )
    higher_jets_absent = not first_gravity.expression.has(v.addot, v.Ndot, v.Nddot)
    audit.observe(
        f"P15R.{tag}.first_order_bulk",
        higher_jets_absent and exact_equal(first_gravity.expression, bulk_expected),
        "compare the registered endpoint removal with the first-order bulk target",
    )

    scalar_product = sp.simplify(
        scalar_node.expression * v.N / (v.V_0 * v.a**3)
    )
    scalar_expected = (v.Tdot**2 + v.Ydot**2) / 2
    scalar_ok = exact_equal(scalar_product, scalar_expected) and not scalar_product.has(sp.I)
    audit.observe(
        f"P15R.{tag}.same_source_scalar",
        scalar_ok,
        "compare the same-source complex chiral reduction with the exact real 1/2 normalization",
    )

    if not (raw_boundary_ok and higher_jets_absent and scalar_ok):
        partial_record = TerminalRecord(
            source_tag=tag,
            source_role=source_role,
            curvature_expression=sp.sstr(curvature.expression),
            r_over_q_coefficient=coefficient_record,
            known_prior_curvature_match=known_prior_curvature_match,
            raw_gravity_expression=sp.sstr(raw_gravity.expression),
            raw_boundary_identity=raw_boundary_ok,
            first_order_expression=sp.sstr(
                sp.simplify(first_gravity.expression + scalar_node.expression)
            ),
            first_order_free_of_higher_jets=higher_jets_absent,
            scalar_product_expression=sp.sstr(scalar_product),
            scalar_sign_check=scalar_ok,
            hessian_expression=None,
            hessian_rank=None,
            hessian_determinant=None,
            inertia=None,
            hamiltonian_expression=None,
            target_hamiltonian_match=None,
            bosonic_derivation_complete=False,
            bosonic_parent_test_pass=None,
            source_coverage_status=coverage_status,
            full_offshell_coverage_pass=coverage_pass,
            evidential_weight=evidential_weight,
        )
        return partial_record, {
            "q": q_node,
            "curvature": curvature,
            "coefficient": coefficient_node,
            "raw_gravity": raw_gravity,
            "endpoint": b_node,
            "dot_endpoint": dot_b_node,
            "first_gravity": first_gravity,
            "scalar": scalar_node,
            "first_total": None,
            "hessian": None,
            "hamiltonian": None,
        }

    adot_from_x = v.a * v.Xdot / (sp.sqrt(6) * v.M_P)
    first_total = tagged_node(
        tag,
        "L_first_XTY",
        sp.simplify(
            (first_gravity.expression + scalar_node.expression).subs(v.adot, adot_from_x)
        ),
        (first_gravity, scalar_node),
    )
    velocities = (v.Xdot, v.Tdot, v.Ydot)
    hessian_expression = sp.hessian(first_total.expression, velocities)
    hessian = tagged_node(
        tag,
        "G_XTY",
        sp.simplify(hessian_expression),
        (first_total,),
    )
    prefactor = v.V_0 * v.a**3 / v.N
    inertia = hessian_inertia(sp.Matrix(hessian.expression), prefactor)
    hessian_matrix = sp.Matrix(hessian.expression)
    hessian_rank = int(hessian_matrix.rank())
    hessian_resolved = (
        inertia is not None and hessian_matrix.is_symmetric() and hessian_rank == 3
    )
    audit.observe(
        f"P15R.{tag}.hessian_exact",
        hessian_resolved,
        "record whether the first-order X,T,Y Hessian is exact, symmetric, and nondegenerate",
    )

    momenta = sp.symbols(f"p_X_{tag} p_T_{tag} p_Y_{tag}", real=True)
    register_symbols(tag, momenta)
    equations = [
        sp.Eq(momenta[index], sp.diff(first_total.expression, velocity))
        for index, velocity in enumerate(velocities)
    ]
    velocity_solution = (
        sp.solve(equations, velocities, dict=True) if hessian_rank == 3 else []
    )
    legendre_complete = (
        len(velocity_solution) == 1 and len(velocity_solution[0]) == 3
    )
    audit.observe(
        f"P15R.{tag}.legendre_invertible",
        legendre_complete,
        "record whether the exact Legendre map has one complete solution",
    )
    target_hamiltonian = sp.simplify(
        v.N
        * (-momenta[0] ** 2 + momenta[1] ** 2 + momenta[2] ** 2)
        / (2 * v.V_0 * v.a**3)
    )
    hamiltonian: TaggedNode | None = None
    target_match: bool | None = None
    if legendre_complete:
        solved = velocity_solution[0]
        hamiltonian_expression = sp.simplify(
            sum(momenta[index] * velocities[index] for index in range(3)).subs(solved)
            - first_total.expression.subs(solved)
        )
        hamiltonian = tagged_node(
            tag,
            "H_kin",
            hamiltonian_expression,
            (first_total, hessian),
        )
        target_match = exact_equal(hamiltonian.expression, target_hamiltonian)

    endpoint_linear = sp.symbols(
        f"F_X_{tag} F_T_{tag} F_Y_{tag} F_t_{tag}", real=True
    )
    register_symbols(tag, endpoint_linear)
    allowed_later_endpoint = tagged_node(
        tag,
        "allowed_later_endpoint",
        endpoint_linear[0] * v.Xdot
        + endpoint_linear[1] * v.Tdot
        + endpoint_linear[2] * v.Ydot
        + endpoint_linear[3],
        (first_total,),
    )
    audit.check(
        f"P15R.{tag}.later_endpoint_hessian_zero",
        exact_zero(sp.hessian(allowed_later_endpoint.expression, velocities)),
        "a later velocity-independent generating function contributes zero velocity Hessian",
    )

    general_j_entries = sp.symbols(
        " ".join(f"J_{row}{column}_{tag}" for row in range(3) for column in range(3)),
        real=True,
    )
    register_symbols(tag, general_j_entries)
    general_j = sp.Matrix(3, 3, general_j_entries)
    general_j_node = tagged_node(tag, "general_point_jacobian", general_j)
    transformed_velocities = sp.symbols(
        f"u_X_{tag} u_T_{tag} u_Y_{tag}", real=True
    )
    register_symbols(tag, transformed_velocities)
    velocity_substitution = {
        velocities[row]: sum(
            general_j[row, column] * transformed_velocities[column]
            for column in range(3)
        )
        for row in range(3)
    }
    transformed_lagrangian = tagged_node(
        tag,
        "point_transformed_lagrangian",
        sp.expand(first_total.expression.subs(velocity_substitution)),
        (first_total, general_j_node),
    )
    transformed_hessian = tagged_node(
        tag,
        "point_transformed_hessian",
        sp.hessian(transformed_lagrangian.expression, transformed_velocities),
        (transformed_lagrangian,),
    )
    audit.check(
        f"P15R.{tag}.general_point_map_congruence",
        exact_equal(
            transformed_hessian.expression,
            general_j.T * hessian_matrix * general_j,
        )
        and not exact_zero(general_j.det()),
        "a general real derivative-free point-map Jacobian acts by exact Hessian congruence; inertia preservation is conditional on det(J)!=0",
    )

    j1, j2, j3, densitizer = sp.symbols(
        f"j1_{tag} j2_{tag} j3_{tag} d_{tag}", positive=True
    )
    register_symbols(tag, (j1, j2, j3, densitizer))
    jacobian = sp.diag(j1, j2, j3)
    jacobian_node = tagged_node(tag, "positive_diagonal_jacobian", jacobian)
    congruent = tagged_node(
        tag,
        "positive_diagonal_congruence",
        sp.simplify(jacobian.T * hessian_matrix * jacobian),
        (hessian, jacobian_node),
    )
    densitized = tagged_node(
        tag,
        "positive_densitized_hessian",
        sp.simplify(densitizer * hessian_matrix),
        (hessian,),
    )
    congruent_inertia = hessian_inertia(sp.Matrix(congruent.expression), prefactor)
    densitized_inertia = hessian_inertia(
        sp.Matrix(densitized.expression),
        densitizer * prefactor,
    )
    inertia_equivalence_ok = bool(
        inertia is not None
        and jacobian.det().is_positive
        and congruent_inertia == inertia
        and densitized_inertia == inertia
    )
    audit.observe(
        f"P15R.{tag}.inertia_equivalences",
        inertia_equivalence_ok,
        "record whether the exact positive-diagonal witness and positive densitization preserve computed inertia",
    )

    bosonic_derivation_complete = bool(
        ratio_resolved
        and raw_boundary_ok
        and higher_jets_absent
        and scalar_ok
        and hessian_resolved
        and legendre_complete
        and inertia_equivalence_ok
    )
    bosonic_parent_test_pass = bool(
        bosonic_derivation_complete
        and inertia == (1, 0, 2)
    )
    record = TerminalRecord(
        source_tag=tag,
        source_role=source_role,
        curvature_expression=sp.sstr(curvature.expression),
        r_over_q_coefficient=coefficient_record,
        known_prior_curvature_match=known_prior_curvature_match,
        raw_gravity_expression=sp.sstr(raw_gravity.expression),
        raw_boundary_identity=raw_boundary_ok,
        first_order_expression=sp.sstr(first_total.expression),
        first_order_free_of_higher_jets=higher_jets_absent,
        scalar_product_expression=sp.sstr(scalar_product),
        scalar_sign_check=scalar_ok,
        hessian_expression=sp.sstr(hessian.expression),
        hessian_rank=hessian_rank,
        hessian_determinant=sp.sstr(sp.factor(hessian_matrix.det())),
        inertia=inertia,
        hamiltonian_expression=(
            None if hamiltonian is None else sp.sstr(hamiltonian.expression)
        ),
        target_hamiltonian_match=target_match,
        bosonic_derivation_complete=bosonic_derivation_complete,
        bosonic_parent_test_pass=bosonic_parent_test_pass,
        source_coverage_status=coverage_status,
        full_offshell_coverage_pass=coverage_pass,
        evidential_weight=evidential_weight,
    )
    return record, {
        "q": q_node,
        "curvature": curvature,
        "coefficient": coefficient_node,
        "raw_gravity": raw_gravity,
        "endpoint": b_node,
        "dot_endpoint": dot_b_node,
        "first_gravity": first_gravity,
        "scalar": scalar_node,
        "first_total": first_total,
        "hessian": hessian,
        "hamiltonian": hamiltonian,
    }


def candidate_status(
    source_id: str,
    candidate_role: str,
    terminal: TerminalRecord | None,
    coverage_source_id: str,
    coverage_complete: bool,
    coverage_pass: bool | None,
) -> CandidateRecord:
    if terminal is not None and terminal.source_tag != source_id:
        raise SourceStackingError(
            f"candidate {source_id} received terminal {terminal.source_tag}"
        )
    if terminal is not None and terminal.source_role != candidate_role:
        raise SourceStackingError(
            f"candidate {source_id} role {candidate_role} does not match terminal role {terminal.source_role}"
        )
    if coverage_source_id != source_id:
        raise SourceStackingError(
            f"candidate {source_id} received coverage {coverage_source_id}"
        )
    bosonic_complete = (
        terminal is not None and terminal.bosonic_derivation_complete
    )
    inertia_match = (
        None
        if terminal is None or terminal.inertia is None
        else terminal.inertia == (1, 0, 2)
    )
    parent_test_pass = (
        None if terminal is None else terminal.bosonic_parent_test_pass
    )
    bosonic_equivalence_class_id = None
    full_equivalence_class_id = None
    if not bosonic_complete or inertia_match is None or parent_test_pass is None:
        status = "UNRESOLVED"
        reason = "BOSONIC_DERIVATION_UNRESOLVED"
    elif not parent_test_pass:
        status = "REJECT_SIGN"
        reason = (
            "EXACT_NONDEGENERATE_INERTIA_MISMATCH"
            if not inertia_match
            else "BOSONIC_PARENT_GATE_MISMATCH"
        )
    elif not coverage_complete or coverage_pass is None:
        status = "UNRESOLVED"
        reason = "FULL_OFFSHELL_COVERAGE_UNRESOLVED"
    elif coverage_pass:
        status = "FULL_OFFSHELL_ELIGIBLE"
        reason = None
    else:
        status = "BOSONIC_PARENT_ONLY"
        reason = "FULL_OFFSHELL_SOURCE_COVERAGE_MISSING"
    return CandidateRecord(
        source_id=source_id,
        candidate_role=candidate_role,
        bosonic_test_complete=bosonic_complete,
        bosonic_inertia_matches_target=inertia_match,
        bosonic_parent_test_pass=parent_test_pass,
        coverage_test_complete=coverage_complete,
        full_offshell_coverage_pass=coverage_pass,
        bosonic_equivalence_class_id=bosonic_equivalence_class_id,
        full_offshell_equivalence_class_id=full_equivalence_class_id,
        candidate_status=status,
        rejection_reason=reason,
    )


def selection_status(
    candidates: list[CandidateRecord],
    *,
    require_full: bool,
) -> str:
    if any(
        not candidate.bosonic_test_complete
        or candidate.bosonic_parent_test_pass is None
        for candidate in candidates
    ):
        return "UNRESOLVED"
    if require_full and any(
        not candidate.coverage_test_complete
        or candidate.full_offshell_coverage_pass is None
        for candidate in candidates
    ):
        return "UNRESOLVED"
    eligible_candidates: list[CandidateRecord] = []
    for candidate in candidates:
        if candidate.bosonic_parent_test_pass is not True:
            continue
        if require_full and candidate.full_offshell_coverage_pass is not True:
            continue
        eligible_candidates.append(candidate)
    if not eligible_candidates:
        return "NONE_ELIGIBLE"
    if len(eligible_candidates) == 1:
        return "SINGLE_ELIGIBLE"
    # The frozen packet contains no pairwise point-map equivalence certificate.
    # Do not invent one after seeing multiple passing candidates.
    return "UNRESOLVED"


def target_record(
    target_claim_id: str,
    *,
    census_complete: bool,
    eligible_source_ids: list[str],
) -> dict[str, Any]:
    if target_claim_id not in {TARGET_BOSONIC, TARGET_FULL}:
        raise AuditFailure(
            "INTERNAL_INCONSISTENCY",
            "P15R.R4.unknown_target",
            f"unknown active target: {target_claim_id}",
        )
    if not census_complete:
        inference = "INCONCLUSIVE"
        qualification = "UNCONSTRUCTED" if target_claim_id == TARGET_BOSONIC else "SOURCE_INCOMPLETE"
        follow_up = "Resolve the frozen source derivation or coverage map before any target verdict."
    elif eligible_source_ids:
        inference = "SUPPORTS"
        qualification = "NONE"
        follow_up = (
            "Record the scoped source parent; do not infer temporal-branch supersymmetry."
        )
    else:
        inference = "CONTRADICTS"
        qualification = (
            "NO_VALID_BOSONIC_PARENT_IN_FROZEN_CENSUS"
            if target_claim_id == TARGET_BOSONIC
            else "NO_VALID_SINGLE_PARENT_IN_FROZEN_CENSUS"
        )
        follow_up = (
            "Stop this frozen-census route. A new primary-source candidate requires a new preregistered cycle."
        )
    return {
        "target_claim_id": target_claim_id,
        "validity": "VALID",
        "inference": inference,
        "qualification": qualification,
        "novelty": "REPRODUCTION",
        "registration": "PREREGISTERED",
        "fitting_risk": "NOT_APPLICABLE",
        "null_model": "NOT_APPLICABLE",
        "multiplicity": "NOT_APPLICABLE",
        "reproduction": "EXACT_SYMBOLIC_FIRST_RUN_PENDING_REPLAY_RATIFICATION",
        "bayes": "NOT_ESTIMABLE",
        "lakatos": "NOT_APPLICABLE",
        "kg_action": "NONE",
        "ratification_request": "none",
        "follow_up": follow_up,
    }


def invalid_target_record(
    target_claim_id: str,
    qualification: str,
    reason: str,
) -> dict[str, Any]:
    return {
        "target_claim_id": target_claim_id,
        "validity": "INVALID",
        "inference": "INCONCLUSIVE",
        "qualification": qualification,
        "novelty": "REPRODUCTION",
        "registration": "PREREGISTERED",
        "fitting_risk": "NOT_APPLICABLE",
        "null_model": "NOT_APPLICABLE",
        "multiplicity": "NOT_APPLICABLE",
        "reproduction": "EXECUTABLE_INTEGRITY_FAILURE",
        "bayes": "NOT_ESTIMABLE",
        "lakatos": "NOT_APPLICABLE",
        "kg_action": "NONE",
        "ratification_request": "none",
        "follow_up": f"Stop Phase 15R and repair the preregistered integrity failure: {reason}",
    }


def emit_invalid_machine_record(
    qualifications: str | Iterable[str],
    check_id: str,
    reason: str,
) -> None:
    if isinstance(qualifications, str):
        qualifications = (qualifications,)
    observed_qualifications = tuple(qualifications)
    qualification = choose_invalid_qualification(observed_qualifications)
    record = {
        "cycle_id": CYCLE_ID,
        "registration": "PREREGISTERED",
        "novelty": "REPRODUCTION",
        "integrity_failure": {
            "check_id": check_id,
            "qualification": qualification,
            "observed_qualifications": sorted(set(observed_qualifications)),
            "reason": reason,
        },
        "source_terminals": [],
        "candidate_records": [],
        "bosonic_census_complete": False,
        "full_offshell_census_complete": False,
        "bosonic_eligible_source_ids": [],
        "full_offshell_eligible_source_ids": [],
        "bosonic_parent_selection_status": "UNRESOLVED",
        "full_offshell_parent_selection_status": "UNRESOLVED",
        "target_classifications": [
            invalid_target_record(TARGET_BOSONIC, qualification, reason),
            invalid_target_record(TARGET_FULL, qualification, reason),
        ],
        "scope": "FROZEN_TWO_SOURCE_CENSUS_ONLY",
        "phase15a_k2_evaluated": False,
    }
    print("P15R_MACHINE_RECORD=" + json.dumps(record, sort_keys=True))


def scope_firewall_accepts(source_text: str, packet: dict[str, Any]) -> bool:
    frozen_phrases = packet["executable_requirements"]["must_not_contain"]
    forbidden_atoms = (
        "P_" + "3/2",
        "rho" + "_i",
        "tangency" + " residual",
        "compens" + "ator",
        "canonical" + " supersymmetry constraint",
        "Q_" + "phys",
        "branch" + " projector",
    )
    return all(phrase not in source_text for phrase in frozen_phrases) and all(
        atom not in source_text for atom in forbidden_atoms
    )


def write_api_absent(source_text: str) -> bool:
    write_api_atoms = (
        "write_" + "text(",
        "write_" + "bytes(",
        "open" + "(",
        "touch" + "(",
        "unlink" + "(",
        "mkdir" + "(",
    )
    return all(atom not in source_text for atom in write_api_atoms)


def check_provenance_and_scope(
    audit: Audit,
) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        contract = load_json(CONTRACT_PATH)
        packet = load_json(PACKET_PATH)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise AuditFailure(
            "PREREG_OR_PROVENANCE_INVALID",
            "P15R.R0.input_load",
            f"frozen JSON input missing or malformed: {error}",
        ) from error
    packet_contract_provenance = (
        packet.get("contract_provenance") if isinstance(packet, dict) else None
    )
    safe_provenance_gate = (
        isinstance(contract, dict)
        and isinstance(packet, dict)
        and isinstance(packet_contract_provenance, dict)
        and file_sha256(CONTRACT_PATH) == CONTRACT_SHA256
        and file_sha256(PACKET_PATH) == PACKET_SHA256
        and contract.get("cycle_id") == CYCLE_ID
        and packet.get("cycle_id") == CYCLE_ID
        and packet_contract_provenance.get("commit") == CONTRACT_COMMIT
    )
    if not safe_provenance_gate:
        raise AuditFailure(
            "PREREG_OR_PROVENANCE_INVALID",
            "P15R.R0.safe_input_gate",
            "frozen JSON type, hash, cycle, or contract provenance is invalid",
        )
    audit.begin_integrity_collection()
    audit.check(
        "P15R.R0.input_hashes",
        file_sha256(CONTRACT_PATH) == CONTRACT_SHA256
        and file_sha256(PACKET_PATH) == PACKET_SHA256,
        "contract and source/convention packet match their preregistered hashes",
        failure_qualification="PREREG_OR_PROVENANCE_INVALID",
    )
    audit.check(
        "P15R.R0.cycle_and_commits",
        contract["cycle_id"] == packet["cycle_id"] == CYCLE_ID
        and packet["contract_provenance"]["commit"] == CONTRACT_COMMIT,
        "cycle identity and contract-before-packet provenance are exact",
        failure_qualification="PREREG_OR_PROVENANCE_INVALID",
    )

    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(SCRIPT_RELATIVE_PATH)],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    unchanged = subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", str(SCRIPT_RELATIVE_PATH)],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    contract_before_packet = subprocess.run(
        ["git", "merge-base", "--is-ancestor", CONTRACT_COMMIT, PACKET_COMMIT],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    packet_before_head = subprocess.run(
        ["git", "merge-base", "--is-ancestor", PACKET_COMMIT, "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    script_at_packet_commit = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", PACKET_COMMIT, "--", str(SCRIPT_RELATIVE_PATH)],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    script_add_commit = subprocess.run(
        [
            "git",
            "log",
            "--diff-filter=A",
            "-1",
            "--format=%H",
            "--",
            str(SCRIPT_RELATIVE_PATH),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    add_commit = script_add_commit.stdout.strip()
    add_commit_before_head = subprocess.run(
        ["git", "merge-base", "--is-ancestor", add_commit or "HEAD", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    packet_before_add_commit = subprocess.run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            PACKET_COMMIT,
            add_commit or "HEAD",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    script_unchanged_since_add = subprocess.run(
        [
            "git",
            "diff",
            "--quiet",
            add_commit or "HEAD",
            "HEAD",
            "--",
            str(SCRIPT_RELATIVE_PATH),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    result_paths_at_add = subprocess.run(
        [
            "git",
            "ls-tree",
            "-r",
            "--name-only",
            add_commit or "HEAD",
            "--",
            "cpt_temporal_folded_susy/PHASE15R_RUN_RESULT.json",
            "cpt_temporal_folded_susy/PHASE15R_REPLAY_RECEIPT.json",
            "cpt_temporal_folded_susy/PHASE15R_PARENT_SIGN_REPAIR.md",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    current_head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    result_tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(RUN_RESULT_RELATIVE_PATH)],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    result_unchanged = subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", str(RUN_RESULT_RELATIVE_PATH)],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    result_add_commit_process = subprocess.run(
        [
            "git",
            "log",
            "--diff-filter=A",
            "-1",
            "--format=%H",
            "--",
            str(RUN_RESULT_RELATIVE_PATH),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    result_add_commit = result_add_commit_process.stdout.strip()
    executable_before_result = subprocess.run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            add_commit or "HEAD",
            result_add_commit or "HEAD",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    result_before_head = subprocess.run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            result_add_commit or "HEAD",
            "HEAD",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    replay_result_provenance_ok = True
    if RUN_RESULT_PATH.exists():
        try:
            replay_result = load_json(RUN_RESULT_PATH)
            replay_machine = replay_result.get("machine_record", replay_result)
            replay_provenance = replay_machine["provenance"]
            replay_result_provenance_ok = (
                replay_machine.get("cycle_id") == CYCLE_ID
                and replay_provenance.get("head_commit") == add_commit
                and replay_provenance.get("executable_add_commit") == add_commit
                and replay_provenance.get("contract_commit") == CONTRACT_COMMIT
                and replay_provenance.get("packet_commit") == PACKET_COMMIT
                and replay_provenance.get("contract_sha256") == CONTRACT_SHA256
                and replay_provenance.get("packet_sha256") == PACKET_SHA256
                and replay_provenance.get("executable_sha256")
                == file_sha256(Path(__file__))
            )
        except (
            AttributeError,
            KeyError,
            OSError,
            TypeError,
            UnicodeError,
            json.JSONDecodeError,
        ):
            replay_result_provenance_ok = False
        first_run_position_ok = (
            result_tracked.returncode == 0
            and result_unchanged.returncode == 0
            and result_add_commit_process.returncode == 0
            and bool(result_add_commit)
            and executable_before_result.returncode == 0
            and result_before_head.returncode == 0
            and replay_result_provenance_ok
        )
    else:
        first_run_position_ok = (
            current_head.returncode == 0
            and current_head.stdout.strip() == add_commit
            and not REPLAY_PATH.exists()
            and not REPORT_PATH.exists()
        )
    audit.check(
        "P15R.R0.committed_executable",
        tracked.returncode == 0
        and unchanged.returncode == 0
        and contract_before_packet.returncode == 0
        and packet_before_head.returncode == 0,
        "contract, packet, and unmodified executable occur in the registered commit order",
        failure_qualification="PREREG_OR_PROVENANCE_INVALID",
    )
    audit.check(
        "P15R.R0.historical_artifact_absence",
        script_at_packet_commit.returncode == 0
        and script_at_packet_commit.stdout.strip() == ""
        and script_add_commit.returncode == 0
        and bool(add_commit)
        and add_commit_before_head.returncode == 0
        and packet_before_add_commit.returncode == 0
        and script_unchanged_since_add.returncode == 0
        and result_paths_at_add.returncode == 0
        and result_paths_at_add.stdout.strip() == ""
        and first_run_position_ok,
        "the script is absent at the packet commit, its add-commit contains no result/replay/report, and a pre-result run occurs at that add-commit",
        failure_qualification="PREREG_OR_PROVENANCE_INVALID",
    )

    source_by_id = {source["source_id"]: source for source in packet["official_sources"]}
    audit.check(
        "P15R.R0.primary_source_census",
        set(source_by_id) == {HOHL, KALLOSH},
        "the evidential primary census contains exactly the two frozen candidates",
        failure_qualification="PREREG_OR_PROVENANCE_INVALID",
    )
    audit.check(
        "P15R.R0.official_source_hashes",
        source_by_id[HOHL]["official_source_artifact"]["main_tex_sha256"]
        == "12722fb7ed5e7c52c2011a632cd5c57e218a843888ce9e15ada6c64a4d52fec6"
        and source_by_id[KALLOSH]["official_source_artifact"]["main_tex_sha256"]
        == "81c4ab799f2cd943bb53fec6f8607267a46090b222a9fc659144902862431af7"
        and source_by_id[HOHL]["official_source_artifact"]["transport_sha256"]
        == "991ec8f192c78671a899e61a44ddc53232cc7c4ac019a19f5d54748a14743521"
        and source_by_id[KALLOSH]["official_source_artifact"]["transport_sha256"]
        == "d4cdf9f7e2afc63cce079b264dadda50597ed0c06732b225fafe172b834c9ee8",
        "official main-source and transport hashes are frozen exactly",
        failure_qualification="PREREG_OR_PROVENANCE_INVALID",
    )
    audit.check(
        "P15R.R0.locator_packet",
        len(source_by_id[HOHL]["exact_scopes"]) == 9
        and len(source_by_id[KALLOSH]["exact_scopes"]) == 14
        and all(scope.get("official_tex_lines") for source in source_by_id.values() for scope in source["exact_scopes"]),
        "every frozen locator has an official line span under the immutable packet hash",
        failure_qualification="PREREG_OR_PROVENANCE_INVALID",
    )
    typo_ids = {entry["id"] for entry in packet["kallosh_same_source_typography_packets"]}
    audit.check(
        "P15R.R0.typography_packets",
        typo_ids == {"P15R_KU1_TIME_RELATION", "P15R_KU2_EINSTEIN_MIXED_COMPONENT"},
        "both same-source Kallosh typography packets are present",
        failure_qualification="PREREG_OR_PROVENANCE_INVALID",
    )
    audit.check(
        "P15R.R0.semantic_mutant_ledgers",
        len(contract["semantic_mutants"]) == 10
        and len(packet["semantic_mutants"]) == 16,
        "all contract and packet semantic-mutant fixtures are frozen before execution",
        failure_qualification="PREREG_OR_PROVENANCE_INVALID",
    )
    audit.check(
        "P15R.R0.invalid_precedence",
        choose_invalid_qualification(
            {
                "INTERNAL_INCONSISTENCY",
                "SCOPE_OVERREACH",
                "FORBIDDEN_SIGN_REPAIR",
                "INVALID_SOURCE_STACKING",
                "PREREG_OR_PROVENANCE_INVALID",
            }
        )
        == "PREREG_OR_PROVENANCE_INVALID"
        and choose_invalid_qualification(
            {"INTERNAL_INCONSISTENCY", "FORBIDDEN_SIGN_REPAIR"}
        )
        == "FORBIDDEN_SIGN_REPAIR",
        "multiple invalid conditions follow the exact frozen qualification precedence",
        failure_qualification="INTERNAL_INCONSISTENCY",
    )
    audit.check(
        "P15R.R0.active_source_policy",
        ACTIVE_EINSTEIN_SIGNS == {HOHL: -1, KALLOSH: -1, ADM: +1}
        and ACTIVE_ENDPOINT_SIGNS == {HOHL: +1, KALLOSH: -1, ADM: -1}
        and allowed_equivalence_policy(
            real_point_map=True,
            positive_lapse=True,
            positive_densitizer=True,
        ),
        "the actual active Einstein, endpoint, and positive-domain inputs equal the frozen source policy before science starts",
        failure_qualification="FORBIDDEN_SIGN_REPAIR",
    )
    graph = packet["source_tagged_derivation_graph"]
    audit.check(
        "P15R.R0.source_tag_graph",
        ALLOWED_SOURCE_TAGS == {HOHL, KALLOSH, ADM}
        and set(graph["allowed_tags"]) == ALLOWED_SOURCE_TAGS
        and set(ACTIVE_EINSTEIN_SIGNS) == ALLOWED_SOURCE_TAGS
        and set(ACTIVE_ENDPOINT_SIGNS) == ALLOWED_SOURCE_TAGS
        and "no mixed-source comparison node" in graph["node_rule"]
        and "cannot be a derivation parent" in graph["comparison_boundary"],
        "tag-local symbolic DAGs terminate before the non-symbolic decision layer",
        failure_qualification="INVALID_SOURCE_STACKING",
    )

    script_text = Path(__file__).read_text(encoding="utf-8")
    audit.guard(
        "P15R.R5.forbidden_source_scan",
        scope_firewall_accepts(script_text, packet),
        "the executable contains neither frozen phrases nor atomic forbidden later-stage expressions",
    )
    audit.guard(
        "P15R.R5.no_output_writes",
        write_api_absent(script_text),
        "the science executable exposes no ordinary filesystem-write API",
    )
    audit.guard(
        "P15R.R5.claim_ceiling",
        "Exactly the two primary candidates frozen in the contract; no claim of literature completeness."
        == packet["full_offshell_coverage_matrix"]["census_scope"],
        "the two-source result cannot be promoted to a literature-wide theorem",
    )
    # This is the single preflight flush.  Any invalid provenance, source-tag,
    # sign/domain, or scope condition stops before curvature is evaluated.
    audit.end_integrity_collection()
    return contract, packet


def check_connections_and_curvatures(
    audit: Audit,
    h: SourceVars,
    k: SourceVars,
    a_ref: SourceVars,
) -> tuple[TaggedNode, TaggedNode, TaggedNode, dict[str, Any]]:
    h_curvature_expr, h_tensor, h_omega = hohl_scalar_curvature(h)
    h_q = q_curvature(h)
    f_h = h.adot / h.N
    fdot_h = h.addot / h.N - h.adot * h.Ndot / h.N**2
    omega_nonzero_ok = all(
        exact_equal(h_omega[i][0][i], f_h)
        and exact_equal(h_omega[i][i][0], f_h)
        for i in range(1, 4)
    )
    unexpected_omega = [
        (m, b, upper)
        for m in range(4)
        for b in range(4)
        for upper in range(4)
        if h_omega[m][b][upper] != 0
        and not (m in range(1, 4) and ((b == 0 and upper == m) or (b == m and upper == 0)))
    ]
    audit.check(
        "P15R.Hohl.spin_connection",
        omega_nonzero_ok and not unexpected_omega and all(exact_zero(h_omega[0][b][u]) for b in range(4) for u in range(4)),
        "the source coframe formula derives only omega[i,0,i]=omega[i,i,0]=adot/N",
    )
    audit.check(
        "P15R.Hohl.curvature_components",
        all(
            exact_equal(h_tensor[0][i][i][0], fdot_h)
            and exact_equal(h_tensor[0][i][0][i], fdot_h)
            for i in range(1, 4)
        )
        and all(
            exact_equal(h_tensor[i][j][j][i], f_h**2)
            for i in range(1, 4)
            for j in range(1, 4)
            if i != j
        ),
        "the source lower-first curvature product gives the registered derivative and spatial components",
    )
    audit.check(
        "P15R.Hohl.curvature_antisymmetry",
        all(
            exact_equal(h_tensor[n][m][b][u], -h_tensor[m][n][b][u])
            for n in range(4)
            for m in range(4)
            for b in range(4)
            for u in range(4)
        ),
        "the Hohl curvature is antisymmetric in its source coordinate pair",
    )
    h_curvature = tagged_node(HOHL, "R_H", h_curvature_expr)

    k_curvature_expr, k_gamma = metric_scalar_curvature(
        k, derivative_order="KALLOSH_N_THEN_M"
    )
    gamma_expected = [
        exact_equal(k_gamma[0][0][0], k.Ndot / k.N),
        all(exact_equal(k_gamma[0][i][i], k.a * k.adot / k.N**2) for i in range(1, 4)),
        all(
            exact_equal(k_gamma[i][0][i], k.adot / k.a)
            and exact_equal(k_gamma[i][i][0], k.adot / k.a)
            for i in range(1, 4)
        ),
    ]
    audit.check(
        "P15R.Kallosh.christoffel",
        all(gamma_expected),
        "the Kallosh-tagged displayed metric derives the arbitrary-lapse Levi-Civita components",
    )
    k_curvature = tagged_node(KALLOSH, "R_K", k_curvature_expr)
    H_k = sp.symbols("H_K", nonzero=True, real=True)
    register_symbols(KALLOSH, (H_k,))
    de_sitter_node = tagged_node(
        KALLOSH,
        "de_sitter_curvature_anchor",
        sp.simplify(
            k_curvature_expr.subs(
                {
                    k.N: 1,
                    k.Ndot: 0,
                    k.Nddot: 0,
                    k.adot: H_k * k.a,
                    k.addot: H_k**2 * k.a,
                }
            )
        ),
        (k_curvature,),
    )
    de_sitter = de_sitter_node.expression
    audit.check(
        "P15R.Kallosh.de_sitter_anchor",
        exact_equal(de_sitter, -12 * H_k**2),
        "the source-native curvature reproduces the printed de Sitter sign",
    )
    eta_first = k.a * k.adot / k.N
    eta_second = sp.simplify((k.a / k.N) * d_dt(k, eta_first))
    audit.check(
        "P15R.Kallosh.conformal_time_anchor",
        exact_equal(eta_second / k.a**3, q_curvature(k))
        and exact_equal(k_curvature_expr, -6 * eta_second / k.a**3),
        "the accepted conformal-time bridge independently matches the arbitrary-lapse result",
    )

    adm_curvature_expr, adm_gamma = metric_scalar_curvature(
        a_ref, derivative_order="STANDARD_M_THEN_N"
    )
    audit.check(
        "P15R.ADM.independent_connection",
        exact_equal(adm_gamma[0][0][0], a_ref.Ndot / a_ref.N)
        and exact_equal(adm_gamma[0][1][1], a_ref.a * a_ref.adot / a_ref.N**2),
        "the internal ADM control rebuilds its own tagged connection",
    )
    adm_curvature = tagged_node(ADM, "R_standard", adm_curvature_expr)

    h_bad_expr, _, _ = hohl_scalar_curvature(h, transpose_product_mutant=True)
    h_reversed_order_expr, _, _ = hohl_scalar_curvature(
        h, reverse_curvature_order_mutant=True
    )
    k_wrong_order_expr, _ = metric_scalar_curvature(
        k, derivative_order="STANDARD_M_THEN_N"
    )
    h_bad_node = tagged_node(HOHL, "mutant_transposed_product_curvature", h_bad_expr)
    h_reversed_node = tagged_node(
        HOHL, "mutant_reversed_order_curvature", h_reversed_order_expr
    )
    k_wrong_order_node = tagged_node(
        KALLOSH, "mutant_standard_order_curvature", k_wrong_order_expr
    )
    k_wrong_de_sitter_node = tagged_node(
        KALLOSH,
        "mutant_de_sitter_curvature_anchor",
        sp.simplify(
            k_wrong_order_expr.subs(
                {
                    k.N: 1,
                    k.Ndot: 0,
                    k.Nddot: 0,
                    k.adot: H_k * k.a,
                    k.addot: H_k**2 * k.a,
                }
            )
        ),
        (k_wrong_order_node,),
    )
    k_wrong_de_sitter = k_wrong_de_sitter_node.expression
    audit.reject(
        "P15R.M17.hohl_storage_transpose",
        not exact_equal(h_bad_node.expression, h_curvature_expr)
        and not exact_equal(h_bad_node.expression, 6 * h_q),
        "upper-first/transposed connection multiplication fails the Hohl component and scalar regressions",
    )
    audit.reject(
        "P15R.M4.hohl_uses_kallosh_order",
        not exact_equal(h_reversed_node.expression, h_curvature_expr)
        and exact_equal(h_reversed_node.expression, -h_curvature_expr),
        "the explicitly reversed derivative-and-product tensor fails Hohl's source-order result",
    )
    audit.reject(
        "P15R.M5.kallosh_uses_hohl_sign",
        not exact_equal(k_wrong_order_node.expression, k_curvature_expr)
        and not exact_equal(k_wrong_de_sitter, -12 * H_k**2),
        "the explicitly standard-order tensor fails Kallosh's source and de Sitter anchors",
    )
    audit.reject(
        "P15R.M6.premature_unit_lapse",
        not exact_equal(
            6 * (h.addot / h.a + h.adot**2 / h.a**2),
            h_curvature_expr,
        ),
        "setting N=1 before the arbitrary-lapse identity loses registered lapse dependence",
    )
    h_without_ndot = h_curvature_expr.subs(h.Ndot, 0)
    audit.reject(
        "P15R.M7.omit_Ndot",
        not exact_equal(h_without_ndot, h_curvature_expr)
        and exact_equal(sp.diff(h_curvature_expr, h.Ndot), -6 * h.adot / (h.a * h.N**3)),
        "omitting Ndot fails the exact arbitrary-lapse coefficient",
    )

    return h_curvature, k_curvature, adm_curvature, {
        "hohl_bad_transpose": h_bad_expr,
        "kallosh_de_sitter": de_sitter,
    }


def check_typography_mutants(audit: Audit, k: SourceVars) -> None:
    time_coefficient_accepted = tagged_node(
        KALLOSH, "accepted_conformal_time_coefficient", -(k.a) ** 2
    )
    time_coefficient_literal = tagged_node(
        KALLOSH, "mutant_conformal_time_coefficient", -(1 / k.a) ** 2
    )
    audit.check(
        "P15R.KU1.accepted_time_relation",
        exact_equal(time_coefficient_accepted.expression, -k.a**2),
        "dt=a deta reproduces the conformal metric time coefficient",
    )
    audit.reject(
        "P15R.M1.literal_time_relation",
        not exact_equal(time_coefficient_literal.expression, -k.a**2),
        "the printed dt=deta/a mutant gives -a^-2 rather than -a^2",
    )
    H = sp.symbols("H_typography", nonzero=True, real=True)
    register_symbols(KALLOSH, (H,))
    rho = tagged_node(KALLOSH, "typography_rho", 3 * k.M_P**2 * H**2)
    einstein_mixed = tagged_node(KALLOSH, "typography_G00", -3 * H**2)
    audit.check(
        "P15R.KU2.accepted_einstein_sign",
        exact_equal(einstein_mixed.expression, -rho.expression / k.M_P**2),
        "the accepted mixed Einstein component agrees with the same-source Friedmann anchors",
    )
    audit.reject(
        "P15R.M2.literal_einstein_sign",
        not exact_equal(einstein_mixed.expression, rho.expression / k.M_P**2),
        "the printed positive mixed-component mutant has exact residual -6 H^2",
    )


def coverage_records(
    audit: Audit,
    packet: dict[str, Any],
) -> dict[str, CoverageEvaluation]:
    matrix = packet["full_offshell_coverage_matrix"]
    rows = {row["source_id"]: row for row in matrix["candidates"]}
    required = {
        field.replace(" and ", "_and_").replace(" ", "_")
        for field in matrix["required_fields"]
    }
    evaluated = {
        source_id: evaluate_coverage_row(row, required)
        for source_id, row in rows.items()
    }
    audit.check(
        "P15R.R3.coverage_census",
        set(rows) == {HOHL, KALLOSH}
        and set(rows[HOHL]["field_rows"]) == required
        and set(rows[KALLOSH]["field_rows"]) == required,
        "both frozen candidates have a complete source-coverage row inventory",
    )
    audit.check(
        "P15R.R3.hohl_coverage",
        evaluated[HOHL].complete
        and evaluated[HOHL].full_offshell_pass is True
        and "FROZEN_GLYPH_CAVEATS" in evaluated[HOHL].coverage_status,
        "Hohl supplies the frozen formula-family coverage with disclosed glyph caveats",
    )
    audit.check(
        "P15R.R3.kallosh_coverage",
        evaluated[KALLOSH].complete
        and evaluated[KALLOSH].full_offshell_pass is False
        and rows[KALLOSH]["superconformal_auxiliary_retaining_action_available"],
        "Kallosh's superconformal auxiliaries are not relabeled as the missing target old-minimal family",
    )
    mutated_row = dict(rows[KALLOSH])
    mutated_row["target_old_minimal_auxiliary_uneliminated_action_available"] = True
    mutated_evaluation = evaluate_coverage_row(mutated_row, required)
    audit.reject(
        "P15R.M13.auxiliary_elimination_as_full_coverage",
        mutated_evaluation.full_offshell_pass is False,
        "changing only the action-availability flag leaves restricted transformations and missing target rows unable to pass the same coverage predicate",
    )
    return evaluated


def semantic_scope_mutants(
    audit: Audit,
    packet: dict[str, Any],
    h: SourceVars,
    k: SourceVars,
    h_nodes: dict[str, TaggedNode],
    k_nodes: dict[str, TaggedNode],
    h_record: TerminalRecord,
    k_record: TerminalRecord,
) -> None:
    h_eh_flip = tagged_node(
        HOHL,
        "mutant_positive_Einstein_coefficient",
        +h.M_P**2 / 2,
    )
    audit.reject(
        "P15R.M3.hohl_EH_sign_flip",
        not exact_equal(h_eh_flip.expression, frozen_einstein_coefficient(h))
        and exact_equal(h_nodes["coefficient"].expression, frozen_einstein_coefficient(h)),
        "an injected positive Hohl Einstein coefficient fails the same frozen coefficient predicate used by the active path",
    )
    audit.reject(
        "P15R.M8.endpoint_omitted",
        h_nodes["raw_gravity"].expression.has(h.addot, h.Ndot),
        "omitting the registered endpoint leaves higher jets in the raw Einstein term",
    )
    h_double_endpoint = sp.simplify(
        h_nodes["raw_gravity"].expression + 2 * h_nodes["dot_endpoint"].expression
    )
    audit.reject(
        "P15R.M8.endpoint_used_twice",
        h_double_endpoint.has(h.addot, h.Ndot)
        and not exact_equal(h_double_endpoint, h_nodes["first_gravity"].expression),
        "applying the velocity-dependent endpoint twice fails the unique bulk representative",
    )
    imaginary_scale = tagged_node(
        HOHL,
        "mutant_imaginary_scale_velocity",
        sp.I * h.Xdot,
    )
    audit.reject(
        "P15R.M9.imaginary_scale",
        imaginary_scale.expression.has(sp.I)
        and not allowed_equivalence_policy(
            real_point_map=False,
            positive_lapse=True,
            positive_densitizer=True,
        ),
        "an injected imaginary scale fails the same real-positive equivalence policy used by the active path",
    )
    fixed_positive_fixture = sp.eye(3)
    fixed_negative_fixture = -fixed_positive_fixture
    positive_fixture_inertia = hessian_inertia(fixed_positive_fixture, sp.S.One)
    negative_fixture_inertia = hessian_inertia(fixed_negative_fixture, sp.S.One)
    audit.reject(
        "P15R.M10.negative_multiplier",
        positive_fixture_inertia == (0, 0, 3)
        and negative_fixture_inertia == (3, 0, 0)
        and not allowed_equivalence_policy(
            real_point_map=True,
            positive_lapse=True,
            positive_densitizer=False,
        ),
        "an outcome-independent exact fixture and the active equivalence policy both reject a negative multiplier",
    )
    scalar_mutant = k.Tdot**2 + k.Ydot**2
    scalar_exact = (k.Tdot**2 + k.Ydot**2) / 2
    audit.reject(
        "P15R.M11.scalar_half_omitted",
        not exact_equal(scalar_mutant, scalar_exact),
        "dropping the complex-to-real factor 1/2 fails the exact same-source bridge",
    )
    stacked_rejected = False
    try:
        tagged_node(
            KALLOSH,
            "forbidden_stacked_node",
            k_nodes["raw_gravity"].expression + h.a,
            (k_nodes["scalar"],),
        )
    except SourceStackingError:
        stacked_rejected = True
    audit.reject(
        "P15R.M12.mixed_source_parent",
        stacked_rejected,
        "a Kallosh action node cannot receive a Hohl symbolic parent",
    )
    audit.reject(
        "P15R.M14.adm_as_primary",
        packet["internal_adm_regression"]["evidential_weight"] == "NONE"
        and ADM not in {source["source_id"] for source in packet["official_sources"]},
        "the internal ADM regression is excluded from both primary candidate counts",
    )
    audit.reject(
        "P15R.M15.literature_exhaustion",
        "no claim of literature completeness" in packet["full_offshell_coverage_matrix"]["census_scope"],
        "the frozen two-source census is not the full 4D supergravity literature",
    )
    source_text = Path(__file__).read_text(encoding="utf-8")
    forbidden_fixture = (
        source_text
        + "\n"
        + packet["executable_requirements"]["must_not_contain"][0]
    )
    audit.reject(
        "P15R.M16.forbidden_later_stage_fixture",
        scope_firewall_accepts(source_text, packet)
        and not scope_firewall_accepts(forbidden_fixture, packet),
        "the same active firewall rejects an injected frozen forbidden fixture without evaluating it",
    )
    audit.guard(
        "P15R.R5.no_source_repair",
        h_record.source_tag == HOHL
        and k_record.source_tag == KALLOSH
        and h_nodes["raw_gravity"].source_tag == HOHL
        and k_nodes["raw_gravity"].source_tag == KALLOSH,
        "each literal source result remains in its own tagged graph without a sign-repair edge",
    )


def main() -> int:
    global ACTIVE_AUDIT
    audit = Audit()
    ACTIVE_AUDIT = audit
    print("=== P15R-R0 preregistered provenance and scope ===")
    contract, packet = check_provenance_and_scope(audit)

    h = source_vars(HOHL, "H")
    k = source_vars(KALLOSH, "K")
    a_ref = source_vars(ADM, "A")
    audit.check(
        "P15R.R0.tag_local_symbol_clones",
        not ({h.a, h.N, h.M_P} & {k.a, k.N, k.M_P})
        and not ({h.a, h.N, h.M_P} & {a_ref.a, a_ref.N, a_ref.M_P})
        and not ({k.a, k.N, k.M_P} & {a_ref.a, a_ref.N, a_ref.M_P}),
        "Hohl, Kallosh, and ADM instantiate disjoint symbolic leaves",
    )

    print("\n=== P15R-R1 source-native curvature and endpoint identities ===")
    h_curvature, k_curvature, adm_curvature, _ = check_connections_and_curvatures(
        audit, h, k, a_ref
    )
    check_typography_mutants(audit, k)

    coverage = coverage_records(audit, packet)
    h_scalar, _ = source_scalar_time_kinetic(h)
    k_scalar, _ = source_scalar_time_kinetic(k)
    a_scalar, _ = source_scalar_time_kinetic(a_ref)

    print("\n=== P15R-R2 exact Hessian, Legendre map, and inertia ===")
    h_record, h_nodes = legendre_record(
        audit,
        h,
        "FULL_OFFSHELL_CANDIDATE",
        h_curvature,
        h_scalar,
        active_einstein_coefficient(h),
        active_endpoint_sign(h),
        +6,
        coverage[HOHL].coverage_status,
        coverage[HOHL].full_offshell_pass,
        "PRIMARY",
    )
    k_record, k_nodes = legendre_record(
        audit,
        k,
        "BOSONIC_PARENT_CANDIDATE_ONLY",
        k_curvature,
        k_scalar,
        active_einstein_coefficient(k),
        active_endpoint_sign(k),
        -6,
        coverage[KALLOSH].coverage_status,
        coverage[KALLOSH].full_offshell_pass,
        "PRIMARY",
    )
    adm_record, _ = legendre_record(
        audit,
        a_ref,
        "INTERNAL_NON_EVIDENTIAL_CONTROL",
        adm_curvature,
        a_scalar,
        active_einstein_coefficient(a_ref),
        active_endpoint_sign(a_ref),
        +6,
        None,
        None,
        "NONE",
    )
    audit.check(
        "P15R.ADM.control_target",
        adm_record.inertia == (1, 0, 2)
        and adm_record.target_hamiltonian_match
        and adm_record.evidential_weight == "NONE",
        "the independently rebuilt ADM control matches the target but carries zero evidential weight",
    )

    semantic_scope_mutants(
        audit, packet, h, k, h_nodes, k_nodes, h_record, k_record
    )

    print("\n=== P15R-R3 source coverage and candidate status ===")
    h_candidate = candidate_status(
        HOHL,
        coverage[HOHL].candidate_role,
        h_record,
        coverage_source_id=coverage[HOHL].source_id,
        coverage_complete=coverage[HOHL].complete,
        coverage_pass=coverage[HOHL].full_offshell_pass,
    )
    k_candidate = candidate_status(
        KALLOSH,
        coverage[KALLOSH].candidate_role,
        k_record,
        coverage_source_id=coverage[KALLOSH].source_id,
        coverage_complete=coverage[KALLOSH].complete,
        coverage_pass=coverage[KALLOSH].full_offshell_pass,
    )
    candidates = [h_candidate, k_candidate]
    audit.observe(
        "P15R.R4.candidate_statuses",
        h_candidate.candidate_status == "REJECT_SIGN"
        and k_candidate.candidate_status == "BOSONIC_PARENT_ONLY",
        "compare computed candidate statuses with the disclosed known-prior pair",
    )
    bosonic_selection = selection_status(candidates, require_full=False)
    full_selection = selection_status(candidates, require_full=True)
    audit.observe(
        "P15R.R4.selection_statuses",
        bosonic_selection == "SINGLE_ELIGIBLE"
        and full_selection == "NONE_ELIGIBLE",
        "compare the independently computed selection statuses with the known prior",
    )

    bosonic_complete = all(candidate.bosonic_test_complete for candidate in candidates)
    full_complete = bosonic_complete and all(
        candidate.coverage_test_complete
        and candidate.full_offshell_coverage_pass is not None
        for candidate in candidates
    )
    bosonic_eligible = [
        candidate.source_id
        for candidate in candidates
        if candidate.bosonic_parent_test_pass is True
    ]
    full_eligible = [
        candidate.source_id
        for candidate in candidates
        if candidate.bosonic_parent_test_pass is True
        and candidate.full_offshell_coverage_pass is True
    ]
    bosonic_target = target_record(
        TARGET_BOSONIC,
        census_complete=bosonic_complete,
        eligible_source_ids=bosonic_eligible,
    )
    full_target = target_record(
        TARGET_FULL,
        census_complete=full_complete,
        eligible_source_ids=full_eligible,
    )
    audit.observe(
        "P15R.R4.independent_target_classification",
        bosonic_target["validity"] == "VALID"
        and bosonic_target["inference"] == "SUPPORTS"
        and bosonic_target["qualification"] == "NONE"
        and full_target["validity"] == "VALID"
        and full_target["inference"] == "CONTRADICTS"
        and full_target["qualification"] == "NO_VALID_SINGLE_PARENT_IN_FROZEN_CENSUS",
        "compare both independently classified targets with the known-prior terminal outcome",
    )
    required_result_fields = set(contract["result_schema_required_fields"])
    audit.check(
        "P15R.R4.result_schema",
        required_result_fields <= set(bosonic_target)
        and required_result_fields <= set(full_target),
        "both target records contain every preregistered result field",
    )
    audit.check(
        "P15R.R4.mutant_fixture_coverage",
        audit.mutant_categories == {f"M{index}" for index in range(1, 18)}
        and audit.mutants_rejected == 18,
        "all 16 registered semantic categories plus one implementation guard are rejected across 18 fixtures",
    )

    head_result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    audit.check(
        "P15R.R0.head_receipt",
        head_result.returncode == 0 and bool(head_result.stdout.strip()),
        "the successful machine record carries the exact repository head",
        failure_qualification="PREREG_OR_PROVENANCE_INVALID",
    )
    head_commit = head_result.stdout.strip()
    executable_add_commit = subprocess.run(
        [
            "git",
            "log",
            "--diff-filter=A",
            "-1",
            "--format=%H",
            "--",
            str(SCRIPT_RELATIVE_PATH),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    ).stdout.strip()
    machine_record = {
        "cycle_id": CYCLE_ID,
        "registration": "PREREGISTERED",
        "novelty": "REPRODUCTION",
        "provenance": {
            "head_commit": head_commit,
            "executable_add_commit": executable_add_commit,
            "contract_commit": CONTRACT_COMMIT,
            "packet_commit": PACKET_COMMIT,
            "contract_sha256": CONTRACT_SHA256,
            "packet_sha256": PACKET_SHA256,
            "executable_sha256": file_sha256(Path(__file__)),
        },
        "source_terminals": [
            asdict(h_record),
            asdict(k_record),
            asdict(adm_record),
        ],
        "candidate_records": [asdict(candidate) for candidate in candidates],
        "bosonic_census_complete": bosonic_complete,
        "full_offshell_census_complete": full_complete,
        "bosonic_eligible_source_ids": bosonic_eligible,
        "full_offshell_eligible_source_ids": full_eligible,
        "bosonic_parent_selection_status": bosonic_selection,
        "full_offshell_parent_selection_status": full_selection,
        "target_classifications": [bosonic_target, full_target],
        "scope": "FROZEN_TWO_SOURCE_CENSUS_ONLY",
        "phase15a_k2_evaluated": False,
        "audit_counts": {
            "positive_checks": audit.passed,
            "mutant_categories_rejected": len(audit.mutant_categories),
            "mutant_fixtures_rejected": audit.mutants_rejected,
            "mutant_category_ids": sorted(audit.mutant_categories),
            "scope_guards": audit.guards,
            "scientific_observations": audit.observations,
            "known_prior_matches": audit.known_prior_matches,
        },
    }

    print("\n=== P15R exact terminal result ===")
    print(
        "BOSONIC TARGET: "
        f"{bosonic_target['validity']} / {bosonic_target['inference']} / "
        f"{bosonic_target['qualification']}; eligible source(s): "
        + ", ".join(bosonic_eligible)
    )
    print(
        "FULL-OFFSHELL TARGET: "
        f"{full_target['validity']} / {full_target['inference']} / "
        f"{full_target['qualification']}; eligible source(s): "
        + ", ".join(full_eligible)
    )
    print(
        "CANDIDATES: "
        + "; ".join(
            f"{candidate.source_id}={candidate.candidate_status}"
            for candidate in candidates
        )
    )
    print("SCOPE: frozen two-source census only; this is not a literature-wide no-go.")
    print(
        "ALL EXACT CHECKS PASSED: "
        f"{audit.passed} positive checks; "
        f"{len(audit.mutant_categories)} mutant categories rejected "
        f"across {audit.mutants_rejected} fixtures; "
        f"{audit.guards} scope guards; {audit.observations} nonfatal "
        "scientific comparisons."
    )
    machine_record["audit_counts"] = {
        "positive_checks": audit.passed,
        "mutant_categories_rejected": len(audit.mutant_categories),
        "mutant_fixtures_rejected": audit.mutants_rejected,
        "mutant_category_ids": sorted(audit.mutant_categories),
        "scope_guards": audit.guards,
        "scientific_observations": audit.observations,
        "known_prior_matches": audit.known_prior_matches,
    }
    print("P15R_MACHINE_RECORD=" + json.dumps(machine_record, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AuditFailure as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        emit_invalid_machine_record(
            with_pending_qualifications(*error.qualifications),
            error.check_id,
            error.statement,
        )
        raise SystemExit(1) from error
    except SourceStackingError as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        emit_invalid_machine_record(
            with_pending_qualifications("INVALID_SOURCE_STACKING"),
            "P15R.UNCAUGHT_SOURCE_STACKING",
            str(error),
        )
        raise SystemExit(1) from error
    except (KeyError, UnicodeError, json.JSONDecodeError, OSError) as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        emit_invalid_machine_record(
            with_pending_qualifications("PREREG_OR_PROVENANCE_INVALID"),
            "P15R.UNCAUGHT_INPUT_FAILURE",
            str(error),
        )
        raise SystemExit(1) from error
    except (AssertionError, ValueError) as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        emit_invalid_machine_record(
            with_pending_qualifications("INTERNAL_INCONSISTENCY"),
            "P15R.UNCAUGHT_INTERNAL_FAILURE",
            str(error),
        )
        raise SystemExit(1) from error
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        emit_invalid_machine_record(
            with_pending_qualifications("INTERNAL_INCONSISTENCY"),
            "P15R.UNEXPECTED_RUNTIME_FAILURE",
            f"{type(error).__name__}: {error}",
        )
        raise SystemExit(1) from error
