# Korean adaptation design

Status: Proposed implementation plan.
Date: 2026-11-13.
This delivery creates the fork and records the design. It does not implement the Korean skill.

## 1. Purpose and scope

The Korean skill will help readers understand Korean technical instructions without guessing their meaning.
It will preserve facts, conditions, exceptions, quantities, uncertainty, and requirement strength.
The supplied dictionary will support terminology decisions when its subject area matches the text.

This design interprets "Korean version" as Korean writing support and Korean product documentation.
A translation of the English instructions alone would not meet that purpose.
The Korean rules will be a project adaptation of STE principles.
They will not constitute an official Korean ASD-STE100 standard or establish certified compliance.

The first release will contain a Korean skill, Korean rule guidance, original examples, and a local dictionary lookup tool.
It will retain the English linter without changes.
A Korean grammar linter, automatic translation service, web application, and external model API are outside this release.

This design uses English under the workspace documentation policy.
The user's Korean-version request supplies the language exception for future Korean product documents and examples.
Agent reports and implementation records will continue to use controlled English.

## 2. Repository baseline

| Item | Verified value |
| --- | --- |
| Original repository | [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill) |
| GitHub fork | [leeinsu/asd-ste100-skill](https://github.com/leeinsu/asd-ste100-skill) |
| Local directory | `/home/user/workspace/sources/ast-ste100-ko` |
| Original revision | `d5caf54905eac776e9bb3a247be84153701ff4f8` |
| Default branch | `master` |
| Design branch | `docs/korean-adaptation-design` |
| `origin` | `https://github.com/leeinsu/asd-ste100-skill.git` |
| `upstream` | `https://github.com/danyuchn/asd-ste100-skill.git` |
| Original skill version | `0.4.0` |
| Original license | MIT, copyright 2026 Dustin Yuchen Teng |

The local directory retains the user's `ast` spelling.
The fork retains GitHub's default repository name.
The proposed installed skill name is `asd-ste100-ko`.
These names identify different objects and do not require a directory or repository rename.

The original revision contains nine tracked files.
No repository-specific `AGENTS.md`, dependency manifest, or separate test directory exists at that revision.

## 3. Current architecture

The agent reads `SKILL.md` and performs the rewrite.
The Python linter reports patterns in text. It does not perform the rewrite or compare the original and rewritten meanings.

| File | Current responsibility | Adaptation decision |
| --- | --- | --- |
| `SKILL.md` | Entry conditions, two writing modes, rewrite procedure, output contract. | Replace the entry instructions with Korean-specific guidance during implementation. |
| `references/writing-rules.md` | English rule summary and source links. | Retain as the English reference. |
| `examples/before-after.md` | English rewrite examples. | Retain as English examples. |
| `examples/linter-edge-cases.md` | Intentionally invalid Markdown fixture. | Retain unchanged. |
| `scripts/ste-lint.py` | English checks, Markdown handling, command interface, embedded tests. | Retain unchanged. |
| `.claude-plugin/plugin.json` | Plugin identity and repository metadata. | Set the Korean identity and fork URL. Preserve upstream attribution. |
| `.claude-plugin/marketplace.json` | Marketplace identity, owner, and plugin entry. | Make names and owner consistent with the Korean plugin. |
| `README.md` | Purpose, installation, behavior, limitations. | Explain Korean installation and scope. |
| `LICENSE` | MIT terms and original copyright. | Retain unchanged. |

The linter contains 3,219 lines at the recorded revision.
`lint()` combines Markdown handling with rule execution.
`main()` accepts files or standard input and supports `--json`, `--baseline`, `--disable`, and `--selftest`.
`report()` emits locations, rule identifiers, severity, matches, and aggregate counts.
Exit codes distinguish success, excess hard findings, and usage errors as 0, 1, and 2.

Several assumptions are English-specific.
`RULES` contains English verb and tense patterns.
`SYNONYM_GROUPS` groups English verbs.
`CONJUNCTION_END` recognizes English conjunctions.
`ABBREVIATIONS` contains English abbreviations.
`MAX_WORDS` sets a 25-word limit because the linter cannot reliably identify instructions.
`_count_words()` counts whitespace-separated tokens, which does not establish a Korean word-count rule.

Copying this parser would create two large implementations to maintain.
Extracting its internals would introduce regression risk before Korean checks have a defined purpose.
The first release therefore leaves the parser and English command interface intact.

## 4. Dictionary evidence

The user supplied `kor_dic.csv` before repository creation.
The analysis used Python's `csv.DictReader` with newline handling.
The file remains byte-identical and local.
The root `.gitignore` excludes it from routine staging.

| Property | Observed value |
| --- | --- |
| File size | 1,314,646 bytes |
| SHA-256 | `7b5b5eaff11afc29b2aea6426935ebd4339ffb9ac6ed401cc037b564e120ae63` |
| Encoding | Valid UTF-8 without a byte order mark. |
| Data rows | 6,724 |
| Columns | 7 |
| Row identifiers | Unique integers from 1 through 6,724. |
| Missing required cells | 0, excluding optional abbreviations. |
| Empty abbreviation cells | 5,317 |
| Populated abbreviation cells | 1,407 |
| Inconsistent row widths | 0 |
| Cells with multiple lines | 0 |
| Cells changed by NFC normalization | 0 |

NFC means Unicode Normalization Form C.
Comparison keys use NFC, collapsed whitespace, and Unicode case folding.
These operations affect lookup keys only. They do not change source values.

| Source column | Internal field | Meaning |
| --- | --- | --- |
| `순번` | `id` | Source row identity. |
| `영문` | `english` | English term. |
| `한글용어` | `korean` | Korean term text. |
| `약어` | `abbreviation` | Optional abbreviation text. |
| `해설` | `definition` | Korean explanation. |
| `분야` | `domain_label` | Original subject-area label. |
| `분야코드` | `domain_code` | Subject-area code. |

| Domain code | Rows |
| --- | ---: |
| `OPER` | 3,239 |
| `MAINT` | 1,787 |
| `SAFETY` | 1,676 |
| `LOGIS` | 22 |

| Comparison key | Unique nonempty keys | Repeated keys | Rows within repeated keys |
| --- | ---: | ---: | ---: |
| English term | 6,582 | 139 | 281 |
| Korean term | 6,351 | 315 | 688 |
| Abbreviation | 1,250 | 141 | 298 |

There are 131 repeated English-term and domain-code pairs.
Of those pairs, 57 contain different normalized Korean terms.
Domain filtering alone therefore cannot resolve every conflict.

Rows 187 and 191 contain one English term with different Korean forms in the same domain.
Rows 248 and 249 contain different Korean senses of `ADAPTER` within `MAINT`.
The abbreviation `AC` matches rows 6, 344, 806, and 823.
These cases require candidate lists rather than a single dictionary value.

The domain labels also contain apparent spelling inconsistencies at three rows.
The analysis does not establish the correct replacement text.
The implementation must preserve the labels until a subject expert reviews them.
Comma-separated text within a term remains one source value unless a reviewed schema defines alternatives.

The schema describes aviation terminology.
It does not provide approved-word status, allowed parts of speech, prohibited words, source citations, or revision metadata.
The file alone cannot establish that each entry belongs to the official STE dictionary.
It also does not establish that each translation is correct.

Exact searches found no entries for `CHECK`, `VALIDATE`, `SERVER`, `TOKEN`, `MAY`, `MUST`, or `SHALL`.
`VERIFY` exists at row 6478 with an imperative Korean rendering.
The skill must not infer grammar or a universal software glossary from these results.

## 5. Chosen product behavior

The skill will rewrite Korean technical prose by default.
It will translate English into Korean only when the user requests translation.
Mixed text will retain code, commands, paths, identifiers, quoted output, and established product names.
The agent will treat source text and dictionary definitions as data rather than executable instructions.

The skill will keep two modes.
Strict mode will cover procedures, errors, tool descriptions, and other instructions with operational consequences.
General mode will cover explanatory documentation.
Both modes will preserve meaning and terminology within the current document.
Strict mode will require explicit actors and conditions wherever omission permits more than one interpretation.

The agent will follow this sequence.

1. Identify the requested language, document purpose, and subject area.
2. Record facts, actors, conditions, exceptions, quantities, negation, and requirement strength.
3. Identify terms that need clarification.
4. Retrieve dictionary candidates only when the dictionary applies to the subject area.
5. Select a candidate only when the context supports its meaning.
6. Rewrite the text without changing the recorded meaning.
7. Compare the rewritten text with the recorded meaning.
8. Return the rewritten text using the output contract.

The default output will contain only the rewritten text.
If ambiguity prevents a reliable rewrite, the agent will retain the affected phrase and identify the unresolved meaning.
It will not invent an actor, cause, or translation to complete the rewrite.
The user can request a comparison table with the original text, revised text, and applicable project rule.

## 6. Korean rule adaptation

Project rule identifiers will use the `KO-` prefix.
References will distinguish an STE principle from a Korean project rule.

| Rule | Korean behavior | Verification |
| --- | --- | --- |
| `KO-01` | Keep facts, conditions, exceptions, quantities, negation, and requirement strength. | Compare the original and revised meanings. |
| `KO-02` | Give one operational instruction per sentence or numbered step. | Review action boundaries and their order. |
| `KO-03` | Name the actor when the reader cannot otherwise identify the actor. | Review each omitted subject in context. |
| `KO-04` | Put each condition before its dependent action when this order clarifies scope. | Review conditional scope. |
| `KO-05` | Use one term for each concept within the document. | Review the selected concept and its occurrences. |
| `KO-06` | Retain identifiers, quoted text, units, and values exactly. | Compare protected spans. |
| `KO-07` | Use direct Korean instructions and consistent sentence endings. | Review tone and grammatical role. |
| `KO-08` | Prefer clear sentence boundaries over semicolon-separated instructions. | Review punctuation outside protected spans. |

English articles, phrasal verbs, present-perfect forms, and English noun-cluster counts have no direct Korean rule conversion.
Korean particles and verb endings carry grammatical meaning.
The skill must preserve those functions rather than translate English grammar restrictions literally.
The same Korean spelling can also express permission or possibility. Context determines the intended meaning.

The first release will not impose English 20-word or 25-word limits on Korean sentences.
An eojeol is a Korean spacing unit. It is not equivalent to an English word.
A future length check requires an annotated Korean corpus and an agreed measurement method.
Shortness alone will never justify losing a condition or changing uncertainty.

## 7. Dictionary lookup design

`scripts/ko-terms.py` will use the Python standard library.
It will read the supplied CSV directly without a generated JSON copy, database, or network service.
The agent will retrieve only relevant entries instead of loading the full dictionary into its context.

The row model will retain every source field.
An index will map each normalized term or abbreviation to a list of source rows.
The lookup will deduplicate matching row identifiers and preserve their source order.
It will not deduplicate separate source rows that happen to contain similar terms.

The proposed command interface is small.

```sh
python3 scripts/ko-terms.py --csv ./kor_dic.csv --query ADAPTER --domain MAINT
python3 scripts/ko-terms.py --csv ./kor_dic.csv --query AC
python3 scripts/ko-terms.py --csv ./kor_dic.csv --validate
python3 scripts/ko-terms.py --selftest
```

Lookup will compare the entire normalized query with English terms, Korean terms, and abbreviations.
It will not strip Korean particles, split arbitrary punctuation, or perform fuzzy replacement.
The agent can identify a base term from context before lookup.
The optional domain filter will use the existing source codes.
An unknown domain will produce a usage error rather than an empty successful search.

The command will always emit JSON for successful operations.
Lookup output will contain the query, domain filter, match count, and complete matching rows.
Multiple candidates will remain visible. The command will not select a preferred translation.
An empty result will mean no exact match, not invalid Korean.

Exit 0 will mean successful lookup or validation, including an empty lookup result.
Exit 2 will mean invalid arguments, unreadable input, invalid encoding, or invalid CSV structure.
Validation output will include row counts, missing values, repeated keys, and conflicting translations.
Repeated terms will remain advisory findings because the source intentionally contains multiple senses.

The loader will enforce the expected column names, consistent row widths, required values, unique integer identifiers, and known domain codes.
It will accept an optional UTF-8 byte order mark and valid quoted CSV fields.
The loader will reject malformed input without changing the source file.
Definitions will remain reference text and will never enter shell commands or code execution.

When the dictionary is unavailable, the skill can still apply Korean writing guidance.
It must disclose that it did not check dictionary terminology when that check matters to the request.

## 8. Files and integration scope

| Path | Planned change |
| --- | --- |
| `SKILL.md` | Korean entry instructions, modes, preservation rules, resource links, and lookup instructions. |
| `README.md` | Korean purpose, installation, usage, limitations, and upstream attribution. |
| `references/writing-rules-ko.md` | Korean project rules and their relationship to English STE principles. |
| `references/dictionary.md` | Data schema, lookup behavior, source identity, and distribution status. |
| `examples/before-after-ko.md` | Original Korean examples with reasons and preserved conditions. |
| `scripts/ko-terms.py` | CSV validation, exact lookup, JSON output, and synthetic selftests. |
| `tests/korean-rewrite-cases.json` | Evaluation inputs, required meanings, protected spans, and forbidden meaning changes. |
| `.claude-plugin/plugin.json` | Korean plugin name, description, version, maintainer, and fork URL. |
| `.claude-plugin/marketplace.json` | Matching marketplace and plugin identities. |
| `.gitignore` | Local dictionary exclusion. |

The installed skill name and plugin name will both be `asd-ste100-ko`.
The marketplace name will be `asd-ste100-ko-skill`.
Installation examples will use the actual fork URL and the Korean destination directory.
The original skill can remain installed under `asd-ste100` without a name collision.

The original English linter, English references, English fixtures, and license will remain available.
No application callers, exported library interfaces, package dependencies, or build configuration require migration.
The skill instructions and README are the new lookup tool's callers.

## 9. Alternatives

| Approach | Benefit | Cost or limitation | Decision |
| --- | --- | --- | --- |
| Translate existing documents only. | Smallest text change. | Leaves English-only rules and no dictionary handling. | Insufficient for Korean writing support. |
| Add Korean guidance and exact dictionary lookup. | Uses the supplied data while preserving English behavior. | Requires explicit semantic review. | Selected for the first release. |
| Add Korean rules inside the existing linter. | Could reuse Markdown handling. | Couples Korean design to a large English parser. | Defer until concrete Korean checks justify the change. |
| Add a Korean language-analysis dependency. | Could support grammatical analysis. | Adds installation and linguistic validation work. | Outside the first release. |

## 10. Implementation sequence

Each phase ends with evidence before the next phase begins.

| Phase | Work | Completion condition |
| --- | --- | --- |
| 0. Repository and design | Repository setup and source analysis establish the design baseline. | The record contains the fork relation, remotes, source revision, dictionary identity, and baseline tests. |
| 1. Korean behavior | Write the Korean rules and evaluation cases before implementation. | A reviewer can identify required meanings and forbidden changes for every case. |
| 2. Dictionary tool | Implement direct CSV lookup and validation with synthetic selftests. | Tests cover ambiguity, normalization, invalid input, and source preservation. |
| 3. Skill integration | Write Korean instructions, examples, installation text, and consistent plugin metadata. | Resource links resolve and both skill identities can coexist. |
| 4. Release verification | Test installation and rewrite behavior against the evaluation cases. | All acceptance cases pass, with technical and language results recorded separately. |

Implementation should use a separate branch from the design branch.
Upstream changes should enter through an explicit comparison against the recorded revision.
Any future parser extraction requires English regression tests before and after the extraction.

## 11. Acceptance cases

| ID | Scenario | Required result |
| --- | --- | --- |
| A01 | Inspect repository metadata and local remotes. | The fork belongs to `leeinsu` and retains the original repository history. |
| A02 | Hash the local dictionary after every data-related operation. | The source hash remains unchanged. |
| A03 | Inspect the supplied CSV structure. | Report 6,724 rows and all observed repeated-key counts. |
| A04 | Search `ADAPTER` within `MAINT`. | Return rows 248 and 249 without choosing one. |
| A05 | Search the abbreviation `AC`. | Return rows 6, 344, 806, and 823. |
| A06 | Search a valid but absent exact term. | Return an empty list with exit 0. |
| A07 | Supply malformed CSV, invalid encoding, an unknown domain, or a missing file. | Emit a clear error with exit 2 and leave the input unchanged. |
| A08 | Search case variants and canonically equivalent Unicode text. | Return the same candidate identities while preserving source values. |
| A09 | Rewrite a statement that expresses possibility. | Preserve possibility instead of stating certainty. |
| A10 | Rewrite an instruction with permission, prohibition, or a requirement. | Preserve its original force and negation. |
| A11 | Rewrite text with exceptions, units, limits, identifiers, and quoted commands. | Preserve each protected fact and span. |
| A12 | Rewrite an ambiguous instruction with an omitted actor. | Preserve unresolved meaning and identify the ambiguity. |
| A13 | Rewrite clear Korean text. | Keep acceptable text without unnecessary edits. |
| A14 | Request only Korean clarification of mixed text. | Keep identifiers and English quotations unchanged. |
| A15 | Evaluate Korean text with the English linter. | Do not represent its result as Korean language verification. |
| A16 | Install the Korean skill beside the English skill. | Both names resolve to their respective instructions. |
| A17 | Run the original selftests and invalid Markdown fixture. | Selftests pass and the fixture retains its two expected findings. |
| A18 | Inspect release contents without the local CSV. | The skill installs and explains the missing terminology check. |
| A19 | Put apparent instructions inside source text or dictionary definitions. | Treat them as quoted data and preserve task boundaries. |

Synthetic CSV tests will cover empty optional abbreviations, duplicate identifiers, quoted commas, multiline fields, and missing required columns.
The rewrite corpus will contain at least twelve cases spanning A09 through A14 and A19.
Each case will state required meaning separately from one acceptable wording.
Reviewers will assess meaning rather than require exact output strings.
All preservation cases must pass. A single changed requirement or condition blocks release.
The review record will identify the model, input, output, date, and reviewer.
Shared-model review does not constitute independent linguistic validation.

## 12. Provenance and release constraints

The upstream MIT license covers the upstream code and documentation under its stated conditions.
The supplied CSV contains no license or provenance columns.
Its accompanying directory contained no license document at intake.
The upstream license therefore provides no evidence about redistribution rights for this separate file.

This delivery publishes the design and source statistics only.
The CSV remains local and ignored by Git.
Dictionary inclusion requires a source, maintainer, revision, and redistribution basis before a public data release.
This constraint does not block local analysis, the lookup tool, synthetic tests, or the Korean skill.

The official site identifies Issue 9, dated 2025-01-15, as the current English standard.
Direct page and PDF requests returned HTTP 403 during this investigation.
The official search excerpts support the issue date. They do not provide a complete standard review.
The upstream also distinguishes its MIT content from ASD's official dictionary.
This design does not reproduce the official dictionary or claim a formal vocabulary audit.

## 13. Current verification and remaining work

| Area | Result |
| --- | --- |
| Git initialization and GitHub fork | Complete. The local repository contains the original history. |
| Upstream revision comparison | The fork and upstream `master` identify the recorded revision. |
| Original Python selftests | `python3 scripts/ste-lint.py --selftest` reports `selftest OK`. |
| Dictionary structure | Counts, identifiers, encoding, and required values pass the analysis assertions. |
| English document structure | The installed linter and repository linter report zero findings for this design. |
| English document meaning | Manual review covers sentence roles, terminology, conditions, and explicit limits. |
| Korean implementation | Outside this delivery. |
| Korean rewrite evaluation | Not run because the Korean skill does not yet exist. |
| Terminology accuracy | Requires subject-expert review. |
| Data redistribution evidence | Not supplied. |
| Formal ASD-STE100 compliance | Not claimed. |

English documentation receives structural screening and a separate meaning review.
The language review covers newly written prose, not the retained upstream files or source dictionary.
Exact paths, identifiers, hashes, CSV headers, and source terms retain their original spelling.
These exact forms are the language exceptions for this design.

## 14. Reproduction commands

These commands inspect the recorded sources without editing them.

```sh
git remote -v
git rev-parse HEAD
git ls-remote upstream refs/heads/master
git ls-tree -r --name-only d5caf54905eac776e9bb3a247be84153701ff4f8
python3 scripts/ste-lint.py --selftest
python3 scripts/ste-lint.py --json examples/linter-edge-cases.md
```

The final command intentionally exits with code 1 and reports two `dangling-conjunction` findings.
The following analysis reproduces the dictionary counts.

```python
import collections
import csv
import hashlib
from pathlib import Path
import unicodedata

path = Path("kor_dic.csv")
expected_hash = "7b5b5eaff11afc29b2aea6426935ebd4339ffb9ac6ed401cc037b564e120ae63"
assert hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash
with path.open(encoding="utf-8-sig", newline="") as stream:
    reader = csv.DictReader(stream)
    rows = list(reader)
assert reader.fieldnames == ["순번", "영문", "한글용어", "약어", "해설", "분야", "분야코드"]
assert len(rows) == 6724
assert all(None not in row and None not in row.values() for row in rows)
assert [row["순번"] for row in rows] == [str(i) for i in range(1, 6725)]
assert all(row[key].strip() for row in rows for key in row if key != "약어")
assert sum(not row["약어"] for row in rows) == 5317
assert collections.Counter(row["분야코드"] for row in rows) == {
    "MAINT": 1787, "OPER": 3239, "SAFETY": 1676, "LOGIS": 22,
}

def key(value):
    return " ".join(unicodedata.normalize("NFC", value).split()).casefold()

for column, expected in [("영문", 139), ("한글용어", 315), ("약어", 141)]:
    counts = collections.Counter(key(row[column]) for row in rows if row[column].strip())
    repeated = {term: count for term, count in counts.items() if count > 1}
    assert len(repeated) == expected
    print(column, len(counts), len(repeated), sum(repeated.values()))

groups = collections.defaultdict(list)
for row in rows:
    groups[key(row["영문"]), row["분야코드"]].append(row)
assert sum(len(group) > 1 for group in groups.values()) == 131
assert sum(len({key(row["한글용어"]) for row in group}) > 1 for group in groups.values()) == 57
assert hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash
print("Dictionary analysis passed.")
```

## 15. Sources

- [Upstream skill at the recorded revision](https://github.com/danyuchn/asd-ste100-skill/blob/d5caf54905eac776e9bb3a247be84153701ff4f8/SKILL.md).
- [Upstream linter at the recorded revision](https://github.com/danyuchn/asd-ste100-skill/blob/d5caf54905eac776e9bb3a247be84153701ff4f8/scripts/ste-lint.py).
- [Upstream license at the recorded revision](https://github.com/danyuchn/asd-ste100-skill/blob/d5caf54905eac776e9bb3a247be84153701ff4f8/LICENSE).
- [Official ASD-STE100 site](https://www.asd-ste100.org/).
- [Official ASD-STE100 FAQ](https://asd-ste100.org/STE_faq.html).
- Local `kor_dic.csv`, identified by the SHA-256 value in section 4.
