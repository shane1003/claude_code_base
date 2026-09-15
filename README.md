# Claude Code Base Template

새 레포에 복사해서 쓰는 Claude Code 공통 설정 템플릿입니다.

## 구조

```
CLAUDE.md                        # 프로젝트 지침 (Section A: 레포별 / Section B: 공통)
.claude/
├── settings.json                # 권한 allowlist + 훅 (팀 공유, 커밋 대상)
├── settings.local.json          # 개인 설정 (gitignore 대상, 필요 시 각자 생성)
├── HANDOFF.md                   # 작업 마무리 핸드오프 (매 작업마다 덮어쓰기, gitignore 대상)
├── hooks/
│   └── format.py                # 파일 수정 직후 ruff format 자동 실행 (PostToolUse)
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

1. `CLAUDE.md`와 `.claude/` 디렉토리를 통째로 복사합니다.
2. `CLAUDE.md`의 **Section A** (빌드 명령, 아키텍처 규칙)를 해당 레포에 맞게 교체합니다.
   **Section B**는 수정하지 않습니다.
3. `.claude/settings.json`의 permissions allowlist에서 명령어를 레포의
   빌드 도구에 맞게 바꿉니다 (`uv run pytest` → `npm test` 등).
4. Python이 아닌 레포라면 `.claude/hooks/format.py`를 해당 언어의 포매터로
   교체하거나 훅을 제거합니다.
5. ML 레포가 아니라면 `.claude/skills/mr/template.md`의 ML 전용 체크리스트
   블록을 삭제합니다.

## 원칙

- **강제할 수 있는 것은 문서가 아니라 훅으로**: 포맷팅은 PostToolUse 훅이 실행하므로 잊힐 수 없습니다.
- **경로 참조는 정확하게**: CLAUDE.md가 가리키는 파일 경로는 대소문자까지 실제 파일과 일치해야 합니다 (Linux/macOS 호환).
- **팀 공통은 `settings.json`, 개인 취향은 `settings.local.json`**.
- **커밋·푸시는 사람이**: `settings.json`이 `git commit`/`git push`를 deny합니다. Claude는 대신 `.claude/HANDOFF.md`(작업 이력·확인점·커밋 추천[무엇을/왜 지금/타입/메시지]·상세 기록)를 덮어써서 작업을 마무리하고, 사용자는 이 파일을 보고 커밋하거나 파일에 직접 피드백을 남깁니다. 다음 작업 시작 시 Claude가 그 피드백을 먼저 읽습니다.
