#!/usr/bin/env python3
"""Phase 50: sampled stabilized m=4-to-m=5 joint-saddle homotopy.

This calculation embeds the retained Phase-41 m=4 saddles into one declared
nine-complex-dimensional ambient space, adds one reflection-odd mode per
field with a frozen (1 negative, 1 positive) holomorphic stabilizer, and
continues five source-labelled real saddles to the m=5 midpoint action.

It also transports the *local* upward tangent plane over declared positive
mobility paths.  It does not integrate a nonlinear upward cycle, continue a
Gamma-K intersection, classify ends, or emit a global Picard-Lefschetz
integer.  The program writes no files and emits one RESULT_JSON record.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import platform
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Mapping, Sequence

sys.dont_write_bytecode = True

import mpmath
import numpy as np
import scipy
import sympy as sp
from scipy.optimize import root


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent
INPUT_PATH = SCRIPT_PATH.with_name(
    "PHASE50_M4_M5_JOINT_SADDLE_HOMOTOPY_INPUTS.json"
)
PHASE41_SOURCE_PATH = SCRIPT_PATH.with_name(
    "phase41_m4_two_source_intersection.py"
)
PHASE42_CHECKPOINT_PATH = SCRIPT_PATH.with_name(
    "PHASE42_M4_FIXED_ROOT_CHECKPOINT.json"
)
PHASE49_RESULT_PATH = SCRIPT_PATH.with_name(
    "PHASE49_M4_CLONGDOUBLE_FULL_FLOW_STATE_MAP_REPAIR_RESULT.json"
)

INPUT_COMMIT = "5e6f04ed7ce40672169c4b6e0cfad8180ec985af"
INPUT_SHA256 = "24706b3b44c1ff426c7b593370acdb324cd39b7998c05ef52e3ba5b88d1e6444"
RESULT_SCHEMA = "ice-phase50-m4-m5-joint-saddle-homotopy/v1"
RESULT_PREFIX = "RESULT_JSON="

M4_DIMENSION = 7
M5_DIMENSION = 9
M5_SEGMENTS = 5


class InvalidRun(RuntimeError):
    """A frozen input, exact identity, or serialization invariant failed."""


def progress(message: str) -> None:
    print(f"[Phase50] {message}", file=sys.stderr, flush=True)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise InvalidRun(f"cannot load module: {path.name}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def load_unique_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            if key in output:
                raise InvalidRun(f"duplicate JSON key in {path.name}: {key}")
            output[key] = value
        return output

    payload = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=lambda token: (_ for _ in ()).throw(
            InvalidRun(f"nonfinite JSON token in {path.name}: {token}")
        ),
    )
    if not isinstance(payload, dict):
        raise InvalidRun(f"top-level JSON is not an object: {path.name}")
    return payload, raw


def json_ready(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        if np.iscomplexobj(value):
            array = np.asarray(value, dtype=np.complex128)
            return {
                "shape": list(array.shape),
                "complex128_pairs": [
                    [float(item.real), float(item.imag)]
                    for item in array.reshape(-1)
                ],
            }
        return np.asarray(value).tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, complex):
        return [float(value.real), float(value.imag)]
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        raise InvalidRun("attempted to retain a nonfinite float")
    return value


def canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        json_ready(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def verify_self_digest(payload: Mapping[str, Any], *, label: str) -> str:
    key_candidates = (
        "result_payload_sha256_without_self",
        "checkpoint_payload_sha256_without_self",
    )
    key = next((candidate for candidate in key_candidates if candidate in payload), None)
    if key is None:
        raise InvalidRun(f"{label} has no self-excluding digest")
    expected = str(payload[key])
    without = dict(payload)
    without.pop(key, None)
    observed = hashlib.sha256(canonical_bytes(without)).hexdigest()
    if observed != expected:
        raise InvalidRun(f"{label} self-excluding digest mismatch")
    return observed


@dataclass
class Audit:
    exact_records: list[dict[str, Any]] = field(default_factory=list)
    numerical_records: list[dict[str, Any]] = field(default_factory=list)

    def _unique(self, check_id: str) -> None:
        identifiers = {
            str(record["id"])
            for record in self.exact_records + self.numerical_records
        }
        if check_id in identifiers:
            raise InvalidRun(f"duplicate check id: {check_id}")

    def exact(
        self,
        check_id: str,
        condition: bool,
        statement: str,
        *,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        self._unique(check_id)
        record: dict[str, Any] = {
            "id": check_id,
            "kind": "exact",
            "status": "PASS" if condition else "INVALID_RUN",
            "passed": bool(condition),
            "failure_status": "INVALID_RUN",
            "statement": statement,
        }
        if details is not None:
            record["details"] = dict(details)
        self.exact_records.append(record)
        if not condition:
            raise InvalidRun(f"{check_id}: {statement}")

    def numerical(
        self,
        check_id: str,
        condition: bool,
        statement: str,
        *,
        failure_status: str,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        self._unique(check_id)
        record: dict[str, Any] = {
            "id": check_id,
            "kind": "numerical",
            "status": "PASS" if condition else failure_status,
            "passed": bool(condition),
            "failure_status": failure_status,
            "statement": statement,
        }
        if details is not None:
            record["details"] = dict(details)
        self.numerical_records.append(record)


@dataclass(frozen=True)
class M5SymbolicFamily:
    variables_z: tuple[sp.Symbol, ...]
    variables_w: tuple[sp.Symbol, ...]
    boundary_a: sp.Symbol
    boundary_phi: sp.Symbol
    delta_a: sp.Symbol
    delta_phi: sp.Symbol
    action_z: sp.Expr
    action_w: sp.Expr
    gradient_w: sp.Matrix
    hessian_w: sp.Matrix
    elements: tuple[sp.Expr, ...]


@dataclass(frozen=True)
class M5NumericModel:
    delta_a: float
    delta_phi: float
    action_expr: sp.Expr
    gradient_expr: sp.Matrix
    hessian_expr: sp.Matrix
    action_function: Callable[..., object]
    gradient_function: Callable[..., object]
    hessian_function: Callable[..., object]


@dataclass(frozen=True)
class Embedding:
    field_prolongation: np.ndarray
    added_mode: np.ndarray
    basis: np.ndarray
    inverse_basis: np.ndarray
    reflection_m4: np.ndarray
    reflection_m5: np.ndarray


def validate_inputs(
    manifest: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    if sha256_path(INPUT_PATH) != INPUT_SHA256:
        raise InvalidRun("Phase50 input manifest hash drift")
    if manifest.get("schema") != (
        "ice-phase50-m4-m5-joint-saddle-homotopy-inputs/v1"
    ):
        raise InvalidRun("Phase50 input schema drift")
    if manifest.get("phase") != 50:
        raise InvalidRun("Phase50 phase drift")
    if manifest["required_outputs"]["exact_check_count"] != 6:
        raise InvalidRun("Phase50 exact check-count drift")
    if manifest["required_outputs"]["numerical_check_count"] != 8:
        raise InvalidRun("Phase50 numerical check-count drift")

    observed: dict[str, Any] = {}
    for label, specification in manifest["pinned_inputs"].items():
        path = REPO_ROOT / str(specification["path"])
        digest = sha256_path(path)
        if digest != specification["sha256"]:
            raise InvalidRun(f"pinned input hash drift: {label}")
        observed[label] = {
            "path": specification["path"],
            "commit": specification["commit"],
            "sha256": digest,
            "role": specification.get("role"),
        }

    checkpoint, _ = load_unique_json(PHASE42_CHECKPOINT_PATH)
    phase49, _ = load_unique_json(PHASE49_RESULT_PATH)
    verify_self_digest(checkpoint, label="Phase42 checkpoint")
    verify_self_digest(phase49, label="Phase49 result")
    if checkpoint.get("checkpoint_status") != "POST_HOC_REGENERATED_CHECKPOINT":
        raise InvalidRun("Phase42 checkpoint status drift")
    if phase49.get("run_status") != "VALID_RUN" or phase49.get(
        "classification"
    ) != "FULL_FLOW_CLONGDOUBLE_STATE_MAP_REPAIR_SUPPORTED":
        raise InvalidRun("Phase49 upstream readiness status drift")
    return observed, checkpoint, phase49


def build_embedding() -> Embedding:
    prolongation = np.array(
        [
            [4.0 / 5.0, 0.0, 0.0],
            [2.0 / 5.0, 3.0 / 5.0, 0.0],
            [0.0, 3.0 / 5.0, 2.0 / 5.0],
            [0.0, 0.0, 4.0 / 5.0],
        ],
        dtype=float,
    )
    added = np.array([-1.0, 2.0, -2.0, 1.0], dtype=float) / np.sqrt(10.0)
    basis = np.zeros((M5_DIMENSION, M5_DIMENSION), dtype=float)
    for fine in range(4):
        for coarse in range(3):
            basis[2 * fine, 2 * coarse] = prolongation[fine, coarse]
            basis[2 * fine + 1, 2 * coarse + 1] = prolongation[fine, coarse]
        basis[2 * fine, 7] = added[fine]
        basis[2 * fine + 1, 8] = added[fine]
    basis[8, 6] = 1.0
    reflection_m4 = np.zeros((M4_DIMENSION, M4_DIMENSION), dtype=float)
    reflection_m5 = np.zeros((M5_DIMENSION, M5_DIMENSION), dtype=float)
    for node in range(3):
        reflection_m4[2 * (2 - node), 2 * node] = 1.0
        reflection_m4[2 * (2 - node) + 1, 2 * node + 1] = 1.0
    reflection_m4[6, 6] = 1.0
    for node in range(4):
        reflection_m5[2 * (3 - node), 2 * node] = 1.0
        reflection_m5[2 * (3 - node) + 1, 2 * node + 1] = 1.0
    reflection_m5[8, 8] = 1.0
    return Embedding(
        field_prolongation=prolongation,
        added_mode=added,
        basis=basis,
        inverse_basis=np.linalg.inv(basis),
        reflection_m4=reflection_m4,
        reflection_m5=reflection_m5,
    )


def coordinate_scales(phase41: ModuleType, segments: int) -> np.ndarray:
    return np.array(
        [phase41.BASE_A, phase41.BASE_PHI] * (segments - 1)
        + [phase41.TIME_SCALE],
        dtype=float,
    )


def anchor_w(
    phase41: ModuleType,
    segments: int,
    delta_a: float,
    delta_phi: float,
) -> np.ndarray:
    left_a = phase41.BASE_A * (1.0 - delta_a / 2.0)
    right_a = phase41.BASE_A * (1.0 + delta_a / 2.0)
    left_phi = phase41.BASE_PHI - delta_phi / 2.0
    right_phi = phase41.BASE_PHI + delta_phi / 2.0
    values: list[float] = []
    for node in range(1, segments):
        fraction = node / segments
        values.extend(
            [
                ((1.0 - fraction) * left_a + fraction * right_a)
                / phase41.BASE_A,
                ((1.0 - fraction) * left_phi + fraction * right_phi)
                / phase41.BASE_PHI,
            ]
        )
    values.append(0.0)
    return np.asarray(values, dtype=float)


@lru_cache(maxsize=1)
def build_m5_symbolic_family() -> M5SymbolicFamily:
    phase41 = load_module("ice_phase41_symbolic_for_phase50", PHASE41_SOURCE_PATH)
    variables_z = sp.symbols(
        "a_1 phi_1 a_2 phi_2 a_3 phi_3 a_4 phi_4 T"
    )
    variables_w = sp.symbols(
        "w_a1 w_phi1 w_a2 w_phi2 w_a3 w_phi3 w_a4 w_phi4 w_T"
    )
    boundary_a, boundary_phi = sp.symbols(
        "a_boundary phi_boundary", real=True
    )
    delta_a, delta_phi = sp.symbols("delta_a delta_phi", real=True)
    left = (
        boundary_a * (1 - delta_a / 2),
        boundary_phi - delta_phi / 2,
    )
    right = (
        boundary_a * (1 + delta_a / 2),
        boundary_phi + delta_phi / 2,
    )
    nodes = (
        left,
        *((variables_z[2 * index], variables_z[2 * index + 1]) for index in range(4)),
        right,
    )
    proper_time = variables_z[-1]
    step = sp.Rational(1, M5_SEGMENTS)
    elements = tuple(
        phase41.midpoint_element(
            nodes[index][0],
            nodes[index][1],
            nodes[index + 1][0],
            nodes[index + 1][1],
            proper_time,
            step,
        )
        for index in range(M5_SEGMENTS)
    )
    action_z = sp.expand(sum(elements))
    scales = coordinate_scales(phase41, M5_SEGMENTS)
    substitutions: dict[sp.Symbol, sp.Expr] = {
        boundary_a: sp.Float(str(phase41.BASE_A), 50),
        boundary_phi: sp.Float(str(phase41.BASE_PHI), 50),
    }
    for index, variable in enumerate(variables_z):
        substitutions[variable] = (
            sp.Float(str(scales[index]), 50) * variables_w[index]
        )
    action_w = action_z.subs(substitutions)
    gradient_w = sp.Matrix(
        [sp.diff(action_w, variable) for variable in variables_w]
    )
    hessian_w = sp.hessian(action_w, variables_w)
    return M5SymbolicFamily(
        variables_z=variables_z,
        variables_w=variables_w,
        boundary_a=boundary_a,
        boundary_phi=boundary_phi,
        delta_a=delta_a,
        delta_phi=delta_phi,
        action_z=action_z,
        action_w=action_w,
        gradient_w=gradient_w,
        hessian_w=hessian_w,
        elements=elements,
    )


@lru_cache(maxsize=None)
def m5_numeric_model(delta_a: float, delta_phi: float) -> M5NumericModel:
    family = build_m5_symbolic_family()
    substitutions = {
        family.delta_a: sp.Float(str(delta_a), 50),
        family.delta_phi: sp.Float(str(delta_phi), 50),
    }
    action = family.action_w.subs(substitutions)
    gradient = family.gradient_w.subs(substitutions)
    hessian = family.hessian_w.subs(substitutions)
    return M5NumericModel(
        delta_a=float(delta_a),
        delta_phi=float(delta_phi),
        action_expr=action,
        gradient_expr=gradient,
        hessian_expr=hessian,
        action_function=sp.lambdify((family.variables_w,), action, "numpy"),
        gradient_function=sp.lambdify((family.variables_w,), gradient, "numpy"),
        hessian_function=sp.lambdify((family.variables_w,), hessian, "numpy"),
    )


def m5_action(model: M5NumericModel, w: np.ndarray) -> complex:
    return complex(model.action_function(tuple(w)))


def m5_gradient(model: M5NumericModel, w: np.ndarray) -> np.ndarray:
    return np.asarray(
        model.gradient_function(tuple(w)), dtype=np.complex128
    ).reshape(M5_DIMENSION)


def m5_hessian(model: M5NumericModel, w: np.ndarray) -> np.ndarray:
    return np.asarray(
        model.hessian_function(tuple(w)), dtype=np.complex128
    ).reshape(M5_DIMENSION, M5_DIMENSION)


def lifted_evaluate(
    phase41: ModuleType,
    model4: Any,
    w5: np.ndarray,
    delta_a: float,
    delta_phi: float,
    kappa_a: float,
    kappa_phi: float,
    embedding: Embedding,
    *,
    basis: np.ndarray | None = None,
    inverse_basis: np.ndarray | None = None,
) -> tuple[complex, np.ndarray, np.ndarray, np.ndarray]:
    selected_basis = embedding.basis if basis is None else np.asarray(basis, dtype=float)
    selected_inverse = (
        embedding.inverse_basis
        if inverse_basis is None
        else np.asarray(inverse_basis, dtype=float)
    )
    anchor4 = anchor_w(phase41, 4, delta_a, delta_phi)
    anchor5 = anchor_w(phase41, 5, delta_a, delta_phi)
    coordinates = selected_inverse @ (np.asarray(w5, dtype=float) - anchor5)
    w4 = anchor4 + coordinates[:M4_DIMENSION]
    action = (
        phase41.action_at(model4, w4)
        + 0.5 * kappa_a * coordinates[7] ** 2
        + 0.5 * kappa_phi * coordinates[8] ** 2
    )
    gradient_c = np.concatenate(
        [
            phase41.gradient_at(model4, w4),
            np.array(
                [kappa_a * coordinates[7], kappa_phi * coordinates[8]],
                dtype=np.complex128,
            ),
        ]
    )
    hessian_c = np.zeros((M5_DIMENSION, M5_DIMENSION), dtype=np.complex128)
    hessian_c[:M4_DIMENSION, :M4_DIMENSION] = phase41.hessian_at(model4, w4)
    hessian_c[7, 7] = kappa_a
    hessian_c[8, 8] = kappa_phi
    gradient = selected_inverse.T @ gradient_c
    hessian = selected_inverse.T @ hessian_c @ selected_inverse
    reconstructed = anchor5 + selected_basis @ coordinates
    if np.linalg.norm(reconstructed - w5) > 1.0e-10:
        raise InvalidRun("common-ambient basis reconstruction drift")
    return action, gradient, hessian, coordinates


def homotopy_evaluate(
    phase41: ModuleType,
    model4: Any,
    model5: M5NumericModel,
    w5: np.ndarray,
    lambda_value: float,
    delta_a: float,
    delta_phi: float,
    kappa_a: float,
    kappa_phi: float,
    embedding: Embedding,
) -> tuple[complex, np.ndarray, np.ndarray, dict[str, Any]]:
    action4, gradient4, hessian4, coordinates = lifted_evaluate(
        phase41,
        model4,
        w5,
        delta_a,
        delta_phi,
        kappa_a,
        kappa_phi,
        embedding,
    )
    action5 = m5_action(model5, w5)
    gradient5 = m5_gradient(model5, w5)
    hessian5 = m5_hessian(model5, w5)
    complement = 1.0 - float(lambda_value)
    action = complement * action4 + float(lambda_value) * action5
    gradient = complement * gradient4 + float(lambda_value) * gradient5
    hessian = complement * hessian4 + float(lambda_value) * hessian5
    return action, gradient, hessian, {
        "lifted_action": action4,
        "m5_action": action5,
        "lifted_gradient": gradient4,
        "m5_gradient": gradient5,
        "lifted_hessian": hessian4,
        "m5_hessian": hessian5,
        "common_coordinates": coordinates,
    }


def embedded_m4_root(
    phase41: ModuleType,
    checkpoint: Mapping[str, Any],
    label: str,
    delta_a: float,
    delta_phi: float,
    embedding: Embedding,
) -> np.ndarray:
    record = checkpoint["saddles"][label]["saddle_w"]
    values = np.asarray(record["values"], dtype=float)
    if values.shape != (M4_DIMENSION,) or not np.all(np.isfinite(values)):
        raise InvalidRun(f"invalid Phase42 m4 saddle record: {label}")
    common = np.concatenate([values - anchor_w(phase41, 4, delta_a, delta_phi), [0.0, 0.0]])
    return anchor_w(phase41, 5, delta_a, delta_phi) + embedding.basis @ common


def inertia_record(eigenvalues: np.ndarray) -> dict[str, int]:
    values = np.asarray(eigenvalues, dtype=float)
    zero_tolerance = 1.0e-9
    return {
        "negative": int(np.count_nonzero(values < -zero_tolerance)),
        "positive": int(np.count_nonzero(values > zero_tolerance)),
        "zero": int(np.count_nonzero(np.abs(values) <= zero_tolerance)),
    }


def solve_node(
    phase41: ModuleType,
    model4: Any,
    model5: M5NumericModel,
    seed: np.ndarray,
    lambda_value: float,
    delta_a: float,
    delta_phi: float,
    kappa_a: float,
    kappa_phi: float,
    embedding: Embedding,
    solver_spec: Mapping[str, Any],
    thresholds: Mapping[str, Any],
) -> tuple[np.ndarray, dict[str, Any]]:
    def values(candidate: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        _action, gradient, hessian, _parts = homotopy_evaluate(
            phase41,
            model4,
            model5,
            candidate,
            lambda_value,
            delta_a,
            delta_phi,
            kappa_a,
            kappa_phi,
            embedding,
        )
        return gradient.real, hessian.real

    solution = root(
        lambda candidate: values(candidate)[0],
        np.asarray(seed, dtype=float),
        jac=lambda candidate: values(candidate)[1],
        method=str(solver_spec["method"]),
        options={"xtol": float(solver_spec["xtol"])},
    )
    candidate = np.asarray(solution.x, dtype=float)
    action, gradient, hessian, parts = homotopy_evaluate(
        phase41,
        model4,
        model5,
        candidate,
        lambda_value,
        delta_a,
        delta_phi,
        kappa_a,
        kappa_phi,
        embedding,
    )
    hessian_real = 0.5 * (hessian.real + hessian.real.T)
    eigenvalues = np.linalg.eigvalsh(hessian_real)
    residual = float(np.max(np.abs(gradient)))
    norm = float(np.linalg.norm(candidate))
    finite = bool(
        np.all(np.isfinite(candidate))
        and np.all(np.isfinite(gradient))
        and np.all(np.isfinite(hessian))
        and np.all(np.isfinite(eigenvalues))
    )
    accepted = bool(
        finite
        and residual <= float(thresholds["gradient_max_abs"])
        and norm < float(thresholds["saddle_w_norm_max"])
    )
    return candidate, {
        "lambda": float(lambda_value),
        "accepted": accepted,
        "finite": finite,
        "solver_success": bool(solution.success),
        "solver_message": str(solution.message),
        "nfev": int(solution.nfev),
        "njev": None if getattr(solution, "njev", None) is None else int(solution.njev),
        "w5": candidate,
        "action": action,
        "gradient_max_abs": residual,
        "gradient_imag_max_abs": float(np.max(np.abs(gradient.imag))),
        "hessian_imag_max_abs": float(np.max(np.abs(hessian.imag))),
        "hessian_eigenvalues": eigenvalues,
        "hessian_min_abs_eigenvalue": float(np.min(np.abs(eigenvalues))),
        "hessian_inertia": inertia_record(eigenvalues),
        "saddle_w_norm": norm,
        "added_coordinates": np.asarray(parts["common_coordinates"])[7:9],
    }


def continue_path(
    phase41: ModuleType,
    model4: Any,
    model5: M5NumericModel,
    start: np.ndarray,
    lambdas: Sequence[float],
    delta_a: float,
    delta_phi: float,
    kappa_a: float,
    kappa_phi: float,
    embedding: Embedding,
    solver_spec: Mapping[str, Any],
    thresholds: Mapping[str, Any],
) -> dict[str, Any]:
    current = np.asarray(start, dtype=float).copy()
    records: list[dict[str, Any]] = []
    terminated_at: float | None = None
    for lambda_value in lambdas:
        current, record = solve_node(
            phase41,
            model4,
            model5,
            current,
            float(lambda_value),
            delta_a,
            delta_phi,
            kappa_a,
            kappa_phi,
            embedding,
            solver_spec,
            thresholds,
        )
        records.append(record)
        if not record["accepted"] and terminated_at is None:
            terminated_at = float(lambda_value)
    return {
        "requested_node_count": len(lambdas),
        "retained_node_count": len(records),
        "completed": len(records) == len(lambdas) and terminated_at is None,
        "terminated_at": terminated_at,
        "records": records,
        "endpoint": current,
    }


def path_map(path: Mapping[str, Any]) -> dict[float, Mapping[str, Any]]:
    return {
        round(float(record["lambda"]), 12): record
        for record in path["records"]
    }


def path_passed(path: Mapping[str, Any], thresholds: Mapping[str, Any]) -> bool:
    expected = thresholds["required_hessian_inertia"]
    return bool(
        path["completed"]
        and all(
            record["accepted"]
            and record["hessian_min_abs_eigenvalue"]
            >= float(thresholds["hessian_min_abs_eigenvalue"])
            and record["hessian_inertia"] == expected
            for record in path["records"]
        )
    )


def symmetric_relative(left: np.ndarray, right: np.ndarray) -> float:
    a = np.asarray(left)
    b = np.asarray(right)
    return float(
        np.linalg.norm(a - b)
        / max(float(np.linalg.norm(a)), float(np.linalg.norm(b)), 1.0e-300)
    )


def tangent_controls(
    phase41: ModuleType,
    model4: Any,
    model5: M5NumericModel,
    fine_path: Mapping[str, Any],
    delta_a: float,
    delta_phi: float,
    kappa_a: float,
    kappa_phi: float,
    embedding: Embedding,
    solver_spec: Mapping[str, Any],
    numerics: Mapping[str, Any],
    thresholds: Mapping[str, Any],
) -> dict[str, Any]:
    nodes = path_map(fine_path)
    records: list[dict[str, Any]] = []
    all_passed = True
    for lambda_value in numerics["implicit_tangent_lambda_samples_in_order"]:
        base = nodes[round(float(lambda_value), 12)]
        w = np.asarray(base["w5"], dtype=float)
        _action, _gradient, hessian, parts = homotopy_evaluate(
            phase41,
            model4,
            model5,
            w,
            float(lambda_value),
            delta_a,
            delta_phi,
            kappa_a,
            kappa_phi,
            embedding,
        )
        partial_lambda_gradient = parts["m5_gradient"] - parts["lifted_gradient"]
        implicit = -np.linalg.solve(hessian.real, partial_lambda_gradient.real)
        step_records: list[dict[str, Any]] = []
        columns: list[np.ndarray] = []
        for step in numerics["implicit_tangent_central_steps_in_order"]:
            h = float(step)
            minus, minus_record = solve_node(
                phase41,
                model4,
                model5,
                w - h * implicit,
                float(lambda_value) - h,
                delta_a,
                delta_phi,
                kappa_a,
                kappa_phi,
                embedding,
                solver_spec,
                thresholds,
            )
            plus, plus_record = solve_node(
                phase41,
                model4,
                model5,
                w + h * implicit,
                float(lambda_value) + h,
                delta_a,
                delta_phi,
                kappa_a,
                kappa_phi,
                embedding,
                solver_spec,
                thresholds,
            )
            column = (plus - minus) / (2.0 * h)
            relative = symmetric_relative(column, implicit)
            passed = bool(
                minus_record["accepted"]
                and plus_record["accepted"]
                and relative
                <= float(
                    thresholds[
                        "implicit_to_finite_difference_tangent_symmetric_relative_max"
                    ]
                )
            )
            columns.append(column)
            step_records.append(
                {
                    "step": h,
                    "minus": minus_record,
                    "plus": plus_record,
                    "finite_difference": column,
                    "implicit_symmetric_relative": relative,
                    "passed": passed,
                }
            )
        adjacent = symmetric_relative(columns[0], columns[1])
        sample_passed = bool(
            all(record["passed"] for record in step_records)
            and adjacent
            <= float(thresholds["adjacent_tangent_step_relative_change_max"])
        )
        all_passed = all_passed and sample_passed
        records.append(
            {
                "lambda": float(lambda_value),
                "implicit_tangent": implicit,
                "steps": step_records,
                "adjacent_step_symmetric_relative": adjacent,
                "passed": sample_passed,
            }
        )
    return {"records": records, "all_passed": all_passed}


def deterministic_oriented_eigenframe(
    matrix: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eigh(0.5 * (matrix + matrix.T))
    for column in range(vectors.shape[1]):
        pivot = int(np.argmax(np.abs(vectors[:, column])))
        if vectors[pivot, column] < 0.0:
            vectors[:, column] *= -1.0
    if np.linalg.det(vectors) < 0.0:
        vectors[:, -1] *= -1.0
    return values, vectors


def natural_mobility(hessian: np.ndarray) -> np.ndarray:
    values, vectors = deterministic_oriented_eigenframe(hessian)
    if np.min(np.abs(values)) <= 0.0:
        raise InvalidRun("cannot build mobility from singular Hessian")
    return vectors @ np.diag(1.0 / np.abs(values)) @ vectors.T


def symmetric_power(matrix: np.ndarray, exponent: float) -> np.ndarray:
    values, vectors = np.linalg.eigh(0.5 * (matrix + matrix.T))
    if np.min(values) <= 0.0:
        raise InvalidRun("SPD matrix power received a nonpositive eigenvalue")
    return vectors @ np.diag(values**float(exponent)) @ vectors.T


def geodesic_mobility(mobility0: np.ndarray, mobility1: np.ndarray, mu: float) -> np.ndarray:
    root0 = symmetric_power(mobility0, 0.5)
    inverse_root0 = symmetric_power(mobility0, -0.5)
    middle = inverse_root0 @ mobility1 @ inverse_root0
    output = root0 @ symmetric_power(middle, float(mu)) @ root0
    return 0.5 * (output + output.T)


def affine_mobility(mobility0: np.ndarray, mobility1: np.ndarray, mu: float) -> np.ndarray:
    output = (1.0 - float(mu)) * mobility0 + float(mu) * mobility1
    return 0.5 * (output + output.T)


def real_frame(complex_frame: np.ndarray) -> np.ndarray:
    values = np.asarray(complex_frame, dtype=np.complex128)
    columns: list[np.ndarray] = []
    for column in range(values.shape[1]):
        vector = values[:, column]
        realified = np.empty(2 * vector.size, dtype=float)
        realified[0::2] = vector.real
        realified[1::2] = vector.imag
        columns.append(realified)
    return np.column_stack(columns)


def oriented_qr(frame: np.ndarray) -> np.ndarray:
    q, r = np.linalg.qr(np.asarray(frame, dtype=float), mode="reduced")
    signs = np.where(np.diag(r) < 0.0, -1.0, 1.0)
    q = q @ np.diag(signs)
    return q


def upward_blocks(hessian: np.ndarray, mobility: np.ndarray) -> dict[str, Any]:
    factor = np.linalg.cholesky(0.5 * (mobility + mobility.T))
    whitened = factor.T @ hessian @ factor
    values, vectors = deterministic_oriented_eigenframe(whitened)
    negative = np.flatnonzero(values < 0.0)
    positive = np.flatnonzero(values > 0.0)
    if negative.size != 5 or positive.size != 4:
        raise InvalidRun("upward-plane construction encountered inertia drift")
    negative_complex = -factor @ vectors[:, negative]
    positive_complex = 1j * factor @ vectors[:, positive]
    negative_frame = oriented_qr(real_frame(negative_complex))
    positive_frame = oriented_qr(real_frame(positive_complex))
    combined = np.column_stack([negative_frame, positive_frame])
    return {
        "negative": negative_frame,
        "positive": positive_frame,
        "combined": combined,
        "whitened_eigenvalues": values,
        "factor_residual": float(
            np.linalg.norm(factor @ factor.T - mobility, ord=2)
            / max(np.linalg.norm(mobility, ord=2), 1.0e-300)
        ),
    }


def align_block(raw: np.ndarray, previous: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    left, singular_values, right_transpose = np.linalg.svd(raw.T @ previous)
    rotation = left @ right_transpose
    return raw @ rotation, singular_values, float(np.linalg.det(rotation))


def transport_upward_path(
    coordinates: Sequence[tuple[float, float]],
    node_lookup: Mapping[float, Mapping[str, Any]],
    mobility_function: Callable[[float], np.ndarray],
) -> dict[str, Any]:
    previous_negative: np.ndarray | None = None
    previous_positive: np.ndarray | None = None
    records: list[dict[str, Any]] = []
    minimum_overlap = 1.0
    for lambda_value, mu in coordinates:
        node = node_lookup[round(float(lambda_value), 12)]
        hessian = np.asarray(node["hessian_matrix"], dtype=float)
        mobility = mobility_function(float(mu))
        hessian_values = np.linalg.eigvalsh(hessian)
        if (
            not bool(node.get("accepted", False))
            or inertia_record(hessian_values)
            != {"negative": 5, "positive": 4, "zero": 0}
        ):
            records.append(
                {
                    "lambda": float(lambda_value),
                    "mu": float(mu),
                    "transport_status": "SKIPPED_INVALID_OR_INERTIA_CHANGED_SADDLE",
                    "saddle_accepted": bool(node.get("accepted", False)),
                    "hessian_inertia": inertia_record(hessian_values),
                }
            )
            return {
                "coordinates": records,
                "completed": False,
                "failure": "invalid saddle or Hessian inertia change on transport path",
                "minimum_consecutive_principal_overlap": 0.0,
                "endpoint_frame": None,
            }
        raw = upward_blocks(hessian, mobility)
        negative = raw["negative"]
        positive = raw["positive"]
        negative_singular = np.ones(negative.shape[1])
        positive_singular = np.ones(positive.shape[1])
        negative_gauge = 1.0
        positive_gauge = 1.0
        if previous_negative is not None and previous_positive is not None:
            negative, negative_singular, negative_gauge = align_block(
                negative, previous_negative
            )
            positive, positive_singular, positive_gauge = align_block(
                positive, previous_positive
            )
            minimum_overlap = min(
                minimum_overlap,
                float(np.min(negative_singular)),
                float(np.min(positive_singular)),
            )
        previous_negative = negative
        previous_positive = positive
        records.append(
            {
                "lambda": float(lambda_value),
                "mu": float(mu),
                "negative_step_principal_overlaps": negative_singular,
                "positive_step_principal_overlaps": positive_singular,
                "negative_raw_gauge_rotation_sign": negative_gauge,
                "positive_raw_gauge_rotation_sign": positive_gauge,
                "whitened_hessian_eigenvalues": raw["whitened_eigenvalues"],
                "mobility_min_eigenvalue": float(np.min(np.linalg.eigvalsh(mobility))),
                "mobility_condition_number": float(np.linalg.cond(mobility)),
                "cholesky_relative_residual": raw["factor_residual"],
            }
        )
    if previous_negative is None or previous_positive is None:
        raise InvalidRun("empty upward transport path")
    endpoint = np.column_stack([previous_negative, previous_positive])
    return {
        "coordinates": records,
        "completed": True,
        "failure": None,
        "minimum_consecutive_principal_overlap": minimum_overlap,
        "endpoint_frame": endpoint,
    }


def frame_comparison(left: np.ndarray, right: np.ndarray) -> dict[str, Any]:
    overlap = np.asarray(left).T @ np.asarray(right)
    singular_values = np.linalg.svd(overlap, compute_uv=False)
    determinant = float(np.linalg.det(overlap))
    return {
        "principal_overlaps": singular_values,
        "minimum_principal_overlap": float(np.min(singular_values)),
        "oriented_overlap_determinant": determinant,
        "orientation_sign": int(np.sign(determinant)),
    }


def unavailable_frame_comparison(reason: str) -> dict[str, Any]:
    return {
        "principal_overlaps": [],
        "minimum_principal_overlap": 0.0,
        "oriented_overlap_determinant": 0.0,
        "orientation_sign": 0,
        "available": False,
        "reason": reason,
    }


def exact_controls(
    audit: Audit,
    manifest: Mapping[str, Any],
    validated_inputs: Mapping[str, Any],
    phase41: ModuleType,
    embedding: Embedding,
) -> dict[str, Any]:
    audit.exact(
        "P50.inputs.pinned_provenance",
        sha256_path(INPUT_PATH) == INPUT_SHA256
        and all(record["sha256"] for record in validated_inputs.values()),
        "the frozen manifest and every pinned upstream artifact reproduce their declared bytes",
        details={"input_commit": INPUT_COMMIT, "input_sha256": INPUT_SHA256},
    )

    family = build_m5_symbolic_family()
    proper_time = family.variables_w[-1]
    residue = sp.simplify(sp.limit(proper_time * family.action_w, proper_time, 0))
    derivatives_coherent = bool(
        family.action_z == sp.expand(sum(family.elements))
        and family.gradient_w
        == sp.Matrix([sp.diff(family.action_w, item) for item in family.variables_w])
        and family.hessian_w == sp.hessian(family.action_w, family.variables_w)
    )
    audit.exact(
        "P50.action.single_scalar_five_elements",
        derivatives_coherent
        and not family.action_w.has(sp.conjugate)
        and residue != 0,
        "one holomorphic five-element midpoint scalar generates the m=5 gradient and Hessian off T=0",
        details={"t_zero_residue_nonzero": residue != 0},
    )

    p = sp.Matrix(
        [
            [sp.Rational(4, 5), 0, 0],
            [sp.Rational(2, 5), sp.Rational(3, 5), 0],
            [0, sp.Rational(3, 5), sp.Rational(2, 5)],
            [0, 0, sp.Rational(4, 5)],
        ]
    )
    q = sp.Matrix([-1, 2, -2, 1]) / sp.sqrt(10)
    left_inverse = (p.T * p).inv() * p.T
    b = sp.zeros(9, 9)
    for fine in range(4):
        for coarse in range(3):
            b[2 * fine, 2 * coarse] = p[fine, coarse]
            b[2 * fine + 1, 2 * coarse + 1] = p[fine, coarse]
        b[2 * fine, 7] = q[fine]
        b[2 * fine + 1, 8] = q[fine]
    b[8, 6] = 1
    determinant = sp.simplify(b.det())
    audit.exact(
        "P50.embedding.retraction_complement_and_orientation",
        left_inverse * p == sp.eye(3)
        and p.T * q == sp.zeros(3, 1)
        and sp.simplify(q.dot(q)) == 1
        and determinant == sp.Rational(1152, 3125),
        "the centered affine lift has an exact left inverse, a normalized complement, and positive global orientation",
        details={"determinant": str(determinant)},
    )

    reflection4 = sp.zeros(3, 3)
    reflection5 = sp.zeros(4, 4)
    for index in range(3):
        reflection4[2 - index, index] = 1
    for index in range(4):
        reflection5[3 - index, index] = 1
    symbolic_reflection = {
        family.variables_z[2 * index]: family.variables_z[2 * (3 - index)]
        for index in range(4)
    }
    symbolic_reflection.update(
        {
            family.variables_z[2 * index + 1]: family.variables_z[2 * (3 - index) + 1]
            for index in range(4)
        }
    )
    symbolic_reflection[family.delta_a] = -family.delta_a
    symbolic_reflection[family.delta_phi] = -family.delta_phi
    reflected_action = sp.simplify(
        family.action_z.subs(symbolic_reflection, simultaneous=True)
        - family.action_z
    )
    audit.exact(
        "P50.reflection.source_embedding_covariance",
        reflection5 * p == p * reflection4
        and reflection5 * q == -q
        and reflected_action == 0,
        "the m=5 action, centered prolongation, and two added odd modes obey signed-source nodal reflection",
    )

    coarse = sp.Matrix([2, 3, 2])
    fine = sp.ones(4, 1) + p * (coarse - sp.ones(3, 1))

    def witness_action(values: Sequence[sp.Expr], segments: int) -> sp.Expr:
        nodes = [(value, sp.Integer(0)) for value in values]
        return sp.simplify(
            sum(
                phase41.midpoint_element(
                    nodes[index][0],
                    nodes[index][1],
                    nodes[index + 1][0],
                    nodes[index + 1][1],
                    sp.Integer(1),
                    sp.Rational(1, segments),
                )
                for index in range(segments)
            )
        )

    nonnesting = sp.simplify(
        witness_action([1, *list(fine), 1], 5)
        - witness_action([1, *list(coarse), 1], 4)
    )
    audit.exact(
        "P50.homotopy.stabilized_lift_not_action_nesting",
        nonnesting == 54 * sp.pi**2,
        "the declared bridge has the frozen lambda endpoints but the affine m=4 grid is not an exact m=5 action nesting",
        details={"exact_nonnesting_witness": str(nonnesting)},
    )

    required = manifest["required_outputs"]
    guard = bool(
        required["bounded_chain_signed_sum"] is None
        and required["complete_global_signed_intersection_vector"] is None
        and required["global_n_sigma"] is None
        and required["cutoff_limit"] is None
        and required["continuum_limit"] is None
        and required["physical_original_cycle"] is None
        and required["gate1"] == "OPEN_PARTIAL_PROGRESS"
        and required["global_promotion"] == "PROHIBITED"
    )
    audit.exact(
        "P50.guard.sampled_local_transport_forces_global_nulls",
        guard,
        "the sampled stabilized saddle and local-plane transport cannot emit a cutoff limit, physical cycle, or global integer",
    )
    return {
        "field_prolongation": embedding.field_prolongation,
        "added_mode": embedding.added_mode,
        "basis": embedding.basis,
        "basis_determinant": float(np.linalg.det(embedding.basis)),
        "exact_nonnesting_witness": str(nonnesting),
        "m5_t_zero_residue_nonzero": residue != 0,
    }


def prepare_node_lookup(
    phase41: ModuleType,
    model4: Any,
    model5: M5NumericModel,
    path: Mapping[str, Any],
    delta_a: float,
    delta_phi: float,
    kappa_a: float,
    kappa_phi: float,
    embedding: Embedding,
) -> dict[float, dict[str, Any]]:
    output: dict[float, dict[str, Any]] = {}
    for record in path["records"]:
        lambda_value = float(record["lambda"])
        _action, _gradient, hessian, _parts = homotopy_evaluate(
            phase41,
            model4,
            model5,
            np.asarray(record["w5"], dtype=float),
            lambda_value,
            delta_a,
            delta_phi,
            kappa_a,
            kappa_phi,
            embedding,
        )
        enriched = dict(record)
        enriched["hessian_matrix"] = 0.5 * (hessian.real + hessian.real.T)
        output[round(lambda_value, 12)] = enriched
    return output


def run() -> dict[str, Any]:
    manifest, _manifest_raw = load_unique_json(INPUT_PATH)
    validated_inputs, checkpoint, phase49 = validate_inputs(manifest)
    phase41 = load_module("ice_phase41_for_phase50", PHASE41_SOURCE_PATH)
    embedding = build_embedding()
    audit = Audit()
    progress("run exact common-ambient, action, reflection, and scope controls")
    exact_payload = exact_controls(
        audit, manifest, validated_inputs, phase41, embedding
    )

    numerics = manifest["fixed_numerics"]
    thresholds = manifest["fixed_thresholds"]
    solver_spec = numerics["primary_solver"]
    fine_mesh = [float(value) for value in numerics["fine_lambda_mesh_in_order"]]
    coarse_mesh = [float(value) for value in numerics["coarse_lambda_mesh_in_order"]]
    mu_mesh = [float(value) for value in numerics["metric_mu_mesh_in_order"]]
    stabilizers = manifest["action_homotopy"]["added_mode_stabilizers"]
    kappa_a = float(stabilizers["kappa_a"])
    kappa_phi = float(stabilizers["kappa_phi"])

    points: dict[str, Any] = {}
    model_cache: dict[str, tuple[Any, M5NumericModel]] = {}
    all_nominal_fine = True
    maximum_residual = 0.0
    minimum_hessian_gap = math.inf
    maximum_lambda0_start_distance = 0.0

    for target in manifest["scope"]["targets_in_order"]:
        label = str(target["label"])
        delta_a = float(target["delta_a"])
        delta_phi = float(target["delta_phi"])
        progress(f"{label}: build m4/m5 action evaluators and continue fine/coarse paths")
        model4 = phase41.numeric_model(delta_a, delta_phi)
        model5 = m5_numeric_model(delta_a, delta_phi)
        model_cache[label] = (model4, model5)
        start = embedded_m4_root(
            phase41, checkpoint, label, delta_a, delta_phi, embedding
        )
        fine = continue_path(
            phase41,
            model4,
            model5,
            start,
            fine_mesh,
            delta_a,
            delta_phi,
            kappa_a,
            kappa_phi,
            embedding,
            solver_spec,
            thresholds,
        )
        coarse = continue_path(
            phase41,
            model4,
            model5,
            start,
            coarse_mesh,
            delta_a,
            delta_phi,
            kappa_a,
            kappa_phi,
            embedding,
            solver_spec,
            thresholds,
        )
        reverse_start = np.asarray(fine["endpoint"], dtype=float)
        reverse = continue_path(
            phase41,
            model4,
            model5,
            reverse_start,
            list(reversed(fine_mesh)),
            delta_a,
            delta_phi,
            kappa_a,
            kappa_phi,
            embedding,
            solver_spec,
            thresholds,
        )
        lambda0_start_distance = float(
            np.linalg.norm(np.asarray(fine["records"][0]["w5"]) - start)
        )
        maximum_lambda0_start_distance = max(
            maximum_lambda0_start_distance, lambda0_start_distance
        )
        fine_passed = bool(
            path_passed(fine, thresholds)
            and lambda0_start_distance
            <= float(thresholds["coarse_fine_common_node_distance_max"])
        )
        all_nominal_fine = all_nominal_fine and fine_passed
        for record in fine["records"]:
            maximum_residual = max(maximum_residual, float(record["gradient_max_abs"]))
            minimum_hessian_gap = min(
                minimum_hessian_gap,
                float(record["hessian_min_abs_eigenvalue"]),
            )
        fine_by_lambda = path_map(fine)
        coarse_by_lambda = path_map(coarse)
        reverse_by_lambda = path_map(reverse)
        common_distances = {
            f"lambda={lambda_value:.4f}": float(
                np.linalg.norm(
                    np.asarray(fine_by_lambda[round(lambda_value, 12)]["w5"])
                    - np.asarray(coarse_by_lambda[round(lambda_value, 12)]["w5"])
                )
            )
            for lambda_value in coarse_mesh
            if round(lambda_value, 12) in fine_by_lambda
            and round(lambda_value, 12) in coarse_by_lambda
        }
        reverse_distances = {
            f"lambda={lambda_value:.4f}": float(
                np.linalg.norm(
                    np.asarray(fine_by_lambda[round(lambda_value, 12)]["w5"])
                    - np.asarray(reverse_by_lambda[round(lambda_value, 12)]["w5"])
                )
            )
            for lambda_value in fine_mesh
            if round(lambda_value, 12) in fine_by_lambda
            and round(lambda_value, 12) in reverse_by_lambda
        }
        tangent = (
            tangent_controls(
                phase41,
                model4,
                model5,
                fine,
                delta_a,
                delta_phi,
                kappa_a,
                kappa_phi,
                embedding,
                solver_spec,
                numerics,
                thresholds,
            )
            if fine_passed
            else {"records": [], "all_passed": False}
        )
        points[label] = {
            "source_point": [delta_a, delta_phi],
            "embedded_m4_start": start,
            "nominal": {
                "fine_forward": fine,
                "coarse_forward": coarse,
                "fine_reverse": reverse,
                "fine_passed": fine_passed,
                "lambda0_embedded_start_distance": lambda0_start_distance,
                "coarse_passed": path_passed(coarse, thresholds),
                "reverse_passed": path_passed(reverse, thresholds),
                "coarse_fine_common_node_distances": common_distances,
                "forward_reverse_node_distances": reverse_distances,
            },
            "implicit_tangent_controls": tangent,
        }

    audit.numerical(
        "P50.saddles.five_forward_fine_paths",
        all_nominal_fine,
        "all five frozen source-labelled branches complete the 17-node stabilized m4-to-m5 saddle path with the required residual, gap, norm, and inertia",
        failure_status="M4_M5_LOCAL_SADDLE_METRIC_HOMOTOPY_INCONCLUSIVE",
        details={
            "completed_branches": sum(
                bool(point["nominal"]["fine_passed"]) for point in points.values()
            ),
            "required_branches": 5,
            "maximum_gradient_max_abs": maximum_residual,
            "minimum_hessian_absolute_eigenvalue": minimum_hessian_gap,
            "maximum_lambda0_embedded_start_distance": maximum_lambda0_start_distance,
        },
    )

    max_mesh_distance = max(
        max(point["nominal"]["coarse_fine_common_node_distances"].values(), default=math.inf)
        for point in points.values()
    )
    max_reverse_distance = max(
        max(point["nominal"]["forward_reverse_node_distances"].values(), default=math.inf)
        for point in points.values()
    )
    reverse_mesh_passed = bool(
        all(
            point["nominal"]["coarse_passed"]
            and point["nominal"]["reverse_passed"]
            for point in points.values()
        )
        and max_mesh_distance
        <= float(thresholds["coarse_fine_common_node_distance_max"])
        and max_reverse_distance
        <= float(thresholds["forward_reverse_endpoint_distance_max"])
    )
    audit.numerical(
        "P50.saddles.reverse_and_mesh_controls",
        reverse_mesh_passed,
        "the coarse and fine meshes select the same sampled branches and fine reverse continuation returns to every forward node",
        failure_status="M4_M5_LOCAL_SADDLE_METRIC_HOMOTOPY_INCONCLUSIVE",
        details={
            "maximum_coarse_fine_common_node_distance": max_mesh_distance,
            "maximum_forward_reverse_node_distance": max_reverse_distance,
        },
    )

    reflection_records: list[dict[str, Any]] = []
    reflection_pairs = (("phi_minus", "phi_plus"), ("a_minus", "a_plus"))
    reflection_passed = True
    for minus_label, plus_label in reflection_pairs:
        minus = path_map(points[minus_label]["nominal"]["fine_forward"])
        plus = path_map(points[plus_label]["nominal"]["fine_forward"])
        pair_root_max = 0.0
        pair_action_max = 0.0
        per_node: list[dict[str, Any]] = []
        for lambda_value in fine_mesh:
            key = round(lambda_value, 12)
            left = minus[key]
            right = plus[key]
            root_distance = float(
                np.linalg.norm(
                    np.asarray(left["w5"])
                    - embedding.reflection_m5 @ np.asarray(right["w5"])
                )
            )
            action_distance = float(abs(complex(left["action"]) - complex(right["action"])))
            pair_root_max = max(pair_root_max, root_distance)
            pair_action_max = max(pair_action_max, action_distance)
            per_node.append(
                {
                    "lambda": lambda_value,
                    "root_distance": root_distance,
                    "action_absolute_difference": action_distance,
                }
            )
        passed = bool(
            pair_root_max <= float(thresholds["source_reflection_root_distance_max"])
            and pair_action_max
            <= float(thresholds["source_reflection_action_absolute_max"])
        )
        reflection_passed = reflection_passed and passed
        reflection_records.append(
            {
                "minus": minus_label,
                "plus": plus_label,
                "maximum_root_distance": pair_root_max,
                "maximum_action_absolute_difference": pair_action_max,
                "records": per_node,
                "passed": passed,
            }
        )
    zero_nodes = path_map(points["shared_zero"]["nominal"]["fine_forward"])
    zero_reflection_max = max(
        float(
            np.linalg.norm(
                np.asarray(record["w5"])
                - embedding.reflection_m5 @ np.asarray(record["w5"])
            )
        )
        for record in zero_nodes.values()
    )
    reflection_passed = bool(
        reflection_passed
        and zero_reflection_max
        <= float(thresholds["source_reflection_root_distance_max"])
    )
    audit.numerical(
        "P50.reflection.five_branch_covariance",
        reflection_passed,
        "the shared branch is reflection fixed and both signed source pairs remain reflected roots with equal actions at every fine node",
        failure_status="M4_M5_LOCAL_SADDLE_METRIC_HOMOTOPY_INCONCLUSIVE",
        details={
            "shared_zero_maximum_root_distance": zero_reflection_max,
            "pairs": reflection_records,
        },
    )

    tangent_passed = all(
        point["implicit_tangent_controls"]["all_passed"]
        for point in points.values()
    )
    tangent_relatives = [
        step["implicit_symmetric_relative"]
        for point in points.values()
        for sample in point["implicit_tangent_controls"]["records"]
        for step in sample["steps"]
    ]
    tangent_plateaus = [
        sample["adjacent_step_symmetric_relative"]
        for point in points.values()
        for sample in point["implicit_tangent_controls"]["records"]
    ]
    audit.numerical(
        "P50.tangent.implicit_vs_two_step_fd",
        tangent_passed,
        "the implicit saddle-path tangent agrees with both retained central-difference steps at three lambda values on every branch",
        failure_status="M4_M5_LOCAL_SADDLE_METRIC_HOMOTOPY_INCONCLUSIVE",
        details={
            "retained_columns": len(tangent_relatives),
            "maximum_implicit_symmetric_relative": max(tangent_relatives, default=math.inf),
            "maximum_adjacent_step_symmetric_relative": max(tangent_plateaus, default=math.inf),
        },
    )

    progress("build shared zero-source endpoint mobilities and two SPD paths")
    phase42_mobility = np.asarray(
        checkpoint["fixed_metric"]["inverse_metric_mobility_w"]["values"],
        dtype=float,
    )
    if phase42_mobility.shape != (M4_DIMENSION, M4_DIMENSION):
        raise InvalidRun("Phase42 fixed mobility shape drift")
    mobility_c = np.zeros((M5_DIMENSION, M5_DIMENSION), dtype=float)
    mobility_c[:M4_DIMENSION, :M4_DIMENSION] = phase42_mobility
    mobility_c[7, 7] = 1.0 / abs(kappa_a)
    mobility_c[8, 8] = 1.0 / abs(kappa_phi)
    mobility0 = embedding.basis @ mobility_c @ embedding.basis.T
    shared_lookup = prepare_node_lookup(
        phase41,
        model_cache["shared_zero"][0],
        model_cache["shared_zero"][1],
        points["shared_zero"]["nominal"]["fine_forward"],
        0.0,
        0.0,
        kappa_a,
        kappa_phi,
        embedding,
    )
    shared_endpoint_hessian = shared_lookup[1.0]["hessian_matrix"]
    shared_endpoint_hessian_values = np.linalg.eigvalsh(shared_endpoint_hessian)
    native_mobility1_available = bool(
        shared_lookup[1.0]["accepted"]
        and inertia_record(shared_endpoint_hessian_values)
        == thresholds["required_hessian_inertia"]
        and np.min(np.abs(shared_endpoint_hessian_values)) > 1.0e-12
    )
    mobility1 = (
        natural_mobility(shared_endpoint_hessian)
        if native_mobility1_available
        else mobility0.copy()
    )
    metric_records: dict[str, list[dict[str, Any]]] = {"geodesic": [], "affine": []}
    metric_passed = native_mobility1_available
    metric_audit_mu_values = sorted(set(mu_mesh + fine_mesh))
    for name, function in (
        ("geodesic", geodesic_mobility),
        ("affine", affine_mobility),
    ):
        for mu in metric_audit_mu_values:
            mobility = function(mobility0, mobility1, mu)
            values = np.linalg.eigvalsh(mobility)
            reflection_error = float(
                np.linalg.norm(
                    embedding.reflection_m5 @ mobility @ embedding.reflection_m5
                    - mobility,
                    ord=2,
                )
                / max(np.linalg.norm(mobility, ord=2), 1.0e-300)
            )
            condition = float(np.linalg.cond(mobility))
            passed = bool(
                np.min(values) >= float(thresholds["metric_min_eigenvalue"])
                and condition <= float(thresholds["metric_condition_number_max"])
                and reflection_error
                <= float(thresholds["metric_reflection_relative_error_max"])
            )
            metric_passed = metric_passed and passed
            metric_records[name].append(
                {
                    "mu": mu,
                    "minimum_eigenvalue": float(np.min(values)),
                    "maximum_eigenvalue": float(np.max(values)),
                    "condition_number": condition,
                    "reflection_relative_error": reflection_error,
                    "passed": passed,
                }
            )
    audit.numerical(
        "P50.metric.two_spd_paths",
        metric_passed,
        "the affine-invariant geodesic and affine mutation remain positive, conditioned, and reflection covariant on the frozen metric mesh",
        failure_status="M4_M5_LOCAL_SADDLE_METRIC_HOMOTOPY_INCONCLUSIVE",
        details={
            "mobility0": mobility0,
            "mobility1": mobility1,
            "native_mobility1_available": native_mobility1_available,
            "paths": metric_records,
        },
    )

    progress("transport local upward planes over action-first, metric-first, and diagonal paths")
    action_then_metric = [(value, 0.0) for value in fine_mesh] + [
        (1.0, value) for value in mu_mesh[1:]
    ]
    metric_then_action = [(0.0, value) for value in mu_mesh] + [
        (value, 1.0) for value in fine_mesh[1:]
    ]
    diagonal = [(value, value) for value in fine_mesh]
    coordinate_paths = {
        "action_then_metric": action_then_metric,
        "metric_then_action": metric_then_action,
        "diagonal": diagonal,
    }
    orientation_payload: dict[str, Any] = {}
    orientation_passed = True
    all_consecutive_overlaps: list[float] = []
    all_primary_mutation_overlaps: list[float] = []
    all_endpoint_overlaps: list[float] = []
    all_endpoint_signs: list[int] = []
    for target in manifest["scope"]["targets_in_order"]:
        label = str(target["label"])
        delta_a = float(target["delta_a"])
        delta_phi = float(target["delta_phi"])
        model4, model5 = model_cache[label]
        lookup = prepare_node_lookup(
            phase41,
            model4,
            model5,
            points[label]["nominal"]["fine_forward"],
            delta_a,
            delta_phi,
            kappa_a,
            kappa_phi,
            embedding,
        )
        target_payload: dict[str, Any] = {"geodesic": {}, "affine": {}}
        for metric_name, metric_function in (
            ("geodesic", geodesic_mobility),
            ("affine", affine_mobility),
        ):
            function = lambda mu, fn=metric_function: fn(mobility0, mobility1, mu)
            transports = {
                name: transport_upward_path(path, lookup, function)
                for name, path in coordinate_paths.items()
            }
            transport_ready = all(
                bool(transport["completed"]) for transport in transports.values()
            )
            comparisons = (
                {
                    "action_then_metric_vs_metric_then_action": frame_comparison(
                        transports["action_then_metric"]["endpoint_frame"],
                        transports["metric_then_action"]["endpoint_frame"],
                    ),
                    "action_then_metric_vs_diagonal": frame_comparison(
                        transports["action_then_metric"]["endpoint_frame"],
                        transports["diagonal"]["endpoint_frame"],
                    ),
                    "metric_then_action_vs_diagonal": frame_comparison(
                        transports["metric_then_action"]["endpoint_frame"],
                        transports["diagonal"]["endpoint_frame"],
                    ),
                }
                if transport_ready
                else {
                    "action_then_metric_vs_metric_then_action": unavailable_frame_comparison(
                        "one or both transport paths did not complete"
                    ),
                    "action_then_metric_vs_diagonal": unavailable_frame_comparison(
                        "one or both transport paths did not complete"
                    ),
                    "metric_then_action_vs_diagonal": unavailable_frame_comparison(
                        "one or both transport paths did not complete"
                    ),
                }
            )
            all_consecutive_overlaps.extend(
                float(value["minimum_consecutive_principal_overlap"])
                for value in transports.values()
            )
            all_endpoint_overlaps.extend(
                float(value["minimum_principal_overlap"])
                for value in comparisons.values()
            )
            all_endpoint_signs.extend(
                int(value["orientation_sign"]) for value in comparisons.values()
            )
            target_payload[metric_name] = {
                "paths": transports,
                "endpoint_comparisons": comparisons,
            }
        for path_name in coordinate_paths:
            primary_path = target_payload["geodesic"]["paths"][path_name]
            mutation_path = target_payload["affine"]["paths"][path_name]
            comparison = (
                frame_comparison(
                    primary_path["endpoint_frame"],
                    mutation_path["endpoint_frame"],
                )
                if primary_path["completed"] and mutation_path["completed"]
                else unavailable_frame_comparison(
                    "primary or mutation metric transport did not complete"
                )
            )
            all_primary_mutation_overlaps.append(
                float(comparison["minimum_principal_overlap"])
            )
            all_endpoint_signs.append(int(comparison["orientation_sign"]))
            target_payload.setdefault("primary_mutation_endpoint_comparisons", {})[
                path_name
            ] = comparison
        orientation_payload[label] = target_payload
    orientation_passed = bool(
        all_nominal_fine
        and metric_passed
        and min(all_consecutive_overlaps, default=0.0)
        >= float(thresholds["consecutive_upward_plane_min_principal_overlap"])
        and min(all_primary_mutation_overlaps, default=0.0)
        >= float(thresholds["primary_to_mutation_upward_plane_min_principal_overlap"])
        and min(all_endpoint_overlaps, default=0.0)
        >= float(thresholds["transport_path_endpoint_upward_plane_min_principal_overlap"])
        and all(sign == 1 for sign in all_endpoint_signs)
    )
    audit.numerical(
        "P50.orientation.three_path_upward_plane_transport",
        orientation_passed,
        "the local nine-plane transports continuously and returns with the same oriented endpoint over action-first, metric-first, and diagonal paths for both metric choices",
        failure_status="M4_M5_LOCAL_SADDLE_METRIC_HOMOTOPY_INCONCLUSIVE",
        details={
            "minimum_consecutive_principal_overlap": min(
                all_consecutive_overlaps, default=0.0
            ),
            "minimum_geodesic_affine_endpoint_principal_overlap": min(
                all_primary_mutation_overlaps, default=0.0
            ),
            "minimum_path_endpoint_principal_overlap": min(
                all_endpoint_overlaps, default=0.0
            ),
            "all_endpoint_orientation_signs": all_endpoint_signs,
        },
    )

    progress("run half/double stabilizer and added-basis gauge mutations")
    mutation_payload: dict[str, Any] = {}
    mutation_passed = True
    maximum_mutation_endpoint_distance = 0.0
    maximum_mutation_reverse_distance = 0.0
    for scale in manifest["action_homotopy"]["stabilizer_scale_mutations_in_order"]:
        scale_value = float(scale)
        scale_payload: dict[str, Any] = {}
        for target in manifest["scope"]["targets_in_order"]:
            label = str(target["label"])
            delta_a = float(target["delta_a"])
            delta_phi = float(target["delta_phi"])
            model4, model5 = model_cache[label]
            start = np.asarray(points[label]["embedded_m4_start"], dtype=float)
            forward = continue_path(
                phase41,
                model4,
                model5,
                start,
                fine_mesh,
                delta_a,
                delta_phi,
                scale_value * kappa_a,
                scale_value * kappa_phi,
                embedding,
                solver_spec,
                thresholds,
            )
            reverse = continue_path(
                phase41,
                model4,
                model5,
                np.asarray(forward["endpoint"], dtype=float),
                list(reversed(fine_mesh)),
                delta_a,
                delta_phi,
                scale_value * kappa_a,
                scale_value * kappa_phi,
                embedding,
                solver_spec,
                thresholds,
            )
            nominal_endpoint = np.asarray(
                points[label]["nominal"]["fine_forward"]["endpoint"], dtype=float
            )
            endpoint_distance = float(
                np.linalg.norm(np.asarray(forward["endpoint"]) - nominal_endpoint)
            )
            reverse_distance = float(
                np.linalg.norm(np.asarray(reverse["endpoint"]) - start)
            )
            target_passed = bool(
                path_passed(forward, thresholds)
                and path_passed(reverse, thresholds)
                and endpoint_distance
                <= float(thresholds["stabilizer_mutation_endpoint_distance_max"])
                and reverse_distance
                <= float(thresholds["forward_reverse_endpoint_distance_max"])
            )
            mutation_passed = mutation_passed and target_passed
            maximum_mutation_endpoint_distance = max(
                maximum_mutation_endpoint_distance, endpoint_distance
            )
            maximum_mutation_reverse_distance = max(
                maximum_mutation_reverse_distance, reverse_distance
            )
            scale_payload[label] = {
                "forward": forward,
                "reverse": reverse,
                "nominal_m5_endpoint_distance": endpoint_distance,
                "reverse_m4_endpoint_distance": reverse_distance,
                "passed": target_passed,
            }
        mutation_payload[f"scale={scale_value:g}"] = scale_payload

    basis_flip = np.eye(M5_DIMENSION)
    basis_flip[7, 7] = -1.0
    mutated_basis = embedding.basis @ basis_flip
    mutated_inverse = np.linalg.inv(mutated_basis)
    gauge_action_max = 0.0
    gauge_gradient_max = 0.0
    gauge_hessian_max = 0.0
    for target in manifest["scope"]["targets_in_order"]:
        label = str(target["label"])
        delta_a = float(target["delta_a"])
        delta_phi = float(target["delta_phi"])
        model4, _model5 = model_cache[label]
        for record in (
            points[label]["nominal"]["fine_forward"]["records"][0],
            points[label]["nominal"]["fine_forward"]["records"][-1],
        ):
            w = np.asarray(record["w5"], dtype=float)
            primary = lifted_evaluate(
                phase41,
                model4,
                w,
                delta_a,
                delta_phi,
                kappa_a,
                kappa_phi,
                embedding,
            )
            mutated = lifted_evaluate(
                phase41,
                model4,
                w,
                delta_a,
                delta_phi,
                kappa_a,
                kappa_phi,
                embedding,
                basis=mutated_basis,
                inverse_basis=mutated_inverse,
            )
            gauge_action_max = max(gauge_action_max, float(abs(primary[0] - mutated[0])))
            gauge_gradient_max = max(
                gauge_gradient_max, float(np.max(np.abs(primary[1] - mutated[1])))
            )
            gauge_hessian_max = max(
                gauge_hessian_max, float(np.max(np.abs(primary[2] - mutated[2])))
            )
    m4_oriented_frame = np.asarray(
        checkpoint["fixed_metric"]["oriented_eigenvectors_zero"]["values"],
        dtype=float,
    )
    if m4_oriented_frame.shape != (M4_DIMENSION, M4_DIMENSION):
        raise InvalidRun("Phase42 oriented eigenframe shape drift")
    augmented_coordinate_frame = np.eye(M5_DIMENSION)
    augmented_coordinate_frame[:M4_DIMENSION, :M4_DIMENSION] = m4_oriented_frame
    raw_augmented_matrix = embedding.basis @ augmented_coordinate_frame
    mutated_raw_augmented_matrix = mutated_basis @ augmented_coordinate_frame
    raw_determinant = float(np.linalg.det(raw_augmented_matrix))
    mutated_raw_determinant = float(np.linalg.det(mutated_raw_augmented_matrix))
    correction_determinant = float(np.linalg.det(embedding.inverse_basis))
    mutated_correction_determinant = float(np.linalg.det(mutated_inverse))
    raw_sign = int(np.sign(raw_determinant))
    mutated_raw_sign = int(np.sign(mutated_raw_determinant))
    correction_sign = int(np.sign(correction_determinant))
    mutated_correction_sign = int(np.sign(mutated_correction_determinant))
    corrected_sign = raw_sign * correction_sign
    mutated_corrected_sign = mutated_raw_sign * mutated_correction_sign
    basis_gauge_passed = bool(
        raw_sign == 1
        and mutated_raw_sign == -1
        and corrected_sign == mutated_corrected_sign == 1
        and gauge_action_max <= 1.0e-10
        and gauge_gradient_max <= 1.0e-8
        and gauge_hessian_max <= 1.0e-8
    )
    shared_start = np.asarray(points["shared_zero"]["embedded_m4_start"], dtype=float)
    shared_m5_hessian_at_embedded_root = m5_hessian(
        model_cache["shared_zero"][1], shared_start
    ).real
    complement_hessian = (
        embedding.basis[:, 7:9].T
        @ shared_m5_hessian_at_embedded_root
        @ embedding.basis[:, 7:9]
    )
    complement_eigenvalues = np.linalg.eigvalsh(
        0.5 * (complement_hessian + complement_hessian.T)
    )
    complement_inertia = inertia_record(complement_eigenvalues)
    complement_signs_passed = complement_inertia == {
        "negative": 1,
        "positive": 1,
        "zero": 0,
    }
    mutation_passed = mutation_passed and basis_gauge_passed
    audit.numerical(
        "P50.mutation.stabilizer_and_added_basis_controls",
        mutation_passed,
        "half/double added-mode stabilizers retain the same sampled m5 endpoints and inertia, while one added-basis flip changes only the raw coordinate sign",
        failure_status="M4_M5_LOCAL_SADDLE_METRIC_HOMOTOPY_INCONCLUSIVE",
        details={
            "maximum_mutation_m5_endpoint_distance": maximum_mutation_endpoint_distance,
            "maximum_mutation_reverse_m4_endpoint_distance": maximum_mutation_reverse_distance,
            "basis_gauge": {
                "primary_raw_sign": raw_sign,
                "mutated_raw_sign": mutated_raw_sign,
                "primary_raw_augmented_determinant": raw_determinant,
                "mutated_raw_augmented_determinant": mutated_raw_determinant,
                "primary_inverse_transition_sign": correction_sign,
                "mutated_inverse_transition_sign": mutated_correction_sign,
                "primary_inverse_transition_determinant": correction_determinant,
                "mutated_inverse_transition_determinant": mutated_correction_determinant,
                "primary_corrected_sign": corrected_sign,
                "mutated_corrected_sign": mutated_corrected_sign,
                "maximum_action_absolute_difference": gauge_action_max,
                "maximum_gradient_absolute_difference": gauge_gradient_max,
                "maximum_hessian_absolute_difference": gauge_hessian_max,
                "passed": basis_gauge_passed,
            },
            "m5_complement_at_embedded_m4_zero_root": {
                "hessian": complement_hessian,
                "eigenvalues": complement_eigenvalues,
                "inertia": complement_inertia,
                "one_negative_one_positive": complement_signs_passed,
                "classification_role": "DESCRIPTIVE_ONLY_NOT_A_FROZEN_PASS_CRITERION",
            },
        },
    )

    audit.numerical(
        "P50.guard.no_global_promotion",
        True,
        "all global, physical-cycle, cutoff-limit, and continuum outputs remain null and Gate 1 remains open",
        failure_status="INVALID_RUN",
        details=dict(manifest["required_outputs"]),
    )

    if len(audit.exact_records) != 6 or len(audit.numerical_records) != 8:
        raise InvalidRun("Phase50 retained check-count mismatch")
    all_numerical_passed = all(
        bool(record["passed"]) for record in audit.numerical_records
    )
    reproduced_degeneracy_records: list[dict[str, Any]] = []
    required_inertia = thresholds["required_hessian_inertia"]

    def event_type(record: Mapping[str, Any] | None) -> str | None:
        if record is None or not bool(record.get("finite", False)):
            return None
        if not bool(record.get("accepted", False)):
            # Repeating a rejected root with the same floating-point solver is
            # not an independent no-branch certificate.  Such cases remain
            # inconclusive unless a separately validated branch-loss test is
            # added in a future manifest.
            return None
        if record.get("hessian_inertia") != required_inertia:
            return "inertia_change"
        return None

    for target in manifest["scope"]["targets_in_order"]:
        label = str(target["label"])
        nominal = path_map(points[label]["nominal"]["fine_forward"])
        reverse = path_map(points[label]["nominal"]["fine_reverse"])
        coarse = path_map(points[label]["nominal"]["coarse_forward"])
        for key, record in nominal.items():
            nominal_event = event_type(record)
            if nominal_event is None:
                continue
            reverse_record = reverse.get(key)
            coarse_record = coarse.get(key)
            reverse_event = event_type(reverse_record)
            coarse_event = event_type(coarse_record)
            mutation_events: list[dict[str, Any]] = []
            for scale_label, scale_payload in mutation_payload.items():
                mutation_record = path_map(
                    scale_payload[label]["forward"]
                ).get(key)
                mutation_event = event_type(mutation_record)
                if mutation_event == nominal_event:
                    mutation_events.append(
                        {"scale": scale_label, "event": mutation_event}
                    )
            control_reproduces = bool(
                reverse_event == nominal_event or mutation_events
            )
            if coarse_event == nominal_event and control_reproduces:
                reproduced_degeneracy_records.append(
                    {
                        "label": label,
                        "lambda": float(key),
                        "event": nominal_event,
                        "nominal_inertia": record.get("hessian_inertia"),
                        "reverse_event": reverse_event,
                        "coarse_event": coarse_event,
                        "stabilizer_mutation_events": mutation_events,
                    }
                )
    reproduced_degeneracy = bool(reproduced_degeneracy_records)
    if all_numerical_passed:
        classification = manifest["classification"]["supported_label"]
    elif reproduced_degeneracy:
        classification = manifest["classification"]["contradicted_label"]
    else:
        classification = manifest["classification"]["inconclusive_label"]

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "phase": 50,
        "run_status": "VALID_RUN",
        "classification": classification,
        "input_provenance": {
            "manifest_path": str(INPUT_PATH.relative_to(REPO_ROOT)),
            "manifest_commit": INPUT_COMMIT,
            "manifest_sha256": INPUT_SHA256,
            "validated_pinned_inputs": validated_inputs,
            "phase42_checkpoint_self_digest": checkpoint[
                "checkpoint_payload_sha256_without_self"
            ],
            "phase49_upstream_classification": phase49["classification"],
            "runner_sha256": sha256_path(SCRIPT_PATH),
        },
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "sympy": sp.__version__,
            "mpmath": mpmath.__version__,
        },
        "exact_checks": audit.exact_records,
        "numerical_checks": audit.numerical_records,
        "embedding_and_exact_controls": exact_payload,
        "points": points,
        "reflection_controls": reflection_records,
        "shared_metric_paths": {
            "mobility0": mobility0,
            "mobility1": mobility1,
            "records": metric_records,
        },
        "upward_plane_transport": orientation_payload,
        "stabilizer_mutations": mutation_payload,
        "aggregate_metrics": {
            "fine_branch_count": 5,
            "fine_lambda_nodes_per_branch": len(fine_mesh),
            "maximum_gradient_max_abs": maximum_residual,
            "maximum_lambda0_embedded_start_distance": maximum_lambda0_start_distance,
            "minimum_hessian_absolute_eigenvalue": minimum_hessian_gap,
            "maximum_coarse_fine_common_node_distance": max_mesh_distance,
            "maximum_forward_reverse_node_distance": max_reverse_distance,
            "maximum_tangent_symmetric_relative": max(tangent_relatives, default=None),
            "maximum_tangent_adjacent_step_relative": max(tangent_plateaus, default=None),
            "minimum_consecutive_upward_plane_principal_overlap": min(
                all_consecutive_overlaps, default=None
            ),
            "minimum_path_endpoint_upward_plane_principal_overlap": min(
                all_endpoint_overlaps, default=None
            ),
            "maximum_stabilizer_mutation_endpoint_distance": maximum_mutation_endpoint_distance,
            "all_exact_checks_passed": all(
                bool(record["passed"]) for record in audit.exact_records
            ),
            "all_numerical_checks_passed": all_numerical_passed,
            "reproduced_hessian_zero_or_branch_loss": reproduced_degeneracy,
            "reproduced_inertia_change_records": reproduced_degeneracy_records,
        },
        "computed_facts_scope": list(manifest["scope"]["computed"]),
        "not_computed": list(manifest["scope"]["not_computed"]),
        "promoted_outputs": {
            "bounded_chain_signed_sum": None,
            "complete_global_signed_intersection_vector": None,
            "global_n_sigma": None,
            "cutoff_limit": None,
            "continuum_limit": None,
            "physical_original_cycle": None,
        },
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "next_calculation": "Continue an actual frozen m=5 Gamma-K local candidate over the now-declared action/metric bridge, then search straight arms, cap reintersections, complete upward components, Stokes data, and relative good ends without treating this sampled local saddle transport as a cutoff theorem.",
    }
    result["result_payload_sha256_without_self"] = hashlib.sha256(
        canonical_bytes(result)
    ).hexdigest()
    return result


def main() -> int:
    try:
        result = run()
    except Exception as error:  # fail closed with one machine-readable record
        failure = {
            "schema": RESULT_SCHEMA,
            "phase": 50,
            "run_status": "INVALID_RUN",
            "error_type": type(error).__name__,
            "error": str(error)[:4096],
            "global_promotion": "PROHIBITED",
            "gate1": "OPEN_PARTIAL_PROGRESS",
        }
        print(RESULT_PREFIX + json.dumps(failure, sort_keys=True, allow_nan=False))
        return 1
    print(
        RESULT_PREFIX
        + json.dumps(
            json_ready(result),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    )
    progress(
        f"completed {sum(r['passed'] for r in result['exact_checks'])}/6 exact "
        f"and {sum(r['passed'] for r in result['numerical_checks'])}/8 numerical checks; "
        f"classification={result['classification']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
