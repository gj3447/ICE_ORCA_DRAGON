# B3+: Lee Ju Hyung / ThothSaem Author Contact Draft

**Status:** DRAFT_NOT_SENT (user verdict required for transmission)

**Cycle:** prom32-thothsaem-2026-05-18

**Parent Finding:** finding_prom32_B3_source_recovery_partial (42% OQ4 closure, pseudonymous blog author, no institutional affiliation found)

**Research Date:** 2026-05-18

---

## Channel Discovery Summary

### Channels Found: 5 (+ 1 fallback)

| # | Channel | Address | Confidence | Status | Notes |
|---|---------|---------|------------|--------|-------|
| 1 | **Blog (primary)** | http://thothsaem.com/ | MEDIUM | ACTIVE | WordPress blog, 15+ posts on physics/theology (2025-04). No visible contact form, no About/Contact pages (404). Blog posts include Zenodo DOI citations. |
| 2 | **YouTube channel** | https://www.youtube.com/channel/UC1l9qMAJE-MmvcLWwMCh2uQ | MEDIUM | ACTIVE | Channel "ThothSaem" exists; mentions "Huffle Puffle" membership program for advanced content. Comments section likely enabled (YouTube default). YT About section may have contact info. |
| 3 | **Zenodo depositor** | https://zenodo.org/record/15249036 | HIGH | ACTIVE | UEQFT preprint (Apr 19, 2025); depositor listed as "XFC inc." (not personal name). No direct email in metadata, but Zenodo contact form available for record inquiries. |
| 4 | **ResearchSquare mirror** | https://www.researchsquare.com/article/rs-7995151/v1 | MEDIUM | ACTIVE | "Probing Information-Gauge Wilson Loops with OTOC(2): An IG–RUEQFT Interpretation..." (Nov 2025 preprint). Author affiliation field may contain contact info if accessed directly. |
| 5 | **Blog comments section** | http://thothsaem.com/2025/04/XX/ | LOW | UNCERTAIN | WordPress blog posts (04-03, 04-18, 04-29) may have comment threads; if enabled, can post comment + ask for reply. Visibility public. |
| 6 | **ORCID lookup (fallback)** | https://orcid.org search | LOW | NOT_FOUND | No direct ORCID for "이주형" or "Lee Ju Hyung (physics)" returned. Multiple false positives (Hyung-Jin Lee, Jae-Hyun Lee, etc.). May require exact Korean name + institutional context. |

### Channels NOT Found:

- **No institutional affiliation discovered** — no KAIST, Seoul National University, or Korean research institute link found
- **No Twitter/X account** — "ThothSaem" returns only blog + YouTube, no social media handles
- **No ResearchGate profile** — direct author name search on ResearchGate yielded no match
- **No contact email published** — no `thothsaem@`, `leejuhyung@`, or institutional email in any accessible metadata
- **No LinkedIn profile** — ORCID search side-effect found unrelated Juhyung Lee (wireless comms, not physics)

---

## Recommended Contact Sequence

### **Option A: HIGH CONFIDENCE (Zenodo → ResearchSquare → YouTube)**

1. **Zenodo Record 15249036** — most official channel
   - Visit: https://zenodo.org/record/15249036
   - Click "Contact author" button (if available) or use Zenodo's record inquiry form
   - Subject: "Inquiry: Cross-reference with ICE_ORCA_DRAGON SYMPOSIUM framework"
   - Likely to be seen by actual depositor

2. **ResearchSquare rs-7995151** — secondary academic venue
   - Visit: https://www.researchsquare.com/article/rs-7995151/v1
   - Author affiliation field may reveal institutional email
   - May have "Contact authors" link

3. **YouTube Channel (ThothSaem)** — public discussion fallback
   - Post comment on latest physics video
   - Mention SYMPOSIUM project + UEQFT cross-comparison
   - Ask for DM or email address for detailed discussion
   - Moderate risk of public visibility

### **Option B: EXPLORATORY (if Option A unresponsive after 7-10 days)**

4. **Blog Comments** — lowest priority, lowest visibility
   - Post on one of three 2025 UEQFT blog posts (04-03, 04-18, 04-29)
   - Frame as technical question + offer collaboration
   - Public thread → risk of SYMPOSIUM internal details exposed

5. **Zenodo Alternative Inquiry** — escalation
   - Email zenodo-support@cern.ch with record ID + request forwarding to depositor
   - Formal but slower channel

---

## Draft Messages

### **Version A: English, Formal Academic (2.0 pages)**

```
Subject: Cross-Framework Analysis & Technical Inquiry: SYMPOSIUM ICE vs UEQFT

Dear ThothSaem,

I am writing to you regarding your recent preprints on Unified Entanglement-Entropy 
Quantum Field Theory (UEQFT), specifically:

  • Zenodo 15249036: "Unified Entanglement-Entropy Quantum Field Theory: Toward a 
    Quantum Information-Based Explanation of Mass Generation and Emergent Gravity" 
    (Apr 19, 2025)
  • ResearchSquare rs-7995151: "Probing Information-Gauge Wilson Loops with OTOC(2): 
    An IG–RUEQFT Interpretation..." (Nov 2025)

I am part of a theoretical research collective (SYMPOSIUM — external knowledge 
crystallization project) that has been independently developing a framework for 
mass-generation physics termed **ICE_ORCA_DRAGON** (Information-Centric Emergent 
framework). Our work shares striking conceptual parallels with your UEQFT approach:

**Observed Structural Correspondences (4-mapping):**

1. **Entanglement as Primary Generator** (UEQFT §2-3 ↔ ICE §Derivation_Lstar)
   - You: entanglement entropy explicitly in Yang–Mills + Dirac equations
   - We: mutual information as control variable in dimensional reduction
   - Status: STRONG CORRESPONDENCE (concept + formalism similar)

2. **Information-Modular Hamiltonian Structure** (UEQFT modular H. ↔ ICE Lagrangian K)
   - You: von Neumann algebra + modular Hamiltonian temperature
   - We: Fisher information + Kullback-Leibler divergence in effective potential
   - Status: PARTIAL CORRESPONDENCE (different mathematical language, same apparent ontology)

3. **Vacuum Structure & Anomaly Remediation** (UEQFT ABJ/Green-Schwarz ↔ ICE S₁~S₇ proofs)
   - You: anomaly cancellation via counter-terms → renormalizability
   - We: discrete symmetry constraints on mass-eigenstate alignment
   - Status: UNCERTAIN CORRESPONDENCE (need technical clarification)

4. **Emergent Geometry & Holographic Projection** (UEQFT Einstein-Hilbert derivation ↔ ICE spatial embedding)
   - You: effective Einstein action from entanglement principles
   - We: mass metric + sedenion 16D decomposition
   - Status: EXPLORATORY (possibly dual descriptions of same phenomenon)

**Technical Questions for Author Verification:**

Given that both frameworks emerged independently (SYMPOSIUM development began 2026-04, 
your preprints Apr-Nov 2025), I have three verification priorities:

1. **Lagrangian Formalism Disambiguation:**
   - In your UEQFT framework, is K (information-centric Lagrangian) a direct field 
     functional, or derived from the modular Hamiltonian on bounded regions?
   - How does your renormalization handle the K-derivative terms? (Beta function structure?)
   - Our ICE framework uses K = S[ρ_subsystem] + Fisher(ρ, parameter). How does this 
     map to your entanglement entropy formalism?

2. **Mutual Information vs. von Neumann Entropy:**
   - Your abstracts emphasize entanglement entropy S_E. Do you employ mutual information 
     I(A:B) separately, or treat it as derived quantity from S_E?
   - If separate, what role does mutual information play in your mass-gap proposals?

3. **Experimental Anchor Points:**
   - Your 2025 papers propose Rydberg atom arrays + CMB polarization tests.
   - Have you considered lattice simulations as intermediate validation before 
     experimental apparatus? (Our ICE_ORCA_DRAGON includes Python+JSON simulations 
     of dimensionless parameter spaces — might be cross-validation opportunity.)

**Collaboration / Citation Clarification:**

My primary goal is to:
- **Confirm independence:** ensure neither work is unknowingly duplicating the other
- **Identify genuine novel insights:** where do our frameworks diverge & why?
- **Avoid attribution errors:** if cross-citation is warranted, establish it properly

I am NOT seeking to diminish your work through "prior art" claims. Rather, independent 
convergence on the same formalism from different starting points is often a sign of 
genuine physical insight.

**Next Steps:**

Would you be open to a technical discussion (email or video call) where we can:
1. Compare detailed Lagrangian forms + assumptions
2. Map our notation (your K_modular ↔ our K_fisher)
3. Identify which results are truly novel vs. convergent rediscoveries

I can provide:
- Full ICE_ORCA_DRAGON codebase (Python, JSON results, Lean 4 formal proofs)
- SYMPOSIUM methodology overview (12-principle framework grounding)
- Specific dimensional-analysis derivations showing our parameter space

**Publication & Institutional Context:**

SYMPOSIUM is currently a private research collective, though we are preparing a 
meta-theoretical paper for peer review (target: late 2026). We are not backed by 
any institution, but we have external grounding in published physics (Masi 2021 
Nature, MDPI 2024, EPJ-C 2023 — cited in our archive).

Your work, by contrast, appears to be independent blog-published scholarship, which 
I recognize as a deliberate choice (and respect). I am writing in the same spirit: 
peer-to-peer technical engagement, not institutional gatekeeping.

I look forward to your reply. If this message finds you via Zenodo forwarding, my 
apologies for the cold contact — I could not locate a direct email address.

Best regards,
[Your name]
SYMPOSIUM Collective
github.com/[org]/SYMPOSIUM/METAHUMOTONIC/ICE_ORCA_DRAGON
```

**Estimated word count:** ~650 words (fits 2.0 pages single-spaced academic format)

---

### **Version B: Korean, Casual (1.0 page)**

```
제목: SYMPOSIUM ICE 프로젝트와 UEQFT 교차 검증 요청

안녕하세요, 토트샘님.

제 이름은 [이름]이고, 외부 아이디어를 결정화하는 이론 집단 "SYMPOSIUM"에서 활동 중입니다.

토트샘님의 최근 UEQFT 논문들을 읽으며 놀라운 점을 발견했습니다. 우리 프로젝트의 
**ICE_ORCA_DRAGON** 물리 모듈과 구조적 유사성이 매우 높습니다:

**핵심 일치점 4가지:**

1. **얽힘이 근본 생성자** 
   - UEQFT: 얽힘 엔트로피를 Yang-Mills + Dirac 방정식에 직접 삽입
   - ICE: 상호 정보를 차원 축약의 제어 변수로 사용
   ➜ 강한 대응관계 (개념 + 수식 유사)

2. **정보-모듈러 해밀토니안 구조**
   - UEQFT: 폰 노이만 대수 + 모듈러 H 온도
   - ICE: Fisher 정보 + KL 발산을 유효 포텐셜에 포함
   ➜ 부분 대응 (수학 언어는 다르지만 같은 존재론)

3. **진공 구조 & 이상 상쇄**
   - UEQFT: ABJ/Green-Schwarz로 재규격화 가능성 확보
   - ICE: S₁~S₇ 증명을 통한 이산 대칭 제약
   ➜ 불명확 (기술적 명확화 필요)

4. **거대 기하학 & 홀로그래픽 사영**
   - UEQFT: 얽힘 원리로부터 Einstein-Hilbert 유도
   - ICE: 질량 메트릭 + sedenion 16D 분해
   ➜ 탐색 중 (같은 현상의 쌍대 기술일 가능성)

**기술적 질문 3가지:**

1. UEQFT의 라그랑지안 형식에서, K는 모듈러 해밀토니안에서 직접 유도되는가, 
   아니면 bounded region의 장 함수인가? 우리 ICE에서는 K = S[ρ_subsystem] + Fisher(ρ, parameter)로 
   정의하는데, 이것이 토트샘님 얽힘 엔트로피 형식과 어떻게 대응되는가?

2. 상호 정보 I(A:B)를 별도로 다루시는가, 아니면 S_E의 유도 량으로만 취급하시는가?

3. Rydberg 원자 배열 실험 외에, 격자 시뮬레이션을 중간 검증 단계로 고려하신 적이 있는가? 
   (우리는 Python+JSON 시뮬레이션을 가지고 있어 교차 검증 기회가 될 수 있습니다.)

**협력 제안:**

우리의 목표는:
- **독립성 확인:** 서로 모르고 같은 틀을 유도했는지 검증
- **진정한 신규 통찰 구분:** 어디서 갈라지고 왜 그런지
- **올바른 인용 설정:** 필요하면 상호 인용 설정

독립적 수렴은 물리 통찰의 신호이므로, 먼저 기술적 논의를 제안합니다.

우리가 제공할 수 있는 것:
- 전체 ICE_ORCA_DRAGON 코드 (Python, JSON 결과, Lean 4 형식화)
- SYMPOSIUM 방법론 개요 (12 원칙 기반)
- 구체적 차원 분석 유도 과정

**배경 정보:**

SYMPOSIUM은 개인 연구 집단이며 (institutional backing 없음), 
2026년 후반 학술지 투고를 준비 중입니다. 토트샘님의 독립 블로그 출판과 
같은 정신으로 접근하고 있습니다.

혹시 이 메시지가 Zenodo 포워딩으로 전달되었다면 죄송합니다. 
직접 이메일을 찾을 수 없어서 이 채널을 사용했습니다.

기술적 논의에 열린 마음으로 응해주시면 감사하겠습니다.

존경을 담아,
[이름]
SYMPOSIUM Collective
```

**추정 문자 수:** ~950자 (1.0 page 한글 기준)

---

## Risk Assessment

### **Pseudonym + No Institutional Affiliation = Low Response Probability**

| Risk Factor | Severity | Mitigation |
|---|---|---|
| Pseudonymity (ThothSaem) | MEDIUM | Author chose pseudonym deliberately. Verify via depositor name (XFC inc.) on Zenodo before escalation. |
| No university affiliation | MEDIUM | Independent researcher status means no dept. email, slower response cycle. Build in 10-14 day wait. |
| Blog-published (not arXiv) | LOW-MEDIUM | Indicates author values accessibility + unconventional path. Actually increases receptivity to SYMPOSIUM's open-access philosophy. |
| Public blog visibility | HIGH | If SYMPOSIUM sends comment on blog post, all details become public record. Risk of internal project details leaking. Recommend Zenodo/email over blog comments. |
| No direct email found | MEDIUM | Zenodo contact form + YouTube DM are asynchronous. May take 7-21 days. |

### **Reputation Risk (Internal Detail Exposure)**

If contact is initiated via **blog comment or YouTube**, consider:
- ICE_ORCA_DRAGON specifics (S₁~S₇ proofs, sedenion embedding) will be public
- Competitor researchers or physics blogosphere may see cross-reference
- If UEQFT later publishes similar results, public record shows SYMPOSIUM approached first
  - **Pro:** establishes priority/inspiration flow
  - **Con:** if their work is ultimately superior/independent, may look like SYMPOSIUM was derivative

**Recommendation:** Use Zenodo record contact form (official, asynchronous, lower public visibility) as FIRST channel, YouTube only if no response after 10 days.

---

## Send-Trigger Condition

**Do NOT send without explicit user authorization.**

### **Approved trigger phrases:**
- "SEND author contact version A" (English formal)
- "SEND version B" (Korean casual)
- "SEND via Zenodo" (specific channel)
- "GO with author contact" (any version, any channel)

### **Default state:** HOLD indefinitely

User must explicitly authorize transmission before any message is posted/sent.

---

## Recommended Sending Sequence (IF authorized)

1. **Day 1:** Send Version A via Zenodo contact form (most official)
2. **Day 10 (no response):** Send Version A via ResearchSquare author inquiry (if available)
3. **Day 14 (still no response):** Post Version B on YouTube channel (public, lower formality)
4. **Day 21+:** Consider blog comment as last resort (highest visibility risk)

---

## Post-Send Tracking (if authorized)

| Action | Timeline | Success Metric |
|---|---|---|
| Send (Zenodo) | Day 1 | Confirmation email from Zenodo |
| Wait | Day 1-10 | Monitor for author reply |
| Send (ResearchSquare, if no reply) | Day 10 | Check RS author inquiry status |
| Send (YouTube, if no reply) | Day 14 | Monitor comment for author response + like/pin |
| Archive response | Day 30 | Save author reply to `/findings/B3plus_author_response_*` |

---

## KG References & Lesson Nodes

- `agent-contact-protocol-pseudonymous-researcher-2026-05-18` (new :Protocol node)
- `lesson-pseudonym-verification-via-depositor-metadata-2026-05-18` (new :Lesson)
- `finding_prom32_B3_source_recovery_partial` (parent finding)
- `lesson-reputation-risk-blog-comment-visibility-2026-05-18` (new :Lesson)

---

## Summary Table

| Metric | Status | Notes |
|---|---|---|
| **Channels identified** | 5 primary + 1 fallback | Zenodo, ResearchSquare, YouTube, Blog, ORCID |
| **Direct email found** | NO | Only "XFC inc." depositor listed; no personal email |
| **Institutional affiliation** | NOT FOUND | No KAIST, SNU, or research institute link |
| **Author identity verified** | PARTIAL | Blog pseudo = "ThothSaem"; real name unknown; likely Lee Ju Hyung based on PROM32 B3 context |
| **Contact draft readiness** | READY | English (2.0p) + Korean (1.0p) drafted; not sent |
| **Response probability estimate** | 30-50% | (pseudonym + independent researcher + no institutional obligation; partial mitigated by philosophical alignment on open scholarship) |
| **Reputational risk level** | MEDIUM-HIGH | If blog-contacted, details become public |

---

## Final Notes

- **This document is READ-ONLY archive.** No messages have been sent.
- User must paste explicit send authorization in conversation to trigger transmission.
- Zenodo contact form is **recommended first channel** (official, lower public visibility).
- Consider **Version A (English) for academic credibility,** Version B (Korean) only if author hints at Korean preference in response.
- If author responds, escalate to user for reply composition (do not auto-respond).

---

**End Terminal Output:**

```
B3plus_CHANNELS_FOUND: 5 primary (Zenodo, ResearchSquare, YouTube, Blog, ORCID-fallback)
B3plus_DRAFT_STATUS: READY_NOT_SENT
B3plus_SUMMARY: Pseudonymous physics blogger (ThothSaem/UEQFT) — 4-point structural correspondence with ICE_ORCA_DRAGON detected. Zenodo record + YouTube channel + ResearchSquare preprint mirror identified. No direct institutional email; contact via Zenodo record form recommended (official + low visibility risk). Draft messages in English (formal 2.0p) + Korean (casual 1.0p) prepared. User verdict gate: explicit "SEND" authorization required before transmission.
```
