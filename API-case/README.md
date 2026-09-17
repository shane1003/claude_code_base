# Claude Code Base Template

새 레포에 복사해서 쓰는 Claude Code 공통 설정 템플릿입니다.

## 구조

```
CLAUDE.md                        # 프로젝트 지침 (Section A: 레포별 / Section B: 공통)
ruff.toml                        # ruff 설정. Markdown을 포맷 대상에서 제외 (아래 "주의" 참고)
.claude/
├── settings.json                # 권한 allowlist + 훅 (팀 공유, 커밋 대상)
├── settings.local.json          # 개인 설정 (gitignore 대상, 필요 시 각자 생성)
├── HANDOFF.md                   # 작업 마무리 핸드오프 (매 작업마다 덮어쓰기, gitignore 대상)
├── hooks/
│   └── format.py                # 수정한 파일 한 개만 ruff format (PostToolUse)
├── rules/                       # 자동 로드되는 규칙 문서
│   ├── code-style.md            # Python/FastAPI 스타일 가이드
│   ├── commit.md                # 커밋 메시지 규칙 (numpy style, 제목 한 줄만)
│   └── handoff.md               # 작업 마무리 핸드오프 형식 (이력·확인점·커밋 추천: 무엇을/왜 지금/타입/메시지)
├── skills/                      # /명령으로 호출 가능한 스킬
│   ├── refactor/SKILL.md        # /refactor — 안전한 리팩토링 절차
│   ├── handoff/SKILL.md         # /handoff — HANDOFF.md 갱신
│   └── mr/                      # /mr — MR 본문 생성
│       ├── SKILL.md
│       └── template.md          # MR 템플릿 (공통 + ML 전용 체크리스트)
└── agents/
    └── code-reviewer.md         # 커밋 전 diff 리뷰 서브에이전트
```

## 새 레포에 적용하는 방법

1. `CLAUDE.md`, `ruff.toml`, `.claude/` 디렉토리를 통째로 복사합니다.
   레포에 이미 `pyproject.toml`의 `[tool.ruff]` 설정이 있다면 `ruff.toml`은 지우고
   `extend-exclude` 줄만 기존 설정에 합치세요. `ruff.toml`이 `pyproject.toml`보다
   우선하므로 그대로 두면 기존 ruff 설정이 조용히 무시됩니다.
2. ruff를 dev 의존성으로 추가합니다: `uv add --dev ruff`.
   훅은 ruff를 PATH와 프로젝트 환경에서 찾고, 둘 다 없으면 **아무 일도 하지 않고 조용히 끝납니다**.
   이 단계를 빼먹으면 포맷 훅이 영원히 무음 no-op이 됩니다.
3. `CLAUDE.md`의 **Section A** (빌드 명령, 아키텍처 규칙)를 해당 레포에 맞게 교체합니다.
   **Section B**는 수정하지 않습니다.
4. `.claude/settings.json`의 permissions에서 명령어를 레포의 빌드 도구에 맞게
   바꿉니다 (`uv run pytest` → `npm test` 등). 규칙은 `Bash(...)`와 `PowerShell(...)`
   쌍으로 되어 있습니다. 두 도구의 권한 네임스페이스가 별개라 한쪽만 고치면 Windows에서
   차단·허용이 풀립니다. 항상 쌍으로 수정하세요.
5. Python이 아닌 레포라면 `.claude/hooks/format.py`를 해당 언어의 포매터로
   교체하거나 훅을 제거합니다.
6. ML 레포가 아니라면 `.claude/skills/mr/template.md`의 ML 전용 체크리스트
   블록을 삭제합니다.

## 주의: ruff는 Markdown 안의 Python 코드도 고칩니다

ruff 0.16.0부터 `ruff format`은 `.md` 파일 안의 Python 코드 블록까지 재작성하고,
`.md`는 기본 탐색 대상에 포함됩니다. 그래서 `ruff format .` 한 번이면
`.claude/rules/code-style.md` 같은 **규칙 문서가 조용히 수정**됩니다. ruff 0.16.8에서 재현 확인했습니다.

이 템플릿은 두 겹으로 막습니다.

- `ruff.toml`의 `extend-exclude = ["*.md"]`로 ruff가 Markdown에 접근하지 못하게 합니다.
- `CLAUDE.md` Section 1이 명령을 **검증(읽기 전용)** 과 **변경(사람이 실행)** 으로 나눠서,
  Claude가 검증 단계에 `ruff format .`을 돌리지 않게 합니다.

CLI 플래그 `--exclude "*.md"`는 **동작하지 않습니다**. 설정 파일에 넣어야 합니다.

## 원칙

- **강제할 수 있는 것은 문서가 아니라 훅으로**: 포맷팅은 PostToolUse 훅이 실행하므로 잊힐 수 없습니다.
- **검증은 고치지 않는다**: Claude가 돌리는 명령은 읽기 전용이고, 레포 전체를 재작성하는 명령은 사람이 실행합니다. 이렇게 하면 작업과 무관한 파일이 diff에 섞이지 않습니다.
- **포매터에는 항상 파일 하나만 넘긴다**: 훅은 방금 수정한 파일 한 개만 포맷합니다. 디렉토리나 `.`을 넘기지 않습니다.
- **경로 참조는 정확하게**: CLAUDE.md가 가리키는 파일 경로는 대소문자까지 실제 파일과 일치해야 합니다 (Linux/macOS 호환).
- **팀 공통은 `settings.json`, 개인 취향은 `settings.local.json`**.
- **권한 규칙은 셸별로 따로 산다**: Claude Code의 `Bash` 도구와 Windows의 `PowerShell` 도구는 권한 네임스페이스가 다릅니다. `Bash(git commit:*)`만 막으면 PowerShell로는 그대로 커밋됩니다. 그래서 모든 allow·deny 규칙을 두 도구에 쌍으로 두었습니다.
- **커밋·푸시는 사람이**: `settings.json`이 `git commit`/`git push`를 두 셸 모두에서 deny합니다. Claude는 대신 `.claude/HANDOFF.md`(작업 이력·확인점·커밋 추천[무엇을/왜 지금/타입/메시지]·상세 기록)를 덮어써서 작업을 마무리하고, 사용자는 이 파일을 보고 커밋하거나 파일에 직접 피드백을 남깁니다. 다음 작업 시작 시 Claude가 그 피드백을 먼저 읽습니다.
