# tests/test_outputs.py
"""
Verifies the report the agent writes to /app/out.json against the raw
access.log. Each test maps to exactly one numbered success criterion
in instruction.md — see the docstring on each test.
"""
import json
import re
from pathlib import Path

REPORT_PATH = Path("/app/out.json")
LOG_PATH = Path("/app/access.log")

# Apache common/combined log format: 'IP - - [ts] "METHOD path HTTP/x" status size'
LOG_LINE_RE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[.*?\] "(?P<method>\S+) (?P<path>\S+) \S+" \d+ \S+'
)


def _parse_log():
    lines = [line for line in LOG_PATH.read_text().splitlines() if line.strip()]
    ips, paths = [], []
    for line in lines:
        match = LOG_LINE_RE.match(line)
        assert match, f"log line did not match expected Apache format: {line!r}"
        ips.append(match.group("ip"))
        paths.append(match.group("path"))
    return lines, ips, paths


def _load_report():
    assert REPORT_PATH.exists(), "no report found at /app/out.json"
    return json.loads(REPORT_PATH.read_text())


def test_report_exists_at_declared_path():
    """Criterion 1: A JSON report exists at /app/out.json."""
    assert REPORT_PATH.exists(), "expected report at /app/out.json"
    json.loads(REPORT_PATH.read_text())  # must be valid JSON, not just present


def test_total_requests_matches_log():
    """Criterion 2: total_requests equals the number of requests in access.log."""
    lines, _, _ = _parse_log()
    report = _load_report()
    assert "total_requests" in report, "missing total_requests key"
    assert report["total_requests"] == len(lines), (
        f"expected {len(lines)} total_requests, got {report['total_requests']}"
    )


def test_unique_clients_matches_log():
    """Criterion 3: unique_clients equals the number of distinct client IPs in access.log."""
    _, ips, _ = _parse_log()
    report = _load_report()
    assert "unique_clients" in report, "missing unique_clients key"
    expected = len(set(ips))
    assert report["unique_clients"] == expected, (
        f"expected {expected} unique_clients, got {report['unique_clients']}"
    )


def test_top_path_matches_log():
    """Criterion 4: top_path equals the most frequently requested path in access.log."""
    _, _, paths = _parse_log()
    report = _load_report()
    assert "top_path" in report, "missing top_path key"
    counts = {}
    for p in paths:
        counts[p] = counts.get(p, 0) + 1
    expected_top = max(counts, key=counts.get)
    assert report["top_path"] == expected_top, (
        f"expected top_path {expected_top!r}, got {report['top_path']!r}"
    )