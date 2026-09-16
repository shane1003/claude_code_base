# Task Handoff Rule

Claude never commits or pushes. The user reviews and commits manually.
Therefore **every task that changes files must end by writing a handoff
file**, so the user can review, give feedback, and commit without
re-reading the diff.

## Where
- Path: `.claude/HANDOFF.md` (git-ignored).
- **Overwrite** it on every task and on every `/handoff` call. It always
  reflects the *current uncommitted* working tree only — never append or
  keep old entries. Once the user commits, the content is stale by design.
- After writing the file, print in chat: the file path, a one-line status of
  the checks, and the **💬 커밋 추천** section verbatim (the user writes the
  commit by hand from it). Do not paste the rest of the file into chat.

## Language
Body in **Korean**. The commit message in **English**, one line, following
`.claude/rules/commit.md` (`TYPE: sentence`).

## Format

````markdown
# Handoff — <branch> @ <YYYY-MM-DD HH:MM>
<!-- 마지막 작업 시점의 "커밋되지 않은 변경"만 반영. /handoff 로 갱신됩니다. -->

## 📋 작업 이력
- <변경 1: 어떤 파일에서 무엇을 왜 바꿨는지, 동작 관점으로 한 줄>
- <변경 2 ...>

## 🔍 커밋 전 확인 포인트
- 실행한 검증: <pytest / ruff / mypy 결과. 안 돌렸으면 "실행 안 함: <사유>">
- 검증 못 한 것: <수동 확인이 필요한 부분, 없으면 "없음">
- 주의 지점: <동작이 바뀌는 곳, 지표·데이터 파이프라인 변경, 되돌리기 어려운 것>

## 🧪 실험 정보 (실험을 돌렸을 때만)
- config: <configs/... 경로>  ·  seed: <값>  ·  git: <hash 또는 "uncommitted">
- 결과 위치: <outputs/<run>/ 경로>
- 핵심 지표: <baseline → 이번 (metric 이름 포함)>
- 스모크 런 여부: <--debug 로 코드 경로 검증했는지>

## 💬 커밋 추천
- **무엇을**: <이 커밋에 담기는 변경을 한 문장으로>
- **왜 지금**: <지금이 커밋 경계로 적절한 이유. 예: 실험 코드 완결 / 검증 통과 / 되돌릴 수 있는 최소 단위.
  아직 커밋하면 안 되는 상태면 "보류 권고: <사유>"와 커밋 가능 조건>
- **타입 선택**: <TYPE과 선택 이유 (commit.md 우선순위: 프로젝트 타입 → numpy 타입)>
- **추천 메시지**:
  ```sh
  git commit -m "TYPE: one sentence in English"
  ```

## 📝 상세 기록 (선택)
<!-- 판단 근거, 검토했다가 버린 대안, 남은 TODO, 사용자에게 묻고 싶은 것.
     파일이므로 길어도 됩니다. 사용자가 여기에 피드백을 달 수 있습니다. -->
````

## Rules
- **작업 이력**: describe behavior/state changes, not a file list. 2–6 bullets.
- **확인 포인트**: be honest. A failed or skipped check must be stated, never
  hidden. Include the exact command the user can run to verify.
- **실험 정보**: include this section only when a training/eval run was
  executed in this task. Config path, seed, and result directory are
  mandatory so the run can be found and reproduced later. If the metric
  changed against baseline, state both numbers with the metric name.
  Omit the section entirely for pure code changes.
- **커밋 추천 · 무엇을**: one sentence naming the unit of change, so the user
  can judge whether the message below matches it.
- **커밋 추천 · 왜 지금**: justify the commit *boundary*, not the change. A
  good boundary is a coherent, self-contained, revertable unit whose checks
  pass. In a research repo, "experiment config + the code it needs" is a
  natural unit; "half-migrated metric" is not. If the tree is half-done,
  checks fail, or unrelated changes are mixed, say **보류 권고** with the
  reason and what would make it committable (e.g. "테스트 통과 후",
  "config와 metric 수정을 분리한 뒤"). Never recommend committing a broken
  state just because work stopped.
- **커밋 추천 · 타입 선택**: name the TYPE and why, so the user can override it
  with the same reasoning.
- **커밋 추천 · 추천 메시지**: exactly one line. If the change cannot be
  described in one sentence, propose a **split** instead: list 2–3 commits
  in order, each with 무엇을 / 왜 지금 / files to stage (`git add <files>`) /
  one-line message.
- **상세 기록**: optional. Use it for reasoning, rejected alternatives, open
  questions, and leftover TODOs. This is the place for length — keep the
  sections above short.
- **Feedback loop**: if the user has written notes into `.claude/HANDOFF.md`
  (anything that is not Claude's own text), read them at the start of the
  next task and treat them as instructions before overwriting the file.
- Do not stage files (`git add`) unless the user asks; leave the working tree
  as-is for the user to review.
- If nothing was changed (question, analysis, review only), do not touch the
  file.
