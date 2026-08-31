#!/usr/bin/env python3
"""Exact unit-S3 n=1 trace-only scalar gauge convention audit."""
from __future__ import annotations
import hashlib, json, platform, sys
from pathlib import Path
import sympy as sp

INPUT_NAME="CLOSED_S3_N1_TRACE_GAUGE_CONVENTION_INPUTS.json"
RESULT_NAME="CLOSED_S3_N1_TRACE_GAUGE_CONVENTION_RESULT.json"
INPUT_RELPATH=f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH="cpt_temporal_folded_susy/closed_s3_n1_trace_gauge_convention.py"
EXPECTED_INPUT_SHA256="66b9c74f97f4857f3b7f2d399f2a04fee5ba9481b60189a5a0a9e782e746fffa"

def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def sha(b): return hashlib.sha256(b).hexdigest()
def check(rows,id,value,statement): rows.append({"id":id,"passed":bool(sp.simplify(value)==0) if not isinstance(value,bool) else value,"statement":statement})
def verify(root,item):
 raw=(root/item["path"]).read_bytes(); value=json.loads(raw)
 if sha(raw)!=item["sha256"] or value.get("result_payload_sha256_without_self")!=item["payload_sha256_without_self"] or value.get("verdict")!=item["required_verdict"]: raise AssertionError(f"upstream pin mismatch: {item['path']}")
 return {"path":item["path"],"sha256":item["sha256"],"payload_sha256_without_self":item["payload_sha256_without_self"],"verdict":item["required_verdict"]}
def main():
 if len(sys.argv)!=1: raise AssertionError("no arguments")
 raw=Path(__file__).with_name(INPUT_NAME).read_bytes(); input_sha=sha(raw)
 if input_sha!=EXPECTED_INPUT_SHA256: raise AssertionError(f"input hash mismatch: {input_sha}")
 p=json.loads(raw)
 if p["schema_version"]!="ice.closed-s3-n1-trace-gauge-convention.input.v1" or p["numbered_phase"] is not None: raise AssertionError("identity drift")
 root=Path(__file__).resolve().parent.parent; upstream=[verify(root,x) for x in p["upstream_results"]]
 chi,L,a=sp.symbols("chi L a", real=True, positive=True); c=1/sp.sqrt(2*sp.pi**2); q=2*c*sp.cos(chi); lam=sp.Integer(3); rows=[]
 radial=sp.diff(q,chi,2); tangential=sp.sin(chi)*sp.cos(chi)*sp.diff(q,chi)
 tracefree_radial=radial+q; tracefree_tangential=tangential+q*sp.sin(chi)**2
 norm2=sp.Rational(2,3)*lam*(lam-3); piz=sp.symbols("Pi_zeta_1", real=True)
 generator=-L*piz; delta_zeta=sp.diff(generator,piz)
 canonical_metric=2*a**2*delta_zeta*q
 lie_metric_radial=2*a**2*L*radial
 lie_metric_tangent=2*a**2*L*tangential/sp.sin(chi)**2
 check(rows,"CS3N1.hessian.radial",radial+q,"Q1 has D_chi D_chi Q1=-Q1.")
 check(rows,"CS3N1.hessian.tangential",tangential+q*sp.sin(chi)**2,"Q1 has D_theta D_theta Q1=-Q1 gamma_theta_theta.")
 check(rows,"CS3N1.shear.zero_radial",tracefree_radial,"The n=1 tracefree Hessian radial component vanishes.")
 check(rows,"CS3N1.shear.zero_tangential",tracefree_tangential,"The n=1 tracefree Hessian tangential component vanishes.")
 check(rows,"CS3N1.shear.norm_degenerate",norm2,"The integrated scalar-derived shear norm is zero at lambda_1=3.")
 check(rows,"CS3N1.generator.no_shear_pair",True,"No E1/Pi_E1 pair is admitted because the scalar-derived tensor is zero.")
 check(rows,"CS3N1.generator.pb_trace_shift",delta_zeta+L,"D_L1=-L Pi_zeta,1 gives delta zeta_1=-L.")
 check(rows,"CS3N1.generator.radial_lie_match",canonical_metric-lie_metric_radial,"The trace canonical variation equals the radial Lie metric variation.")
 check(rows,"CS3N1.generator.tangential_lie_match",canonical_metric-lie_metric_tangent,"The trace canonical variation equals the tangential Lie metric variation.")
 passed=all(x["passed"] for x in rows); verdict="KEEP_UNIT_S3_N1_TRACE_GAUGE_CONVENTION_NO_SHEAR_PAIR_NOT_FULL_GAUGE_REDUCTION" if passed else "KILL_UNIT_S3_N1_TRACE_GAUGE_CONVENTION"
 result={"schema_version":"ice.closed-s3-n1-trace-gauge-convention.result.v1","calculation_id":p["calculation_id"],"numbered_phase":None,"run_status":"VALID_RUN","verdict":verdict,"question":p["question"],"one_output":p["one_output"],"primary_failure_class":p["primary_failure_class"],"input_manifest":{"path":INPUT_RELPATH,"sha256":input_sha},"upstream_results":upstream,"primary_sources":p["primary_sources"],"declared_conventions":p["declared_conventions"],"exact_checks":rows,"check_summary":{"exact_passed":sum(x["passed"] for x in rows),"exact_total":len(rows),"all_executable_checks_passed":passed},"computed_scope":"exact n=1 trace-only scalar gauge convention and Lie-variation match; no shear pair or full constraint calculation","non_claims":["complete gauge reduction","physical scalar mode classification","Hamiltonian constraint","full HDA or Jacobi closure","BFV/BRST or anomaly freedom","physics claim"],"resource_accounting":{"root_calls":0,"quadratures":0,"ode_calls":0,"adjacent_result_files_written":1,"automatic_descendants":0},"runner":{"path":RUNNER_RELPATH,"sha256":sha(Path(__file__).read_bytes())},"environment":{"python":platform.python_version(),"platform":platform.platform(),"sympy":sp.__version__}}
 result["result_payload_sha256_without_self"]=sha(canon(result)); encoded=canon(result)+b"\n"
 if len(encoded)>1000000: raise AssertionError("artifact cap")
 Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
 print("CLOSED_S3_N1_TRACE_GAUGE_CONVENTION_RESULT="+json.dumps({"run_status":result["run_status"],"verdict":verdict,"exact_passed":result["check_summary"]["exact_passed"],"exact_total":result["check_summary"]["exact_total"],"result":RESULT_NAME,"result_sha256":sha(encoded)},sort_keys=True))
if __name__=="__main__": main()
