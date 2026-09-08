# HSWM 네이티브 런타임에 대한 ICE dogfood 피드백

2026-09-08 · `LOCAL_ENGINEERING_FEEDBACK`.
이 메모는 ICE의 research state 여섯 문맥 field를 native TypeScript/Effect
runtime에 연결하며 확인한 구현 경계다. 물리 결과, HSWM 효능, 관계 발명이나
branch learning의 증거는 아니다. HSWM checkout의 source·SQLite·Git 이력은 이
작업에서 변경하지 않았다.

## 1. context-attempt key 검증 불일치

`adaptive-domain.ts`는 여섯 field의 첫 `updateModel` 뒤
`context_attempts`에 길이 1054의 생성 key를 남긴다. 다음 `predict`와
`updateModel`은 모든 attempt key를 일반 `text`의 256자 식별자 한도로
검증하므로 `MODEL_INVALID: adaptive model`을 반환한다. 따라서 첫 관측 뒤
그 route의 상태를 재사용할 수 없다.

[context-attempt-key-bound.patch](context-attempt-key-bound.patch)는 field 이름의
한도를 바꾸지 않는다. `context:`와 유효 feature key의 최대 개수·길이에서
유도한 별도 attempt-key 상한을 두고 그 index에만 적용한다. synthetic
regression은 원본의 six-field 실패, 패치 후 예측·세 번의 반복 update, 짧은
기존 parity model의 동일성, 유도 상한 초과 key 거절을 검사한다.

```sh
node scripts/qualify-hswm-context-key.mjs \
  --hswm-root /home/lagyeongjun/CD/HSWM \
  --output .ice/hswm-research/native/context-key-qualification
node scripts/check-hswm-context-key.mjs \
  --original-js /home/lagyeongjun/CD/HSWM/src/hswm/effect-runtime/dist/adaptive-domain.js \
  --patched-js .ice/hswm-research/native/context-key-qualification/dist/adaptive-domain.js
```

이것은 local qualification이며 upstream merge나 release가 아니다. 현재 확인한
원본 source/compiled SHA-256은 각각
`4d06d01c6550d9652385d4d43cf4b097ddbcbf7c246a2982c36657f3d2fbc98e`,
`b3ece0e434ea0b1b23d6803be68d84a6cde5029acafd9454e84f3ff5ea3f473b`다.
local patched compiled hash는
`b2f5dbfcffeb007a02dcc92a672096364aaadc22e7763d8019c8a3e83b35a8c6`이며,
candidate에는 patch·source·compiled hash와 runtime file 8개의 pin이 있다.
qualification copy는 실행에 필요한 `node_modules`를 sibling checkout으로 symlink한다.
따라서 이 pin은 entry와 여덟 runtime byte의 local identity를 확인할 뿐 dependency
closure 전체의 attestation은 아니다. upstream release 또는 더 강한 재현에는 lockfile과
dependency artifact identity를 별도로 묶어야 한다.

## 2. 중첩 research branch의 명시적 feedback

native graph에는 parent relation을 가진 nested trajectory가 기록되지만,
`feedback --episode`는 `trajectory:<episode>:0`만 찾아 root relation만 갱신한다.
`--trajectory`는 현재 unknown option으로 거절된다. 그래서 semantic-review의
실제 선택 relation과 그 stage output의 검토를 직접 연결할 수 없다.

제안하는 범위 제한 enhancement는 optional `--trajectory`다. 지정했을 때에는
그 trajectory가 episode 소속인지, 완료됐는지, selected relation을 갖는지를
검증하고 해당 relation만 갱신한다. 기록된 outcome은 episode·trajectory·stage·
reviewed output SHA-256·reviewer/source provenance를 함께 참조해야 한다.
기존 episode-only feedback은 root trajectory shorthand로 보존하면 된다. 필요한
회귀는 foreign trajectory 거절, nested relation만의 revision, 다음 plan의 변화,
그리고 root 호환성이다. 이것은 reviewer가 특정 실행 산출물을 평가했다는
provenance 계약이며, 독립 causal credit·과학적 참·관계 학습의 주장은 아니다.
