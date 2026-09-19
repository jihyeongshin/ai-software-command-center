# Human Public-Site Smoke Result

## status

`HUMAN_PUBLIC_SITE_SMOKE_PASS`

## submitted result

```text
Operation 1 공개 페이지 접속:
PASS

Operation 2 Recorded Replay:
PASS

Operation 3 Live release UI:
PASS

Operation 4 Human Live 시작:
PASS
클릭 횟수: 1

Operation 5 terminal 상태:
PASS
Run ID: YCWVxQpsnK8M5VNzTXtj5Q
최종 Run state: COMPLETED

Operation 6 projection identity:
PASS
Mode: PUBLIC_BOUNDED_LIVE
Scenario / version: stockroom-s1-normal / 1.0.0

Operation 7 Replay/Live 공존:
PASS

Operation 8 시각/사용성:
PASS
```

## screenshot evidence

- `KakaoTalk_20260919_222856152.png` — SHA-256 `bdfb1b83a8d099bc212af13cec2ad85ba97da3ac8cec9fdb8f085c3ceca27805`
- `KakaoTalk_20260919_222907342.png` — SHA-256 `ddd3ba55bcd0ece9784a2c705aa4c4d4e06a60e22dc60b424f03dc83cf82d2d0`
- `KakaoTalk_20260919_222914318.png` — SHA-256 `08d961ed194f464c61b46ffbc77020b8ca93359ee7d9f1f972928193a8270d51`

## Browser admission

The screenshots are consistent with the submitted result.

Observed directly:
- public Bounded Live terminal `COMPLETED`;
- Run `YCWVxQpsnK8M5VNzTXtj5Q`;
- mode `PUBLIC_BOUNDED_LIVE`;
- scenario/version `stockroom-s1-normal / 1.0.0`;
- release-configured Live UI;
- four Recorded Replay scenarios;
- Live and Replay remain visually distinguishable.

No secret-bearing browser DevTools/Network/Storage material was submitted.

## result

`HUMAN_PROVIDED / ACCEPTED`
