# IG-RUEQFT locality audit ontology

> This is a repository-local memory and index over one scoped external-theory audit. It is not an endorsement, a universal refutation, an ICE equivalence, or an external-KG ratification.

## Current result

The frozen oracle asks one narrow question: in a two-dimensional (N=64) free-fermion model with U(1) charge dephasing, does group averaging change an entanglement contribution into a bulk-volume density?

The recorded answer is **no for this model**:

| Diagnostic | First recorded value | Last recorded value | Scoped reading |
| --- | ---: | ---: | --- |
| (S_A/L^2) | 0.345408 at (L=4) | 0.137253 at (L=16) | decreases rather than remaining extensive |
| ((S_A+H(P_A))/L^2) | 0.451950 at (L=4) | 0.147472 at (L=16) | even the exact dephased-entropy upper bracket is subvolume across the scan |
| (S_A/(L\log L)) | 0.901892 at (L=6) | 0.792055 at (L=16) | compatible with the tested log-enhanced boundary interpretation |

This contradicts `claim:IGRUEQFT_GROUP_AVERAGING_MAKES_RECORDED_ENTANGLEMENT_BULK_LOCAL` within `scope:igrueqft-finite-free-u1-oracle`. It does **not** prove a thermodynamic-limit theorem or reject every interacting or gauge-completed IG-RUEQFT construction.

## Evidence chain

```text
external IG-RUEQFT proposal
  -> tested shortcut: charge group averaging makes S_ent bulk local
  -> finite free-U(1) correlation-matrix oracle
  -> upper dephased entropy / volume decreases
  -> shortcut CONTRADICTED in the frozen model
  -> full proposal remains untested without its action and continuum discriminator
```

The machine trace is:

```bash
./ice ontology guide --graph igrueqft --path igrueqft-locality-oracle
./ice ontology show igrueqft::claim:IGRUEQFT_GROUP_AVERAGING_MAKES_RECORDED_ENTANGLEMENT_BULK_LOCAL
./ice ontology trace igrueqft::claim:IGRUEQFT_GROUP_AVERAGING_MAKES_RECORDED_ENTANGLEMENT_BULK_LOCAL --depth 2
```

## Hash-pinned records

- [`../../igrueqft_locality_falsifier_2026-07-12/RESULT.json`](../../igrueqft_locality_falsifier_2026-07-12/RESULT.json) — observed numerical rows and verdict.
- [`../../igrueqft_locality_falsifier_2026-07-12/igrueqft_locality_falsifier.py`](../../igrueqft_locality_falsifier_2026-07-12/igrueqft_locality_falsifier.py) — producer.
- [`../../research/reports/thothsaem/THOTHSAEM_IGRUEQFT_NAESENGMOON_2026-07-12.md`](../../research/reports/thothsaem/THOTHSAEM_IGRUEQFT_NAESENGMOON_2026-07-12.md) — adversarial interpretation and scope.
- [`../../research/reports/thothsaem/THOTHSAEM_UEQFT_SOURCING_2026-07-12.md`](../../research/reports/thothsaem/THOTHSAEM_UEQFT_SOURCING_2026-07-12.md) — proposal/source boundary and non-equivalence to ICE.

## Open boundary

Two distinct problems remain:

1. Specify and independently check the proposal-specific information-gauge action, matter coupling, constraints, and stress tensor.
2. Build a controlled interacting and continuum scaling discriminator rather than extrapolating one finite free model.

The external KG has one collision-free legacy `IG-RUEQFT` BookConcept, linked only as `RELATED`. No matching validation-result UID was found, and the available connector is read-only, so the result bridge remains explicitly `UNRESOLVED`.
