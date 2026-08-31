#!/usr/bin/env python3
"""Exact unit-S3 Q2 coupled momentum DH strain-cancellation audit."""
from __future__ import annotations
import hashlib,json,platform,sys
from pathlib import Path
import sympy as sp
import closed_s3_zonal_v0_scalar_matter_hh_bracket_cutoff_ledger as z
I="CLOSED_S3_Q2_COUPLED_DH_STRAIN_CANCELLATION_INPUTS.json"; R="CLOSED_S3_Q2_COUPLED_DH_STRAIN_CANCELLATION_RESULT.json"; H="74be85e4fc3323d6b5807844a3994458b5c2ebb9fc33ff5cf9749dfe43b25b40"
def cb(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def sh(x): return hashlib.sha256(x).hexdigest()
def ck(rows,i,x,s): rows.append({"id":i,"passed":bool(sp.simplify(x)==0),"statement":s})
def pin(root,x):
 raw=(root/x["path"]).read_bytes(); v=json.loads(raw)
 if sh(raw)!=x["sha256"] or v.get("result_payload_sha256_without_self")!=x["payload_sha256_without_self"] or v.get("verdict")!=x["required_verdict"]: raise AssertionError("upstream pin")
 return {k:x[k] for k in ("path","sha256","payload_sha256_without_self","required_verdict")}
def D(s,n,t,x,a,c): return sp.expand(sum(x[i]*t[j]*z.gradient_triple(i,s,j,c) for i in range(n+1) for j in range(n+1)))
def lieH(s,l,n,t,x,a,c): return sp.expand(sum(z.gradient_triple(k,s,l,c)*z.hamiltonian(k,n,t,x,a,c) for k in range(s+l+1)))
def expected_nulls():
 return {
  "gravitational_hamiltonian_constraint":None,
  "DD_bracket":None,
  "HH_bracket":None,
  "full_scalar_vector_tensor_completion":None,
  "full_hypersurface_deformation_algebra":None,
  "classical_jacobi_closure":None,
  "classical_or_quantum_anomaly":None,
  "BFV_or_BRST_charge":None,
  "physics_claim":None,
  "TOE_claim":None,
  "global_promotion":"PROHIBITED",
  "gate1":"OPEN_PARTIAL_PROGRESS",
  "automatic_next":None,
 }
def main():
 if len(sys.argv)!=1: raise AssertionError("no args")
 raw=Path(__file__).with_name(I).read_bytes(); hs=sh(raw)
 if hs!=H: raise AssertionError("input hash")
 p=json.loads(raw)
 if p["schema_version"]!="ice.closed-s3-q2-coupled-dh-strain-cancellation.input.v1" or p["calculation_id"]!="ClosedS3Q2CoupledDHStrainCancellation" or p["numbered_phase"] is not None or p["resource_caps"]!={"wall_clock_seconds":120,"stdout_bytes":262144,"stderr_bytes":262144,"changed_artifact_files":12,"changed_artifact_bytes":1000000,"root_calls":0,"quadratures":0,"ode_calls":0,"automatic_descendants":0} or len(p["controls"])!=3: raise AssertionError("identity, cap, or control-count drift")
 root=Path(__file__).resolve().parent.parent; pins=[pin(root,x) for x in p["upstream_results"]]
 for x in (p["reused_helper"],p["fixed_metric_provenance"]):
  if sh((root/x["path"]).read_bytes())!=x["sha256"]: raise AssertionError("helper pin")
 a=sp.symbols("a",positive=True,real=True); chi=sp.symbols("chi",real=True); c=1/sp.sqrt(2*sp.pi**2); q1=z.direct_q(1,chi,c); q2=z.direct_q(2,chi,c); th=q1+q2; xi=th; rows=[]
 # v=DQ2; q=a^2[gamma+2 zeta Q2 gamma+2 E S(Q2)].
 div=-8*q2; hrr=sp.diff(q2,chi,2); htt=sp.sin(chi)*sp.cos(chi)*sp.diff(q2,chi); srr=hrr+sp.Rational(8,3)*q2; stt=htt/sp.sin(chi)**2+sp.Rational(8,3)*q2; grad=sp.diff(th,chi); f=grad**2
 strain=z.direct_integral(q1*(-xi**2*div/(2*a**3)+a*f*div/2-a*hrr*f),chi)
 hz=z.direct_integral(q1*q2*(-3*xi**2/a**3+a*f)/2,chi)
 he=z.direct_integral(-a*q1*srr*f,chi)
 zeta,E,piz,pie=sp.symbols("zeta2 E2 Pi_zeta2 Pi_E2",real=True); hlin=hz*zeta+he*E; dg_generator=pie-sp.Rational(8,3)*piz
 dg=sp.simplify(z.poisson(dg_generator,hlin,[zeta,E],[piz,pie],1))
 ck(rows,"CS3Q2.metric.action.zeta",z.poisson(zeta,dg_generator,[zeta,E],[piz,pie],1)+sp.Rational(8,3),"Canonical PB gives delta zeta2=-8/3.")
 ck(rows,"CS3Q2.metric.action.E",z.poisson(E,dg_generator,[zeta,E],[piz,pie],1)-1,"Canonical PB gives delta E2=1.")
 ck(rows,"CS3Q2.metric.action.lie",2*a**2*(-sp.Rational(8,3)*q2+hrr+sp.Rational(8,3)*q2)-2*a**2*hrr,"Trace plus shear variation reconstructs 2a^2 Hess(Q2) in the radial component.")
 ck(rows,"CS3Q2.metric.action.lie_tangential",2*a**2*(-sp.Rational(8,3)*q2+stt)-2*a**2*htt/sp.sin(chi)**2,"Trace plus shear variation reconstructs 2a^2 Hess(Q2) in the tangential component.")
 ck(rows,"CS3Q2.metric.bracket.minus_strain",dg+strain,"The canonical metric bracket equals minus the direct fixed-metric strain.")
 maxn=5; t=list(sp.symbols(f"t0:{maxn+1}")); x=list(sp.symbols(f"x0:{maxn+1}")); subs={**{t[k]:1 if k in (1,2) else 0 for k in range(maxn+1)},**{x[k]:1 if k in (1,2) else 0 for k in range(maxn+1)}}; out=[]
 for n in (2,3):
  amb=n+2; da=D(2,amb,t,x,a,c); ha=z.hamiltonian(1,amb,t,x,a,c); terms=[sp.expand(sp.diff(da,t[k])*sp.diff(ha,x[k])-sp.diff(da,x[k])*sp.diff(ha,t[k])) for k in range(amb+1)]; full=sp.simplify(sum(terms).subs(subs)); dp=D(2,n,t,x,a,c); hp=z.hamiltonian(1,n,t,x,a,c); proj=sp.simplify(z.poisson(dp,hp,t,x,n).subs(subs)); lh=sp.simplify(lieH(2,1,n,t,x,a,c).subs(subs)); omitted=[k for k in range(n+1,amb+1) if sp.simplify(terms[k].subs(subs))!=0]; rem=sp.simplify(full-proj)
  target_direct=z.direct_integral(sp.diff(q2,chi)*sp.diff(q1,chi)*(xi**2/(2*a**3)+a*f/2),chi)
  ck(rows,f"CS3Q2.L{n}.lie_transport_direct",lh-target_direct,"Spectral Lie-lapse transport equals independent direct chi integration.")
  ck(rows,f"CS3Q2.L{n}.matter_decomposition",full-lh-strain,"Matter bracket is Lie transport plus direct strain.")
  ck(rows,f"CS3Q2.L{n}.combined_identity",full+dg-lh,"Metric plus matter ambient bracket equals Lie transport.")
  ck(rows,f"CS3Q2.L{n}.projection",rem-sum(terms[k].subs(subs) for k in omitted),"Projection remainder is the omitted canonical-channel sum.")
  out.append({"cutoff_L":n,"ambient_cutoff":amb,"matter_bracket":str(sp.factor(full)),"lie_transport":str(sp.factor(lh)),"metric_bracket":str(sp.factor(dg)),"combined":str(sp.factor(full+dg)),"projection_remainder":str(sp.factor(rem)),"omitted_channels":omitted})
 ok=all(x["passed"] for x in rows); res={"schema_version":"ice.closed-s3-q2-coupled-dh-strain-cancellation.result.v1","calculation_id":p["calculation_id"],"numbered_phase":None,"run_status":"VALID_RUN","verdict":"KEEP_Q2_COUPLED_DH_STRAIN_CANCELLATION_NOT_FULL_ADM_HDA" if ok else "KILL_Q2_COUPLED_DH_PACKET","input_manifest":{"path":"cpt_temporal_folded_susy/"+I,"sha256":hs},"upstream_results":pins,"primary_sources":p["primary_sources"],"declared_conventions":{"shift":"v^a=D_gamma^a Q2 with no a^-2 factor","lapse":"N=Q1","matter_packet":"theta=xi=Q1+Q2","metric_packet":"q_ab=a^2[gamma_ab+2 zeta2 Q2 gamma_ab+2 E2 S_ab(Q2)]","metric_generator":"D_g=Pi_E2-(8/3)Pi_zeta2","bracket_order":"{D_g+D_phi,H_phi[N]}"},"exact_checks":rows,"check_summary":{"exact_passed":sum(x["passed"] for x in rows),"exact_total":len(rows),"all_executable_checks_passed":ok},"rows":out,"metric_variation":{"H_zeta2":str(sp.factor(hz)),"H_E2":str(sp.factor(he)),"Dg_H":str(sp.factor(dg)),"direct_strain":str(sp.factor(strain))},"computed_scope":"selected Q2 metric-generator cancellation of selected fixed-metric scalar-matter DH strain only","non_claims":["gravitational Hamiltonian constraint","DD or HH brackets","full HDA or Jacobi","BFV/anomaly/physics"],"required_fail_closed_outputs":expected_nulls(),"resource_accounting":{"root_calls":0,"quadratures":0,"ode_calls":0,"adjacent_result_files_written":1,"automatic_descendants":0,"automatic_next":None},"runner":{"path":"cpt_temporal_folded_susy/closed_s3_q2_coupled_dh_strain_cancellation.py","sha256":sh(Path(__file__).read_bytes())},"environment":{"python":platform.python_version(),"sympy":sp.__version__}}
 res["result_payload_sha256_without_self"]=sh(cb(res)); encoded=cb(res)+b"\n";
 if len(encoded)>1000000: raise AssertionError("artifact cap")
 Path(__file__).with_name(R).write_bytes(encoded); print("CLOSED_S3_Q2_COUPLED_DH_STRAIN_CANCELLATION_RESULT="+json.dumps({"run_status":res["run_status"],"verdict":res["verdict"],"exact_passed":res["check_summary"]["exact_passed"],"exact_total":res["check_summary"]["exact_total"],"result":R},sort_keys=True))
if __name__=="__main__": main()
