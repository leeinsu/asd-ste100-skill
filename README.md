# ASD-STE100 한국어 스킬

한국어 대화와 문서를 명확하게 작성하고 수정하는 `asd-ste100-ko` 스킬이다.
조건, 예외, 불확실성과 요구 강도를 보존하면서 문장을 정리한다.
한국어 작성 규칙과 항공용어 6,724개를 담은 `kor_dic.csv`를 함께 제공한다.
영어 스킬 없이 독립적으로 사용할 수 있다.

## 설치

현재 한국어 구현은 `feat/korean-skill` 브랜치에 있다.
아래 방법 중 사용할 도구에 맞는 방법을 선택한다.
사전 조회에는 Python 3가 필요하다. 추가 Python 패키지는 필요하지 않다.

Codex에서 사용하려면 다음 명령을 실행한다.

```sh
mkdir -p ~/.codex/skills
git clone --branch feat/korean-skill https://github.com/leeinsu/asd-ste100-skill.git ~/.codex/skills/asd-ste100-ko
```

`CODEX_HOME`을 별도로 지정했다면 그 폴더의 `skills/asd-ste100-ko`에 설치한다.
설치 후 Codex를 다시 시작한다.

Claude Code에서 사용하려면 다음 명령을 실행한다.

```sh
mkdir -p ~/.claude/skills
git clone --branch feat/korean-skill https://github.com/leeinsu/asd-ste100-skill.git ~/.claude/skills/asd-ste100-ko
```

플러그인 이름은 `asd-ste100-ko`, 마켓플레이스 이름은 `asd-ste100-ko-skill`이다.
플러그인은 루트의 `SKILL.md`를 읽도록 [경로를 지정한다](.claude-plugin/plugin.json).
경로 설정은 [Claude Code 플러그인 규격](https://code.claude.com/docs/en/plugins-reference)을 따른다.

## 사용

스킬 이름과 작업을 함께 요청한다.

```text
asd-ste100-ko로 이 설계를 한국어로 설명해 줘.
asd-ste100-ko로 이 문장을 다듬어 줘. 조건과 불확실성은 유지해 줘.
asd-ste100-ko로 한국어 검토자가 읽을 커밋 메시지와 PR 설명을 작성해 줘.
```

새 글은 요청한 형식으로 작성한다. 수정 작업은 수정문만 기본으로 제공한다.
수정 이유가 필요하면 원문·수정문·적용 규칙 비교를 요청한다.
자세한 사용 형태는 [예시](examples/before-after-ko.md)에서 확인한다.

### 영어 스킬과 함께 쓰는 경우

혼합 운용은 선택 사항이다.
사용자의 명시적인 언어 지정과 상위 지침이 우선한다.

| 사용 상황 | 스킬 |
| --- | --- |
| 한국어 사용자와 대화·설계 | `asd-ste100-ko` |
| 한국어 사용자가 검토할 커밋·PR 메시지와 문서 | `asd-ste100-ko` |
| 한국어 사용자가 포함된 팀에 공유할 문서 | `asd-ste100-ko` |
| LLM 간 대화·작업 지시·내부 문서 등 그 외 작업 | 영어 `asd-ste100` |

## 사전 조회

스킬 폴더에서 다음 명령을 실행한다.
다른 폴더에서는 스크립트의 절대 경로를 사용한다.
도구는 설치본에 포함된 CSV를 기본으로 읽는다.

```sh
python3 scripts/ko-terms.py --query ADAPTER --domain MAINT
python3 scripts/ko-terms.py --query AC
python3 scripts/ko-terms.py --validate
```

`ADAPTER` 조회는 248·249번 항목을 모두 반환한다.
`AC` 조회는 6·344·806·823번 항목을 반환한다.
결과는 JSON이다. 조회 방식과 오류 처리는 [사전 안내](references/dictionary.md)에 정의한다.

사전 출처는 [공공데이터포털의 국토교통부 항공용어사전](https://www.data.go.kr/data/15052307/fileData.do)이다.
자료 버전은 `국토교통부_항공용어사전_20251231`, 기준일은 2025-12-31이다.
포털 등록일·수정일은 2026-02-26이다.
포털 이용허락범위는 "이용허락범위 제한 없음"이다.

## 검증과 유지보수

```sh
python3 scripts/ko-terms.py --selftest
python3 scripts/ste-lint.py --selftest
```

한국어 의미 보존 평가는 [평가 사례](tests/korean-rewrite-cases.json)를 사용한다.
사례의 필수 의미와 금지 변경을 기준으로 결과를 검토한다.
허용 예시와 문장이 다르다는 이유만으로 실패로 판정하지 않는다.
2026-11-13 평가에서 16개 사례가 의미 보존 검토를 통과했다.
입력·출력·검토자와 평가 한계는 [검토 기록](tests/korean-rewrite-review.json)에 남겼다.

영어 검사기, [영어 규칙](references/writing-rules.md), [영어 예시](examples/before-after.md)는 원본을 유지한다.
`examples/linter-edge-cases.md`는 의도적으로 오류 두 건을 포함한 영어 검사기 테스트 자료다.
영어 검사기로 한국어의 문법이나 의미 보존을 판정하지 않는다.

## 원본과 라이선스

[danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill)의 버전 0.4.0을 기반으로 한다.
원본 분석 기준은 `d5caf54905eac776e9bb3a247be84153701ff4f8`이다.
구현 기준은 [한국어 설계서](docs/korean-adaptation-design.md)에 기록한다.
스킬 코드와 문서는 [MIT 라이선스](LICENSE)를 유지한다.
사전 데이터의 출처와 이용허락범위는 위의 포털 표기를 따른다.

이 스킬은 ASD-STE100 원칙을 한국어에 적용한 비공식 지침이다.
정식 ASD-STE100 적합성을 주장하지 않는다.
