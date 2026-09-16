# Human QA Gate: P3-3 Public Live L4 OpenAI Account Evidence

## meta

- task_id: `20260916_1310_aiscc-p3-3-public-live-l4-openai-account-evidence-human-gate-1`
- created_at: `2026-09-16 KST`
- owner: `HUMAN`
- task_type: `HUMAN_QA_GATE / ACCOUNT_EVIDENCE`
- IDE Executor: `NOT_APPLICABLE`
- expected repository HEAD: `04436a11adc6dd6e70b4a98568fe878cc4c9f4aa`

## 목적

Accepted L4 implementation에 실제 OpenAI API account/project evidence를 연결한다.

이 Gate는 UI/account 확인 작업이다.

코드 수정, IDE Executor 실행, paid provider request는 수행하지 않는다.

## 보안 규칙

절대 ChatGPT/Task/report/screenshot에 노출하지 말 것:

- API key secret value
- service account secret
- bearer token
- payment-card/bank information
- recovery/security code

Secret이 화면에 표시되면 screenshot 전에 완전히 가린다.

Secret key를 생성하는 경우 안전한 password manager/secret store에만 보관한다.

## Operation 1 — dedicated API Project

OpenAI API Platform에서 Public Live 전용 Project를 선택하거나 새로 만든다.

Default Project를 사용하지 않는다.

확인:

```text
Dedicated project:
PASS / FAIL

Project display name:
<non-secret name>

Default Project:
NO
```

Evidence:

- Project settings 화면 screenshot 1장.
- Project가 독립 project임을 확인할 수 있어야 한다.
- secret/key 값은 포함하지 않는다.

## Operation 2 — model availability / rate-limit evidence

Project Settings -> Limits / Model usage에서 `gpt-5.6-luna`를 확인한다.

기록:

```text
gpt-5.6-luna available:
PASS / FAIL

RPM:
<actual displayed value>

TPM:
<actual displayed value>

other applicable Luna limit:
<actual or NONE>
```

모델 access가 disabled라면 enable할 수 있는 정상 Project Owner UI control이 있을 경우 enable한다.

RPM/TPM 값을 이번 Gate에서 임의로 변경하지 않는다.

현재 실제 account/provider 값을 evidence로 기록한다.

Evidence:

- Luna model/limit row screenshot.

## Operation 3 — project hard spend limit

Project Settings -> Limits -> Spend -> Edit spend limit.

정확히 설정:

```text
Monthly spend limit:
USD 15

Enforce a hard limit:
ON
```

Save 후 다시 열거나 화면을 refresh하여 persisted state를 확인한다.

Evidence:

```text
$15 monthly:
PASS / FAIL

hard enforcement ON:
PASS / FAIL
```

Screenshot 필수.

Important:

OpenAI hard-limit enforcement는 즉시적이지 않을 수 있고 tracked spend가 설정값을 소폭 초과할 수 있다.

따라서 이 $15/month provider limit은 defense-in-depth이며 AISCC `$15/campaign` application budget을 대체하지 않는다.

## Operation 4 — spend alerts

Project-level monthly spend alerts를 다음 금액으로 설정한다.

```text
USD 10 / month
USD 12 / month
```

현재 OpenAI API Admin surface는 project spend alert를 currency + interval + threshold amount로 지원한다.

UI가 금액 단위 대신 다른 표현을 보이면 임의 환산/추측하지 말고 실제 UI를 screenshot하고 `UI_CONTRACT_MISMATCH`로 제출한다.

Evidence:

```text
$10 alert:
PASS / FAIL

$12 alert:
PASS / FAIL
```

Screenshot 필수.

## Operation 5 — billing/account readiness

Organization/Project billing/usage 상태를 확인한다.

Paid test request는 보내지 않는다.

다음만 확인:

```text
billing/account usable for API:
PASS / FAIL / NOT_DETERMINABLE

prepaid credit state if applicable:
SUFFICIENT / NOT_APPLICABLE / NOT_DETERMINABLE

organization usage tier/approved usage:
<visible non-secret summary>

blocking billing/quota warning:
NONE / <exact warning>
```

Payment method detail 또는 card/account number는 screenshot에서 제거한다.

## Operation 6 — dedicated runtime service account / key isolation

Dedicated Public Live Project 안에서 project-scoped service account를 준비한다.

Recommended display name:

`aiscc-public-live-runtime`

If an existing dedicated project-scoped service account is already suitable, reuse it and record that fact.

Key requirements:

1. project-scoped;
2. runtime-dedicated;
3. Restricted permissions preferred;
4. no broad organization/admin key;
5. secret value never submitted as evidence.

For a newly created service-account key:

- secret is shown only once;
- immediately store it in a secure secret/password manager;
- do not paste it into this chat;
- do not place it in repository/environment files during this Gate.

Permission target:

`/v1/responses` write only, plus only another endpoint permission if the accepted runtime demonstrably requires it.

If the UI cannot express the required narrow permission without granting broad access:

`BLOCKED_CREDENTIAL_PERMISSION_SCOPE`

and STOP before choosing `All`.

Evidence:

```text
project-scoped service account:
PASS / FAIL

runtime-dedicated:
PASS / FAIL

key permission mode:
RESTRICTED / OTHER

Responses write:
PASS / FAIL

secret exposed in submitted evidence:
NO
```

Screenshot should show only non-secret metadata/permissions.

## Operation 7 — no paid provider request

Confirm:

```text
real OpenAI Responses calls during this Human Gate:
0
```

Do not test Luna yet.

A real call requires a later explicit provider-verification Task.

## 제출 형식

Return exactly this block plus screenshots:

```text
L4 OpenAI Account Evidence

Operation 1 dedicated project:
PASS / FAIL
Project display name:

Operation 2 Luna access:
PASS / FAIL
RPM:
TPM:
Other limit:

Operation 3 hard spend:
PASS / FAIL
Monthly limit:
Hard enforcement:

Operation 4 alerts:
PASS / FAIL
Alert 1:
Alert 2:

Operation 5 billing:
PASS / FAIL / NOT_DETERMINABLE
Usage tier/limit summary:
Blocking warning:

Operation 6 credential isolation:
PASS / FAIL / BLOCKED_CREDENTIAL_PERMISSION_SCOPE
Service account:
Permission mode:
Responses write:
Secret included in evidence:
NO

Operation 7 paid calls:
0

Notes:
```

## PASS 기준

Human Gate PASS requires:

- dedicated non-default Project;
- Luna available;
- effective RPM/TPM captured;
- monthly spend limit = USD 15;
- hard enforcement = ON;
- alerts USD 10 and USD 12;
- billing/account state not visibly blocking bounded API use;
- dedicated project-scoped runtime credential capability;
- no secret leaked;
- zero paid request.

If credential permission UI cannot meet least privilege, report BLOCKED instead of broadening authority.

## Gate effect

PASS does NOT authorize Public Live release.

After Human PASS, Browser Command Center will determine whether:

1. L4 can advance to a separately authorized minimal real-provider verification; or
2. remaining credential/deployment binding belongs to L5 and L4 can close without a paid call.

No automatic next action is authorized by this Task.
