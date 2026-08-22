#!/usr/bin/env python3
"""Phase 47: retained-state source-gradient mixed-arithmetic error budget.

The calculation consumes the thirty-six launch/endpoint states already retained
by Phase 46.  It evaluates a fixed six-stage flow telescope and its eighteen
paired u2 central differences.  It performs no trajectory integration, root
search, retuning, or global-intersection calculation and writes no files.
"""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
import math
import platform
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any, Callable, Mapping, Sequence

sys.dont_write_bytecode = True

import mpmath
import numpy as np
import scipy
import sympy as sp
from mpmath import mp


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent
INPUT_PATH = SCRIPT_PATH.with_name(
    "PHASE47_M4_SOURCE_GRADIENT_FLOW_ERROR_BUDGET_INPUTS.json"
)
PHASE42_INPUT_PATH = SCRIPT_PATH.with_name(
    "PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT_INPUTS.json"
)
PHASE42_CHECKPOINT_PATH = SCRIPT_PATH.with_name(
    "PHASE42_M4_FIXED_ROOT_CHECKPOINT.json"
)
PHASE42_SCRIPT_PATH = SCRIPT_PATH.with_name(
    "phase42_m4_fixed_root_tangent_disentanglement.py"
)
PHASE41_SCRIPT_PATH = SCRIPT_PATH.with_name(
    "phase41_m4_two_source_intersection.py"
)
PHASE43_SCRIPT_PATH = SCRIPT_PATH.with_name(
    "phase43_m4_high_precision_local_rhs_arbitration.py"
)
PHASE44_RESULT_PATH = SCRIPT_PATH.with_name(
    "PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION_RESULT.json"
)
PHASE46_RESULT_PATH = SCRIPT_PATH.with_name(
    "PHASE46_M4_U2_STATE_MAP_FD_AUDIT_RESULT.json"
)

INPUT_COMMIT = "9ad082f1b9edb66421c682545b9a35aa91e4d94c"
INPUT_SHA256 = "a4934e2b5f45297f82921a3df7d131afffa184691551cc3c02bb516c36b9fb6e"
PHASE42_INPUT_SHA256 = (
    "1cc88c489b5240019aaf339b25d0cebac9b4a1560b09cbec9c3079ce2067afb6"
)
RESULT_SCHEMA = "ice-phase47-source-gradient-flow-error-budget/v1"
RESULT_PREFIX = "RESULT_JSON="


class InvalidRun(RuntimeError):
    """A frozen input, retained slot, or arithmetic invariant failed."""


def progress(message: str) -> None:
    print(f"[Phase47] {message}", file=sys.stderr, flush=True)


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
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise InvalidRun(f"duplicate JSON key in {path.name}: {key}")
            result[key] = value
        return result

    try:
        payload = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=unique,
            parse_constant=lambda token: (_ for _ in ()).throw(
                InvalidRun(f"nonfinite JSON token in {path.name}: {token}")
            ),
        )
    except UnicodeDecodeError as exc:
        raise InvalidRun(f"non-UTF-8 JSON input: {path.name}") from exc
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
        raise InvalidRun("attempted to serialize a nonfinite float")
    return value


def canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        json_ready(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def verify_self_digest(
    payload: Mapping[str, Any], key: str, expected: str, *, label: str
) -> str:
    embedded = payload.get(key)
    if embedded != expected:
        raise InvalidRun(f"{label} embedded self digest drift")
    without = dict(payload)
    without.pop(key, None)
    observed = hashlib.sha256(canonical_bytes(without)).hexdigest()
    if observed != expected:
        raise InvalidRun(f"{label} self-excluding digest mismatch")
    return observed


def validate_frozen_inputs(manifest: Mapping[str, Any]) -> dict[str, Any]:
    if sha256_path(INPUT_PATH) != INPUT_SHA256:
        raise InvalidRun("Phase47 input manifest hash drift")
    if manifest.get("schema") != (
        "ice-phase47-source-gradient-flow-error-budget-inputs/v1"
    ):
        raise InvalidRun("Phase47 input schema drift")
    if manifest.get("phase") != 47:
        raise InvalidRun("Phase47 input phase drift")
    scope = manifest["scope"]
    if scope["targets_in_order"] != ["shared_zero", "phi_plus", "a_plus"]:
        raise InvalidRun("Phase47 target order drift")
    if scope["locations_in_order"] != ["launch", "endpoint"]:
        raise InvalidRun("Phase47 location order drift")
    if scope["central_difference_steps_in_order"] != [2.0e-6, 5.0e-7, 1.0e-7]:
        raise InvalidRun("Phase47 step order drift")
    if scope["perturbation_signs_in_order"] != [1, -1]:
        raise InvalidRun("Phase47 sign order drift")
    expected_stages = [
        "S0_exact_decimal_reference_exact_w",
        "S1_source_symbolic_expression_exact_w",
        "S2_source_symbolic_expression_lifted_w64",
        "S3_lifted_gradient64_exact_contraction",
        "S4_lifted_matvec64_exact_outer",
        "S5_lifted_source_flow64",
    ]
    expected_deltas = [
        "D_source_symbolic_semantics",
        "D_state_formation",
        "D_gradient_evaluation",
        "D_contraction",
        "D_outer",
    ]
    if manifest["fixed_telescope"]["stage_ids_in_order"] != expected_stages:
        raise InvalidRun("Phase47 stage order drift")
    if manifest["fixed_telescope"]["delta_ids_in_order"] != expected_deltas:
        raise InvalidRun("Phase47 delta order drift")
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
        }
    return observed


def decode_complex_vector(value: Any, *, label: str) -> np.ndarray:
    if not isinstance(value, Mapping) or value.get("shape") != [7]:
        raise InvalidRun(f"{label}: complex-vector shape drift")
    pairs = value.get("complex128_pairs")
    if not isinstance(pairs, list) or len(pairs) != 7:
        raise InvalidRun(f"{label}: complex-pair count drift")
    real = np.empty(7, dtype=np.float64)
    imag = np.empty(7, dtype=np.float64)
    for index, pair in enumerate(pairs):
        if not isinstance(pair, list) or len(pair) != 2:
            raise InvalidRun(f"{label}: malformed complex pair {index}")
        real[index] = float(pair[0])
        imag[index] = float(pair[1])
    if not np.all(np.isfinite(real)) or not np.all(np.isfinite(imag)):
        raise InvalidRun(f"{label}: nonfinite complex vector")
    output = np.empty(7, dtype=np.complex128)
    output.real = real
    output.imag = imag
    return output


def binary64_payload(value: np.ndarray) -> dict[str, Any]:
    array = np.ascontiguousarray(np.asarray(value, dtype=np.complex128))
    little = np.asarray(array, dtype=np.dtype("<c16"))
    return {
        "shape": list(array.shape),
        "complex128_pairs": [
            [float(item.real), float(item.imag)] for item in array.reshape(-1)
        ],
        "component_hex": [
            [float(item.real).hex(), float(item.imag).hex()]
            for item in array.reshape(-1)
        ],
        "canonical_little_endian_sha256": hashlib.sha256(
            little.tobytes(order="C")
        ).hexdigest(),
    }


def bitwise_equal(left: np.ndarray, right: np.ndarray) -> bool:
    a = np.ascontiguousarray(np.asarray(left, dtype=np.complex128))
    b = np.ascontiguousarray(np.asarray(right, dtype=np.complex128))
    return a.shape == b.shape and a.tobytes(order="C") == b.tobytes(order="C")


def numpy_symmetric_relative(left: np.ndarray, right: np.ndarray) -> float:
    a = np.asarray(left, dtype=np.complex128)
    b = np.asarray(right, dtype=np.complex128)
    denominator = max(
        float(np.linalg.norm(a)), float(np.linalg.norm(b)), 1.0e-300
    )
    return float(np.linalg.norm(a - b) / denominator)


def mp_vector(value: Any, phase43: ModuleType) -> list[mp.mpc]:
    return [mp.mpc(item) for item in phase43.flatten_mp(value, 7)]


def finite_mp_vector(value: Sequence[Any], *, label: str) -> list[mp.mpc]:
    result: list[mp.mpc] = []
    for item in value:
        number = mp.mpc(item)
        if not mp.isfinite(number.real) or not mp.isfinite(number.imag):
            raise InvalidRun(f"nonfinite {label}")
        result.append(number)
    if len(result) != 7:
        raise InvalidRun(f"{label} vector length drift")
    return result


def mp_norm(value: Sequence[Any]) -> mp.mpf:
    return mp.sqrt(mp.fsum(abs(item) ** 2 for item in value))


def mp_max_abs(value: Sequence[Any]) -> mp.mpf:
    return max((abs(item) for item in value), default=mp.mpf("0"))


def mp_relative(left: Sequence[Any], right: Sequence[Any]) -> mp.mpf:
    difference = [left[index] - right[index] for index in range(len(left))]
    denominator = max(mp_norm(left), mp_norm(right), mp.mpf("1e-300"))
    return mp_norm(difference) / denominator


def mp_number_text(value: Any, digits: int) -> str:
    return mp.nstr(mp.mpf(value), n=digits, strip_zeros=False)


def mp_vector_payload(value: Sequence[Any], digits: int) -> list[list[str]]:
    return [
        [mp_number_text(mp.re(item), digits), mp_number_text(mp.im(item), digits)]
        for item in value
    ]


def exact_flow_from_gradient(
    linear_map: mp.matrix, gradient: Sequence[Any]
) -> tuple[list[mp.mpc], list[mp.mpc]]:
    raw_matrix = linear_map.T * mp.matrix(list(gradient))
    raw = [mp.mpc(raw_matrix[index]) for index in range(7)]
    flow = [mp.mpc(-mp.conj(item)) for item in raw]
    return raw, flow


def projected_independent_flow(
    phase43: ModuleType,
    evaluator: Any,
    saddle64: np.ndarray,
    linear64: np.ndarray,
    xi64: np.ndarray,
    dps: int,
) -> np.ndarray:
    with mp.workdps(dps):
        saddle = [phase43.mp_complex_from_binary64(item) for item in saddle64]
        linear = phase43.mp_real_matrix_from_numpy(linear64)
        xi = [phase43.mp_complex_from_binary64(item) for item in xi64]
        flow = phase43.reference_flow(evaluator, saddle, linear, xi)
        output = np.empty(7, dtype=np.complex128)
        output.real = [float(item.real) for item in flow]
        output.imag = [float(item.imag) for item in flow]
    if not np.all(np.isfinite(output)):
        raise InvalidRun(f"nonfinite independent {dps}-dps projection")
    return output


def stage_and_delta_payload(
    stage_ids: Sequence[str],
    delta_ids: Sequence[str],
    stages: Sequence[Sequence[Any]],
    digits: int,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], mp.mpf]:
    if len(stages) != len(stage_ids) or len(delta_ids) + 1 != len(stage_ids):
        raise InvalidRun("stage/delta cardinality drift")
    s0 = list(stages[0])
    total = [stages[-1][index] - s0[index] for index in range(7)]
    total_norm = mp_norm(total)
    stage_payload: dict[str, Any] = {}
    for stage_id, stage in zip(stage_ids, stages):
        difference = [stage[index] - s0[index] for index in range(7)]
        stage_payload[stage_id] = {
            "vector": mp_vector_payload(stage, digits),
            "norm": mp_number_text(mp_norm(stage), digits),
            "to_S0_norm": mp_number_text(mp_norm(difference), digits),
            "to_S0_max_component_absolute": mp_number_text(
                mp_max_abs(difference), digits
            ),
            "to_S0_symmetric_relative": mp_number_text(
                mp_relative(stage, s0), digits
            ),
        }
    delta_payload: dict[str, Any] = {}
    delta_vectors: dict[str, list[mp.mpc]] = {}
    delta_norm_sum = mp.mpf("0")
    for index, delta_id in enumerate(delta_ids):
        vector = [
            stages[index + 1][component] - stages[index][component]
            for component in range(7)
        ]
        delta_vectors[delta_id] = vector
        norm = mp_norm(vector)
        delta_norm_sum += norm
        denominator = max(total_norm, mp.mpf("1e-100"))
        if norm == 0 or total_norm == 0:
            alignment = mp.mpf("0")
        else:
            alignment = mp.re(
                mp.fsum(
                    mp.conj(total[component]) * vector[component]
                    for component in range(7)
                )
            ) / (norm * total_norm)
        delta_payload[delta_id] = {
            "from_stage": stage_ids[index],
            "to_stage": stage_ids[index + 1],
            "vector": mp_vector_payload(vector, digits),
            "norm": mp_number_text(norm, digits),
            "max_component_absolute": mp_number_text(mp_max_abs(vector), digits),
            "norm_over_total_error_norm": mp_number_text(norm / denominator, digits),
            "real_alignment_with_total_error": mp_number_text(alignment, digits),
        }
    reconstructed = [
        mp.fsum(delta_vectors[delta_id][component] for delta_id in delta_ids)
        for component in range(7)
    ]
    residual = [reconstructed[index] - total[index] for index in range(7)]
    telescope = {
        "S_last_minus_S0": mp_vector_payload(total, digits),
        "sum_of_deltas": mp_vector_payload(reconstructed, digits),
        "residual": mp_vector_payload(residual, digits),
        "max_component_absolute": mp_number_text(mp_max_abs(residual), digits),
        "total_error_norm": mp_number_text(total_norm, digits),
        "sum_delta_norms": mp_number_text(delta_norm_sum, digits),
        "cancellation_ratio_sum_delta_norms_over_total": mp_number_text(
            delta_norm_sum / max(total_norm, mp.mpf("1e-100")), digits
        ),
    }
    return stage_payload, delta_payload, telescope, mp_max_abs(residual)


def evaluate_state_slot(
    phase41: ModuleType,
    phase43: ModuleType,
    model: Any,
    evaluator: Any,
    source_symbolic_gradient: Callable[..., Any],
    saddle64: np.ndarray,
    linear64: np.ndarray,
    xi64: np.ndarray,
    stage_ids: Sequence[str],
    delta_ids: Sequence[str],
    authoritative_dps: int,
    probe_dps: Sequence[int],
    digits: int,
) -> tuple[dict[str, Any], list[list[mp.mpc]], dict[str, list[mp.mpc]]]:
    saddle_object = SimpleNamespace(saddle_w=saddle64)
    fixed_object = SimpleNamespace(linear_map=linear64)
    u64 = np.asarray(linear64 @ xi64, dtype=np.complex128).reshape(7)
    w64 = np.asarray(saddle64 + u64, dtype=np.complex128).reshape(7)
    gradient_manual = np.asarray(
        model.gradient_function(tuple(w64)), dtype=np.complex128
    ).reshape(7)
    gradient_call = np.asarray(
        phase41.gradient_at(model, w64), dtype=np.complex128
    ).reshape(7)
    matvec64 = np.asarray(linear64.T @ gradient_manual, dtype=np.complex128).reshape(7)
    flow_manual = np.asarray(-np.conjugate(matvec64), dtype=np.complex128).reshape(7)
    flow_call = np.asarray(
        phase41.flow_xi(model, saddle_object, fixed_object, xi64),
        dtype=np.complex128,
    ).reshape(7)
    gradient_bitwise = bitwise_equal(gradient_manual, gradient_call)
    flow_bitwise = bitwise_equal(flow_manual, flow_call)
    if not np.all(np.isfinite(gradient_manual)) or not np.all(np.isfinite(flow_manual)):
        raise InvalidRun("nonfinite source gradient/flow boundary")

    projected = [
        projected_independent_flow(
            phase43, evaluator, saddle64, linear64, xi64, int(dps)
        )
        for dps in probe_dps
    ]
    precision_relative = numpy_symmetric_relative(projected[0], projected[1])

    with mp.workdps(authoritative_dps):
        saddle = [phase43.mp_complex_from_binary64(item) for item in saddle64]
        linear = phase43.mp_real_matrix_from_numpy(linear64)
        xi = [phase43.mp_complex_from_binary64(item) for item in xi64]
        w_exact_matrix = mp.matrix(saddle) + linear * mp.matrix(xi)
        w_exact = [mp.mpc(w_exact_matrix[index]) for index in range(7)]
        w64_lift = [phase43.mp_complex_from_binary64(item) for item in w64]

        s0 = finite_mp_vector(
            phase43.reference_flow(evaluator, saddle, linear, xi),
            label="S0 independent reference flow",
        )
        source_gradient_exact_w = mp_vector(
            source_symbolic_gradient(tuple(w_exact)), phase43
        )
        _raw1, s1 = exact_flow_from_gradient(linear, source_gradient_exact_w)
        source_gradient_w64 = mp_vector(
            source_symbolic_gradient(tuple(w64_lift)), phase43
        )
        _raw2, s2 = exact_flow_from_gradient(linear, source_gradient_w64)
        gradient64_lift = [
            phase43.mp_complex_from_binary64(item) for item in gradient_manual
        ]
        _raw3, s3 = exact_flow_from_gradient(linear, gradient64_lift)
        matvec64_lift = [
            phase43.mp_complex_from_binary64(item) for item in matvec64
        ]
        s4 = [mp.mpc(-mp.conj(item)) for item in matvec64_lift]
        s5 = [phase43.mp_complex_from_binary64(item) for item in flow_manual]
        stages = [s0, s1, s2, s3, s4, s5]
        stage_payload, delta_payload, telescope, telescope_residual = (
            stage_and_delta_payload(
                stage_ids, delta_ids, stages, digits
            )
        )
        delta_vectors = {
            delta_ids[index]: [
                stages[index + 1][component] - stages[index][component]
                for component in range(7)
            ]
            for index in range(len(delta_ids))
        }
        source_reference_relative = mp_relative(s5, s0)
        source_reference_max_abs = mp_max_abs(
            [s5[index] - s0[index] for index in range(7)]
        )
        source_final_lift_residual = mp_max_abs(
            [
                s5[index] - phase43.mp_complex_from_binary64(flow_call[index])
                for index in range(7)
            ]
        )

    payload = {
        "input_xi": binary64_payload(xi64),
        "source_boundaries": {
            "u64": binary64_payload(u64),
            "w64": binary64_payload(w64),
            "gradient64": binary64_payload(gradient_manual),
            "matvec64": binary64_payload(matvec64),
            "flow64": binary64_payload(flow_manual),
        },
        "source_reproduction": {
            "gradient_at_bitwise": gradient_bitwise,
            "flow_xi_bitwise": flow_bitwise,
            "source_final_lift_max_component_absolute": mp_number_text(
                source_final_lift_residual, digits
            ),
        },
        "independent_precision_probe": {
            "dps_in_order": list(probe_dps),
            "projected_complex128": [binary64_payload(value) for value in projected],
            "symmetric_relative": precision_relative,
        },
        "stages": stage_payload,
        "deltas": delta_payload,
        "telescope": telescope,
        "source_to_reference": {
            "symmetric_relative": mp_number_text(source_reference_relative, digits),
            "max_component_absolute": mp_number_text(
                source_reference_max_abs, digits
            ),
        },
    }
    return payload, stages, delta_vectors


def paired_derivative_payload(
    stage_ids: Sequence[str],
    delta_ids: Sequence[str],
    plus_stages: Sequence[Sequence[Any]],
    minus_stages: Sequence[Sequence[Any]],
    step: float,
    phase43: ModuleType,
    digits: int,
) -> tuple[dict[str, Any], mp.mpf]:
    h = phase43.mp_from_binary64(float(step))
    denominator = mp.mpf(2) * h
    derivative_stages: list[list[mp.mpc]] = []
    for stage_index in range(len(stage_ids)):
        derivative_stages.append(
            [
                (plus_stages[stage_index][component] - minus_stages[stage_index][component])
                / denominator
                for component in range(7)
            ]
        )
    stages, deltas, telescope, residual = stage_and_delta_payload(
        stage_ids, delta_ids, derivative_stages, digits
    )
    plus_error = [
        plus_stages[-1][index] - plus_stages[0][index] for index in range(7)
    ]
    minus_error = [
        minus_stages[-1][index] - minus_stages[0][index] for index in range(7)
    ]
    derivative_error = [
        derivative_stages[-1][index] - derivative_stages[0][index]
        for index in range(7)
    ]
    triangle_bound = (mp_norm(plus_error) + mp_norm(minus_error)) / denominator
    derivative_error_norm = mp_norm(derivative_error)
    payload = {
        "step": step,
        "step_binary64_hex": float(step).hex(),
        "stages_Dh": stages,
        "deltas_Dh": deltas,
        "telescope_Dh": telescope,
        "source_minus_reference_Dh": {
            "vector": mp_vector_payload(derivative_error, digits),
            "norm": mp_number_text(derivative_error_norm, digits),
            "max_component_absolute": mp_number_text(
                mp_max_abs(derivative_error), digits
            ),
            "symmetric_relative_to_independent_Dh": mp_number_text(
                mp_relative(derivative_stages[-1], derivative_stages[0]), digits
            ),
        },
        "signwise_source_error_triangle_bound": {
            "plus_error_norm": mp_number_text(mp_norm(plus_error), digits),
            "minus_error_norm": mp_number_text(mp_norm(minus_error), digits),
            "bound_after_division_by_2h": mp_number_text(triangle_bound, digits),
            "actual_Dh_error_norm": mp_number_text(derivative_error_norm, digits),
            "actual_over_triangle_bound": mp_number_text(
                derivative_error_norm / max(triangle_bound, mp.mpf("1e-100")),
                digits,
            ),
        },
    }
    return payload, residual


def result_with_self_digest(payload: Mapping[str, Any]) -> dict[str, Any]:
    result = dict(payload)
    result["result_payload_sha256_without_self"] = hashlib.sha256(
        canonical_bytes(result)
    ).hexdigest()
    return result


def run() -> dict[str, Any]:
    manifest, _manifest_raw = load_unique_json(INPUT_PATH)
    validated_inputs = validate_frozen_inputs(manifest)
    progress("load pinned Phase 42 context and Phase 43 exact reference")
    phase42 = load_module("ice_phase42_for_phase47", PHASE42_SCRIPT_PATH)
    phase41 = load_module("ice_phase41_for_phase47", PHASE41_SCRIPT_PATH)
    phase43 = load_module("ice_phase43_for_phase47", PHASE43_SCRIPT_PATH)
    phase42_manifest, _ = phase42.read_pinned_json(
        PHASE42_INPUT_PATH,
        PHASE42_INPUT_SHA256,
        label="Phase42 input manifest",
    )
    checkpoint, checkpoint_raw = phase42.read_pinned_json(
        PHASE42_CHECKPOINT_PATH,
        manifest["pinned_inputs"]["phase42_checkpoint"]["sha256"],
        label="Phase42 checkpoint",
    )
    context = phase42.rehydrate_checkpoint(
        phase42_manifest, checkpoint, checkpoint_raw
    )
    phase44_result, _ = load_unique_json(PHASE44_RESULT_PATH)
    phase46_result, _ = load_unique_json(PHASE46_RESULT_PATH)
    if phase44_result.get("run_status") != "VALID_TYPED_RUN":
        raise InvalidRun("Phase44 result status drift")
    phase44_expected_digest = str(
        phase44_result["result_payload_sha256_without_self"]
    )
    verify_self_digest(
        phase44_result,
        "result_payload_sha256_without_self",
        phase44_expected_digest,
        label="Phase44 result",
    )
    formula_state = phase44_result["classification_aggregates"]["global"][
        "formula_mismatch"
    ]["universal_all"]
    required_formula_state = manifest["fixed_metrics_and_thresholds"][
        "phase44_formula_mismatch_required_global_state"
    ]
    if formula_state != required_formula_state:
        raise InvalidRun("Phase44 formula-mismatch state drift")
    del phase44_result
    if phase46_result.get("schema") != "ice-phase46-u2-state-map-fd-audit/v1":
        raise InvalidRun("Phase46 result schema drift")
    if phase46_result.get("run_status") != "VALID_RUN":
        raise InvalidRun("Phase46 result status drift")
    phase46_digest = str(phase46_result["result_payload_sha256_without_self"])
    verify_self_digest(
        phase46_result,
        "result_payload_sha256_without_self",
        phase46_digest,
        label="Phase46 result",
    )

    scope = manifest["scope"]
    stage_ids = list(manifest["fixed_telescope"]["stage_ids_in_order"])
    delta_ids = list(manifest["fixed_telescope"]["delta_ids_in_order"])
    numerics = manifest["fixed_numerics"]
    thresholds = manifest["fixed_metrics_and_thresholds"]
    authoritative_dps = int(numerics["authoritative_mpmath_dps"])
    mp.dps = authoritative_dps
    detectable_stage_floor = mp.mpf(thresholds["detectable_stage_norm_floor"])
    probe_dps = [
        int(value)
        for value in numerics["independent_projection_probe_dps_in_order"]
    ]
    digits = int(numerics["retained_mpmath_digits"])
    steps = [float(value) for value in scope["central_difference_steps_in_order"]]
    signs = [int(value) for value in scope["perturbation_signs_in_order"]]
    locations = [str(value) for value in scope["locations_in_order"]]
    linear64 = np.asarray(context.fixed.linear_map, dtype=np.float64)
    if linear64.shape != (7, 7) or not np.all(np.isfinite(linear64)):
        raise InvalidRun("fixed linear-map shape/finiteness drift")

    all_gradient_bitwise = True
    all_flow_bitwise = True
    all_precision = True
    max_precision_relative = 0.0
    max_telescope_residual = mp.mpf("0")
    max_paired_residual = mp.mpf("0")
    dominant_state_delta_counts: Counter[str] = Counter()
    dominant_paired_delta_counts: Counter[str] = Counter()
    detectable_state_delta_counts: Counter[str] = Counter()
    detectable_paired_delta_counts: Counter[str] = Counter()
    state_stage_norm_max = {delta_id: mp.mpf("0") for delta_id in delta_ids}
    paired_stage_norm_max = {delta_id: mp.mpf("0") for delta_id in delta_ids}
    source_reference_relative_max = mp.mpf("0")
    points: dict[str, Any] = {}
    stage_cache: dict[tuple[str, float, int, str], list[list[mp.mpc]]] = {}

    for label in scope["targets_in_order"]:
        progress(f"{label}: build exact/source gradient evaluators")
        point = context.points[label]
        source_point = [float(value) for value in point.source_point]
        model = phase41.numeric_model(source_point[0], source_point[1])
        evaluator = phase43.make_reference_evaluators(
            format(source_point[0], ".17g"), format(source_point[1], ".17g")
        )
        source_symbolic_gradient = sp.lambdify(
            (phase41.build_symbolic_family().variables_w,),
            model.gradient_expr,
            modules="mpmath",
        )
        saddle64 = np.asarray(point.saddle.saddle_w, dtype=np.complex128).reshape(7)
        point_states = phase46_result["points"][label]["retained_state_maps"][
            scope["state_path"]
        ]
        slot_payloads: dict[str, Any] = {}
        source_expr_sha = hashlib.sha256(
            sp.srepr(model.gradient_expr).encode("utf-8")
        ).hexdigest()
        exact_expr_sha = hashlib.sha256(
            sp.srepr(evaluator.exact_family.gradient).encode("utf-8")
        ).hexdigest()

        for step in steps:
            for sign in signs:
                retained_key = f"h={step:.1e},sign={sign:+d}"
                retained = point_states.get(retained_key)
                if not isinstance(retained, Mapping):
                    raise InvalidRun(f"missing retained Phase46 state: {label}/{retained_key}")
                for location in locations:
                    field = "initial_xi" if location == "launch" else "endpoint_xi"
                    xi64 = decode_complex_vector(
                        retained[field], label=f"{label}/{retained_key}/{field}"
                    )
                    slot_key = f"{retained_key},location={location}"
                    progress(f"{label}: {slot_key}")
                    payload, stages, delta_vectors = evaluate_state_slot(
                        phase41,
                        phase43,
                        model,
                        evaluator,
                        source_symbolic_gradient,
                        saddle64,
                        linear64,
                        xi64,
                        stage_ids,
                        delta_ids,
                        authoritative_dps,
                        probe_dps,
                        digits,
                    )
                    payload["retained_phase46_path"] = (
                        f"$.points.{label}.retained_state_maps."
                        f"{scope['state_path']}.{retained_key}.{field}"
                    )
                    payload["step"] = step
                    payload["sign"] = sign
                    payload["location"] = location
                    slot_payloads[slot_key] = payload
                    stage_cache[(label, step, sign, location)] = stages
                    gradient_pass = payload["source_reproduction"][
                        "gradient_at_bitwise"
                    ]
                    flow_pass = payload["source_reproduction"]["flow_xi_bitwise"]
                    precision = float(
                        payload["independent_precision_probe"]["symmetric_relative"]
                    )
                    residual = mp.mpf(payload["telescope"]["max_component_absolute"])
                    all_gradient_bitwise = all_gradient_bitwise and gradient_pass
                    all_flow_bitwise = all_flow_bitwise and flow_pass
                    all_precision = all_precision and precision <= float(
                        thresholds[
                            "independent_80dps_to_120dps_complex128_relative_max"
                        ]
                    )
                    max_precision_relative = max(max_precision_relative, precision)
                    max_telescope_residual = max(max_telescope_residual, residual)
                    source_reference_relative_max = max(
                        source_reference_relative_max,
                        mp.mpf(payload["source_to_reference"]["symmetric_relative"]),
                    )
                    norms = {
                        delta_id: mp_norm(delta_vectors[delta_id])
                        for delta_id in delta_ids
                    }
                    dominant = max(delta_ids, key=lambda key: norms[key])
                    dominant_state_delta_counts[dominant] += 1
                    for delta_id in delta_ids:
                        if norms[delta_id] > detectable_stage_floor:
                            detectable_state_delta_counts[delta_id] += 1
                        state_stage_norm_max[delta_id] = max(
                            state_stage_norm_max[delta_id], norms[delta_id]
                        )

        paired_payloads: dict[str, Any] = {}
        with mp.workdps(authoritative_dps):
            for location in locations:
                for step in steps:
                    plus = stage_cache[(label, step, 1, location)]
                    minus = stage_cache[(label, step, -1, location)]
                    pair_key = f"h={step:.1e},location={location}"
                    paired, residual = paired_derivative_payload(
                        stage_ids,
                        delta_ids,
                        plus,
                        minus,
                        step,
                        phase43,
                        digits,
                    )
                    paired_payloads[pair_key] = paired
                    max_paired_residual = max(max_paired_residual, residual)
                    norms = {
                        delta_id: mp.mpf(paired["deltas_Dh"][delta_id]["norm"])
                        for delta_id in delta_ids
                    }
                    dominant = max(delta_ids, key=lambda key: norms[key])
                    dominant_paired_delta_counts[dominant] += 1
                    for delta_id in delta_ids:
                        if norms[delta_id] > detectable_stage_floor:
                            detectable_paired_delta_counts[delta_id] += 1
                        paired_stage_norm_max[delta_id] = max(
                            paired_stage_norm_max[delta_id], norms[delta_id]
                        )

        points[label] = {
            "source_point": source_point,
            "saddle_w": binary64_payload(saddle64),
            "symbolic_fingerprints": {
                "source_gradient_srepr_sha256": source_expr_sha,
                "independent_exact_gradient_srepr_sha256": exact_expr_sha,
                "source_generated_callable_sha256": hashlib.sha256(
                    inspect.getsource(model.gradient_function).encode("utf-8")
                ).hexdigest(),
            },
            "state_slots": slot_payloads,
            "paired_Dh_slots": paired_payloads,
        }

    state_slot_count = sum(len(value["state_slots"]) for value in points.values())
    paired_slot_count = sum(len(value["paired_Dh_slots"]) for value in points.values())
    telescope_pass = max_telescope_residual <= mp.mpf(
        thresholds["mp_stage_telescope_max_component_absolute_max"]
    )
    paired_telescope_pass = max_paired_residual <= mp.mpf(
        thresholds["paired_Dh_stage_telescope_max_component_absolute_max"]
    )
    source_lift_zero = all(
        mp.mpf(slot["source_reproduction"]["source_final_lift_max_component_absolute"])
        == 0
        for point in points.values()
        for slot in point["state_slots"].values()
    )
    prerequisites = all(
        (
            state_slot_count == int(scope["state_slot_count"]),
            paired_slot_count == int(scope["paired_derivative_slot_count"]),
            all_gradient_bitwise,
            all_flow_bitwise,
            source_lift_zero,
            all_precision,
            telescope_pass,
            paired_telescope_pass,
            formula_state == required_formula_state,
        )
    )
    classification = manifest["classification"][
        "budget_supported_label" if prerequisites else "inconclusive_label"
    ]
    result = {
        "schema": RESULT_SCHEMA,
        "phase": 47,
        "run_status": "VALID_RUN",
        "classification": classification,
        "aggregate_tests": {
            "all_36_state_slots_complete": state_slot_count
            == int(scope["state_slot_count"]),
            "all_18_paired_Dh_slots_complete": paired_slot_count
            == int(scope["paired_derivative_slot_count"]),
            "all_source_gradients_reproduced_bitwise": all_gradient_bitwise,
            "all_source_flows_reproduced_bitwise": all_flow_bitwise,
            "all_source_final_lifts_exact": source_lift_zero,
            "all_independent_80dps_120dps_projections_pass": all_precision,
            "all_state_telescopes_close": telescope_pass,
            "all_paired_Dh_telescopes_close": paired_telescope_pass,
            "phase44_formula_mismatch_remains_not_supported": formula_state
            == required_formula_state,
        },
        "aggregate_metrics": {
            "state_slot_count": state_slot_count,
            "paired_Dh_slot_count": paired_slot_count,
            "independent_projection_relative_max": max_precision_relative,
            "state_telescope_max_component_absolute_max": mp_number_text(
                max_telescope_residual, digits
            ),
            "paired_Dh_telescope_max_component_absolute_max": mp_number_text(
                max_paired_residual, digits
            ),
            "source_to_reference_symmetric_relative_max": mp_number_text(
                source_reference_relative_max, digits
            ),
            "state_delta_norm_max_by_stage": {
                key: mp_number_text(value, digits)
                for key, value in state_stage_norm_max.items()
            },
            "paired_Dh_delta_norm_max_by_stage": {
                key: mp_number_text(value, digits)
                for key, value in paired_stage_norm_max.items()
            },
            "largest_delta_norm_counts_across_state_slots_descriptive_only": {
                key: int(dominant_state_delta_counts.get(key, 0))
                for key in delta_ids
            },
            "largest_delta_norm_counts_across_paired_Dh_slots_descriptive_only": {
                key: int(dominant_paired_delta_counts.get(key, 0))
                for key in delta_ids
            },
            "detectable_state_delta_counts_above_frozen_floor": {
                key: int(detectable_state_delta_counts.get(key, 0))
                for key in delta_ids
            },
            "detectable_paired_Dh_delta_counts_above_frozen_floor": {
                key: int(detectable_paired_delta_counts.get(key, 0))
                for key in delta_ids
            },
        },
        "thresholds": thresholds,
        "phase44_formula_identity_control": {
            "global_formula_mismatch_universal_state": formula_state,
            "required_state": required_formula_state,
            "phase44_result_self_digest": phase44_expected_digest,
        },
        "points": points,
        "provenance": {
            "input_manifest_commit": INPUT_COMMIT,
            "input_manifest_sha256": INPUT_SHA256,
            "validated_inputs": validated_inputs,
            "phase46_result_self_digest": phase46_digest,
            "runner_sha256": sha256_path(SCRIPT_PATH),
            "runtime": {
                "python": platform.python_version(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
                "sympy": sp.__version__,
                "mpmath": mpmath.__version__,
            },
        },
        "interpretation_boundary": {
            "calculation_workbench_only": True,
            "historical_phase41_phase44_phase46_results_unchanged": True,
            "new_trajectory_integration": "NOT_RUN",
            "intermediate_path_sampling": "NOT_AVAILABLE_IN_PHASE46",
            "endpoint_error_propagation_or_solver_accumulation_bound": None,
            "largest_stage_is_not_a_unique_cause": True,
            "complex_step_authorized": False,
            "global_promotion": "PROHIBITED",
            "gate1": "OPEN_PARTIAL_PROGRESS",
        },
    }
    return result_with_self_digest(result)


def main() -> int:
    try:
        result = run()
        print(RESULT_PREFIX + canonical_bytes(result).decode("utf-8"))
        return 0
    except Exception as exc:
        emergency = result_with_self_digest(
            {
                "schema": RESULT_SCHEMA,
                "phase": 47,
                "run_status": "INVALID_RUN",
                "classification": "SOURCE_GRADIENT_FLOW_ERROR_BUDGET_INCONCLUSIVE",
                "error_type": type(exc).__name__,
                "error": str(exc)[:4096],
                "provenance": {
                    "input_manifest_commit": INPUT_COMMIT,
                    "input_manifest_sha256": INPUT_SHA256,
                    "runner_sha256": sha256_path(SCRIPT_PATH),
                    "runtime": {
                        "python": platform.python_version(),
                        "numpy": np.__version__,
                        "scipy": scipy.__version__,
                        "sympy": sp.__version__,
                        "mpmath": mpmath.__version__,
                    },
                },
            }
        )
        print(RESULT_PREFIX + canonical_bytes(emergency).decode("utf-8"))
        print(f"Phase47 invalid run: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
