# Claude Code Base Template — Research Case

ML 연구/실험 레포(PyTorch + uv)에 복사해서 쓰는 Claude Code 설정 템플릿입니다.
API-case와 **Section B(공통 규칙)·커밋 규칙·핸드오프 워크플로우는 동일**하고,
아래 항목이 연구 레포에 맞게 다릅니다.

## API-case와 다른 점

| 항목 | API-case | Research-case |
| --- | --- | --- |
| CLAUDE.md Section A | FastAPI 레이어 규칙 | config-driven 실험, 실험 격리, run 디렉토리, 디바이스 처리 |
| Never Do 추가 | — | `outputs/`·`data/`·`weights/` 삭제 금지, 지표 변경 시 테스트 필수, 노트북 출력 커밋 금지, 풀 학습 임의 실행 금지 |
| code-style.md | FastAPI 아키텍처, HTTP 에러 처리 | 텐서 shape 문서화, 재현성(seed), config 구조, 디바이스, 순수 metric 함수, 실패는 크게 |
| settings.json | — | `nvidia-smi` 허용, `rm -rf`/`rm -r` deny (실험 결과 보호) |
| hooks/format.py | `.py` → ruff format | + `.ipynb` → nbstripout (NotebookEdit 매처 추가) |
| handoff.md | — | 🧪 실험 정보 섹션 (config·seed·git hash·결과 위치·지표 델타) |
| MR template | ML 블록은 선택 | 실험 결과 비교표(baseline vs 이번) 필수 섹션, ML 체크리스트 상시 |
| code-reviewer | 레이어 분리·DI | shape/broadcast 버그, seed·device·경로 하드코딩, 지표-테스트 동반 변경 |
| skills | refactor / mr / handoff | + **`/experiment`** (가설 → config 복사 → 스모크 런 → LOG 기록) |
| .gitignore | Python 기본 | + data/weights/outputs, 체크포인트 확장자, 트래커 디렉토리 |

## 구조

```
CLAUDE.md                        # 프로젝트 지침 (Section A: 레포별 / Section B: 공통)
.claude/
├── settings.json                # 권한 allowlist + deny + 훅
├── settings.local.json          # 개인 설정 (gitignore 대상)
├── HANDOFF.md                   # 작업 마무리 핸드오프 (덮어쓰기, gitignore 대상)
├── hooks/
│   └── format.py                # .py → ruff format, .ipynb → nbstripout
├── rules/
│   ├── code-style.md            # Python/ML 연구 코드 스타일
│   ├── commit.md                # 커밋 메시지 규칙 (API-case와 동일)
│   └── handoff.md               # 핸드오프 형식 (+ 실험 정보 섹션)
├── skills/
│   ├── experiment/SKILL.md      # /experiment — 새 실험 셋업 절차
│   ├── refactor/SKILL.md        # /refactor (동일)
│   ├── handoff/SKILL.md         # /handoff (동일)
│   └── mr/
│       ├── SKILL.md             # (동일)
│       └── template.md          # MR 템플릿 (실험 결과 비교표 포함)
└── agents/
    └── code-reviewer.md         # 연구 코드 리뷰어
```

## 새 레포에 적용하는 방법

1. `CLAUDE.md`, `.claude/`, `.gitignore`, `.gitattributes`를 통째로 복사합니다.
2. `CLAUDE.md` **Section A**의 명령어(`src.train`, `src.eval` 등)와 디렉토리 레이아웃을
   실제 레포 구조에 맞게 교체합니다. **Section B**는 수정하지 않습니다.
3. 프로젝트에 `nbstripout`을 추가합니다 (`uv add --dev nbstripout`).
   노트북을 안 쓰면 `hooks/format.py`의 `.ipynb` 분기를 지워도 됩니다.
4. `experiments/LOG.md`를 만들어 두면 `/experiment`가 거기에 기록합니다 (없으면 자동 생성).
5. 학습 명령을 Claude가 직접 실행하게 하려면 `settings.json` allowlist에
   `Bash(uv run python -m src.train:*)`를 추가하세요. 기본은 **스모크 런도 권한 프롬프트**를
   거치도록 열어두지 않았습니다 (GPU 시간 보호).

## 원칙

- **결과는 config·seed·git hash·데이터 버전으로 추적 가능해야 한다**: 이 넷 중 하나라도 없는 run은 재현 불가로 간주합니다.
- **지표 코드는 테스트와 함께 움직인다**: metric 함수 변경 = known-answer 테스트 변경. 리뷰어가 CRITICAL로 잡습니다.
- **실험 결과는 지우지 않는다**: `rm -rf`를 deny하고, `outputs/`는 run별 디렉토리로 격리합니다.
- **풀 학습은 사람이 시작한다**: Claude는 스모크 런까지만, 명령어를 제시하고 사용자가 실행합니다.
- **강제할 수 있는 것은 문서가 아니라 훅·권한으로**: 포맷팅은 PostToolUse 훅, 커밋·푸시·삭제 금지는 `settings.json` deny.
- **커밋·푸시는 사람이**: Claude는 `.claude/HANDOFF.md`를 덮어써서 작업 이력·확인점·커밋 추천을 남기고, 사용자가 그걸 보고 커밋합니다. 사용자가 그 파일에 남긴 메모는 다음 작업의 지시로 읽습니다.
- **팀 공통은 `settings.json`, 개인 취향은 `settings.local.json`**.

## API-case와 같이 유지해야 하는 파일

두 케이스는 각각 독립적으로 관리하되, 아래 파일은 **동일하게** 두는 것이 좋습니다.
한쪽을 고치면 다른 쪽에도 같은 변경을 반영하세요.

- `CLAUDE.md`의 Section B (행동 원칙, 공통 Never Do, 스타일 요약, 워크플로우)
- `.claude/rules/commit.md`
- `.claude/rules/handoff.md`의 골격 (작업 이력 → 확인 포인트 → 커밋 추천 → 상세 기록)
- `.claude/skills/refactor/SKILL.md`, `.claude/skills/mr/SKILL.md`, `.claude/skills/handoff/SKILL.md`
- `.claude/settings.json`의 `deny` 목록 (`git commit`, `git push`)
- `.gitattributes`
