from log_parser import analyze_log, retry_timestamps, log_by_trace
import sys
import os

# Add the project root to sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_path not in sys.path:
    sys.path.insert(0, project_path)


def test_retry_interval_counts():
    test_log = """\
2025-06-18T09:00:01.900Z [INFO] Retry 1 in 3 seconds
2025-06-18T09:00:05.150Z [INFO] Retry 2 in 5 seconds
2025-06-18T09:00:10.200Z [INFO] Retry 3 in 7 seconds
2025-06-18T09:00:17.300Z [INFO] Trace ID: abc123
"""

    os.makedirs("tests/logs", exist_ok=True)
    log_path = "tests/logs/test_log.txt"
    with open(log_path, "w") as f:
        f.write(test_log)

    log_by_trace.clear()
    retry_timestamps.clear()
    analyze_log(log_path)

    assert "abc123" in retry_timestamps
    assert len(retry_timestamps["abc123"]) == 3


def test_trace_grouping():
    test_log = """\
2025-06-18T09:00:01.900Z [INFO] Retry 1 in 3 seconds
2025-06-18T09:00:17.300Z [INFO] Trace ID: abc123
2025-06-18T09:01:01.900Z [INFO] Retry 1 in 2 seconds
2025-06-18T09:01:08.250Z [INFO] Trace ID: def456
"""

    log_path = "tests/logs/test_log_2.txt"
    with open(log_path, "w") as f:
        f.write(test_log)

    log_by_trace.clear()
    retry_timestamps.clear()
    analyze_log(log_path)

    assert "abc123" in log_by_trace
    assert "def456" in log_by_trace
    assert len(retry_timestamps["abc123"]) == 1
    assert len(retry_timestamps["def456"]) == 1
