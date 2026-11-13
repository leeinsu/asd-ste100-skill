#!/usr/bin/env python3
"""Query the bundled Korean aviation dictionary without changing its contents."""

import argparse
from collections import Counter, defaultdict
import contextlib
import csv
import io
import json
from pathlib import Path
import re
import sys
import tempfile
import unicodedata


COLUMNS = {
    "순번": "id",
    "영문": "english",
    "한글용어": "korean",
    "약어": "abbreviation",
    "해설": "definition",
    "분야": "domain_label",
    "분야코드": "domain_code",
}
DOMAINS = ("MAINT", "OPER", "SAFETY", "LOGIS")
DEFAULT_CSV = Path(__file__).resolve().parent.parent / "kor_dic.csv"


def comparison_key(value):
    return " ".join(unicodedata.normalize("NFC", value).split()).casefold()


def checked_lines(source):
    # csv.reader accepts bare quotes in unquoted fields, even with strict=True.
    quoted = False
    field_start = True
    for number, line in enumerate(source, start=1):
        for character in line:
            if character == '"':
                if not quoted and not field_start:
                    raise ValueError(f"CSV line {number}: quote inside an unquoted field")
                quoted = not quoted
            elif not quoted:
                field_start = character in ",\r\n"
        yield line


def read_rows(path):
    rows = []
    identifiers = set()
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(checked_lines(source), strict=True)
        if next(reader, None) != list(COLUMNS):
            raise ValueError("CSV header must contain these columns in order: " + ", ".join(COLUMNS))
        for number, cells in enumerate(reader, start=2):
            if len(cells) != len(COLUMNS):
                raise ValueError(f"CSV record {number}: expected {len(COLUMNS)} fields, got {len(cells)}")
            row = dict(zip(COLUMNS.values(), cells))
            missing = [field for field, value in row.items() if field != "abbreviation" and not value.strip()]
            if missing:
                raise ValueError(f"CSV record {number}: missing values for {', '.join(missing)}")
            if not re.fullmatch(r"[+-]?[0-9]+", row["id"].strip()):
                raise ValueError(f"CSV record {number}: id must be an integer")
            identifier = int(row["id"])
            if identifier in identifiers:
                raise ValueError(f"CSV record {number}: duplicate id {row['id']!r}")
            if row["domain_code"] not in DOMAINS:
                raise ValueError(f"CSV record {number}: unknown domain code {row['domain_code']!r}")
            identifiers.add(identifier)
            rows.append(row)
    return rows


def query_rows(rows, query, domain):
    key = comparison_key(query)
    matches = [
        row for row in rows
        if (domain is None or row["domain_code"] == domain)
        and any(comparison_key(row[field]) == key for field in ("english", "korean", "abbreviation"))
    ]
    return {"query": query, "domain": domain, "count": len(matches), "rows": matches}


def validation_summary(rows):
    keys = Counter()
    translations = defaultdict(set)
    for row in rows:
        key = (comparison_key(row["english"]), row["domain_code"])
        keys[key] += 1
        translations[key].add(comparison_key(row["korean"]))
    return {
        "row_count": len(rows),
        "missing_values": {
            field: sum(not row[field].strip() for row in rows) for field in COLUMNS.values()
        },
        "duplicate_keys": sum(count > 1 for count in keys.values()),
        "conflicting_translations": sum(len(values) > 1 for values in translations.values()),
    }


def selftest():
    def run(arguments, expected_status=0):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                status = main(arguments)
            except SystemExit as error:
                status = error.code
        assert status == expected_status, (arguments, status, stderr.getvalue())
        if status:
            assert stderr.getvalue(), arguments
            assert not stdout.getvalue(), arguments
            return None
        assert not stderr.getvalue(), stderr.getvalue()
        return json.loads(stdout.getvalue())

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "terms.csv"
        data = [
            ["01", " ADAPTER ", "어댑터", "ADAPTER", 'First, keep "this".\nThen read it.', "정비·감항", "MAINT"],
            ["2", "adapter", "연결기", "", "Run no commands: $(touch forbidden)", "정비·감항", "MAINT"],
            ["3", "AIR  DATA", "항공 자료", "AC", "A separate domain.", "운항·관제", "OPER"],
            ["4", "CAFE\u0301", "카페", "", "A Unicode example.", "운항·관제", "OPER"],
            ["5", "Adapter", "다른 분야", "", "A separate record.", "운항·관제", "OPER"],
        ]

        def write(records=data, header=None):
            with path.open("w", encoding="utf-8-sig", newline="") as target:
                writer = csv.writer(target)
                writer.writerow(list(COLUMNS) if header is None else header)
                writer.writerows(records)

        write()
        original = path.read_bytes()
        base = ["--csv", str(path)]
        result = run(base + ["--query", "adApTer", "--domain", "MAINT"])
        assert result["query"] == "adApTer" and result["domain"] == "MAINT"
        assert result["count"] == 2
        assert result["rows"] == [dict(zip(COLUMNS.values(), record)) for record in data[:2]]
        assert [row["id"] for row in run(base + ["--query", "ADAPTER"])["rows"]] == ["01", "2", "5"]
        assert run(base + ["--query", "air\tdata"])["rows"][0]["id"] == "3"
        assert run(base + ["--query", "AC"])["rows"][0]["id"] == "3"
        assert run(base + ["--query", unicodedata.normalize("NFD", "어댑터")])["rows"][0]["id"] == "01"
        assert run(base + ["--query", "café"])["rows"][0]["english"] == "CAFE\u0301"
        for query in ("absent", "어댑터는", "AIR-DATA"):
            assert run(base + ["--query", query]) == {"query": query, "domain": None, "count": 0, "rows": []}
        summary = run(base + ["--validate"])
        assert summary == {
            "row_count": 5,
            "missing_values": {field: 3 if field == "abbreviation" else 0 for field in COLUMNS.values()},
            "duplicate_keys": 1,
            "conflicting_translations": 1,
        }
        assert path.read_bytes() == original
        for arguments in (
            [], ["--query", " "], ["--query", "ADAPTER", "--domain", "OTHER"],
            ["--validate", "--domain", "MAINT"], ["--query", "ADAPTER", "--validate"],
            ["--selftest", "--domain", "MAINT"], ["--selftest", "--csv", str(path)],
            ["--query", "ADAPTER", "--unknown"],
            ["--csv", str(Path(directory) / "absent.csv"), "--query", "ADAPTER"],
            ["--csv", directory, "--validate"],
        ):
            run(arguments, 2)
        assert path.read_bytes() == original
        for records, header in (
            (data + [["1"] + data[1][1:]], None),
            ([data[0][:-1]], None),
            ([data[0] + ["extra"]], None),
            ([[]], None),
            (data, list(COLUMNS)[:-1]),
            (data, ["순번"] * len(COLUMNS)),
        ):
            write(records, header)
            invalid = path.read_bytes()
            run(base + ["--validate"], 2)
            assert path.read_bytes() == invalid
        for index, value in ((0, "1.5"), (0, "1_0"), (1, " "), (2, ""), (4, ""), (5, ""), (6, "OTHER")):
            record = data[0].copy()
            record[index] = value
            write([record])
            run(base + ["--validate"], 2)
        for content in (b"", b"\xff", (",".join(COLUMNS) + '\n1,"unterminated').encode()):
            path.write_bytes(content)
            run(base + ["--validate"], 2)
            assert path.read_bytes() == content
        for term in ('ADAP"TER', 'ADAPTER"'):
            content = (",".join(COLUMNS) + f"\n1,{term},어댑터,,해설,정비,MAINT\n").encode()
            path.write_bytes(content)
            run(base + ["--validate"], 2)
            assert path.read_bytes() == content
        write([])
        assert run(base + ["--validate"])["row_count"] == 0
        write()
        path.write_bytes(path.read_bytes()[3:])
        assert run(base + ["--validate"])["row_count"] == 5
    return {"selftest": "ok"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--csv", type=Path, help="CSV path. The default is the bundled kor_dic.csv.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--query", help="Match a complete English term, Korean term, or abbreviation.")
    mode.add_argument("--validate", action="store_true", help="Validate the CSV and print its counts.")
    mode.add_argument("--selftest", action="store_true", help="Run the built-in tests.")
    parser.add_argument("--domain", choices=DOMAINS, help="Filter query results by domain code.")
    args = parser.parse_args(argv)
    if args.domain and args.query is None:
        parser.error("--domain requires --query")
    if args.selftest and args.csv is not None:
        parser.error("--selftest does not use --csv")
    if args.query is not None and not comparison_key(args.query):
        parser.error("--query must contain a non-whitespace character")
    if args.selftest:
        result = selftest()
    else:
        try:
            rows = read_rows(args.csv if args.csv is not None else DEFAULT_CSV)
            result = validation_summary(rows) if args.validate else query_rows(rows, args.query, args.domain)
        except (OSError, UnicodeError, csv.Error, ValueError) as error:
            print(f"ko-terms: {error}", file=sys.stderr)
            return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
