# Public Live 선행 설계 Human 결정

설계 상태: `HUMAN_ACCEPTED / FROZEN`. 구현 상태: `NOT_STARTED`.

권위는 1646 Task와 [Human acceptance Judgment](20260915_1646_aiscc-p3-3-public-live-human-acceptance-browser-judgment-1.md)이다. 아래 응답은 `HUMAN_PROVIDED`이며 Executor가 대신 결정한 값이 아니다. 1630 candidate의 H1-H7 선택은 종료되었고, 1600 시도는 여전히 REWORK_REQUIRED 이력이다.

| 결정 | Human 응답 | 확정 내용 |
|---|---|---|
| H1 | ACCEPT | 제출 이후 허용된 기간에 단일 scenario 선행 작업을 계속한다. 후속 작업은 별도 Task로 승인한다. |
| H2 | ACCEPT | `stockroom-s1-normal / 1.0.0`만 허용. client 3/hour·10/day, global 20/day·동시성 2, $0.20/run reserve·$4/day·$15 campaign. 정수 micro-USD ledger와 atomic admission 유지. |
| H3 | ACCEPT_BROWSER_RECOMMENDATION | daily ledger는 UTC day 유지. campaign cutoff는 `2026-10-18T00:00:00+09:00 exclusive`, 즉 `2026-10-17T15:00:00Z`. 해당 순간부터 신규 admission 금지. |
| H4 | ACCEPT | IPv4 /32·IPv6 /64 HMAC bucket. raw IP 저장/로그 금지. NAT 공유 제한 수용. campaign 종료+30일 보존, 미해결 liability만 연장. |
| H5 | ACCEPT_BROWSER_RECOMMENDATION | 256-bit read capability, 24h 만료, `sessionStorage` 보존. 같은 tab refresh 후 GET 재개 가능. URL·cookie·localStorage 금지. |
| H6 | ACCEPT | unknown provider outcome은 자동 재전송·환불·slot 회수 금지. 보수적 비용 산정과 quarantine 유지. Replay 독립성 보존. |
| H7 | ACCEPT | 별도 public Live DB/credentials. owner/private DB 공유 금지. 최소 권한 transaction boundary. |

## H5 운영 의미

성공한 최초 201 응답으로 받은 capability를 같은 tab의 `sessionStorage`에 저장한다. 일반 새로고침은 이를 유지하므로 24h 만료 전 GET을 계속할 수 있다. capability가 없는 독립된 새 tab/session은 복구할 수 없다. tab/session 종료 시 capability는 소실된다. 최초 성공 201 응답 자체를 받지 못했다면 복구 경로가 없고 자동 대체 run을 만들지 않는다. 같은 idempotency key의 재조회는 capability를 재발급하지 않는다. capability를 로그에 남기지 않으며 public cancel은 없다.

## 별도로 증명해야 할 release prerequisites

다음은 미결 H1-H7 선택이 아니라 구현·배포 단계의 증명 조건이다.

- Railway trusted ingress, header stripping/overwrite와 spoof 방어 증명.
- 실제 provider envelope·가격·설정 및 정수 비용 상한 증명. 1552의 계산은 잠정 입력이며 현재 외부 가격 검증이 아니다.
- execution process/filesystem/tool/network 격리와 실제 owner admission composition 증명.
- unknown outcome에서 worker 종료·no-send fencing·remote closure 증명. 불명확하면 slot quarantine 유지.
- 공유 ingress flood 제한과 read abuse 제한 증명. CORS는 인증이나 abuse 방지 수단이 아니다.
- additive migration, 정확한 fixture 범위와 DB 최소 권한 증명.
- 통합 테스트와 Human release acceptance. 설계 수락은 Live enablement가 아니다.

## 다음 단계

L0는 `COMPLETE / HUMAN_ACCEPTED`. L1·L4·L5는 별도 Task로 진행 가능한 후보이며 아직 시작하지 않았다. L2는 L1, L3는 L2, L6는 L3+L4+L5, L7은 L6, L8은 L7 이후 Human release decision에 의존한다. 기존 Replay-only release를 유지한다. 이 문서는 유료 resource 생성, source 구현 또는 deployment를 승인하지 않는다.
