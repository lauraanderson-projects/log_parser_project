
import re
from collections import defaultdict
from datetime import datetime

# Patterns (shared with exporter and main)
trace_pattern = re.compile(r"Trace ID:\s*([a-z0-9\-]+)", re.IGNORECASE)
timestamp_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z")
retry_pattern = re.compile(r"Retry \d+ in \d+ seconds", re.IGNORECASE)

# Shared data structures
log_by_trace = defaultdict(list)
retry_timestamps = defaultdict(list)


def parse_timestamp(line):
    match = timestamp_pattern.match(line)
    if match:
        return datetime.strptime(match.group(), "%Y-%m-%dT%H:%M:%S.%fZ")
    return None


def analyze_log(file_path):
    current_trace_id = None
    buffer = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            buffer.append(line)

            # Check for trace ID
            trace_match = trace_pattern.search(line)
            if trace_match:
                current_trace_id = trace_match.group(1)

                for buffered_line in buffer:
                    log_by_trace[current_trace_id].append(buffered_line)

                    if retry_pattern.search(buffered_line):
                        ts = parse_timestamp(buffered_line)
                        if ts:
                            retry_timestamps[current_trace_id].append(ts)

                buffer = []


def summarize():
    """Print summary of log data grouped by Trace ID."""
    print("\n📦 API Log Summary Grouped by Trace ID")
    print("=======================================")

    for trace_id, lines in log_by_trace.items():
        print(f"\n🧵 Trace ID: {trace_id}")

        for line in lines:
            if "[ERROR]" in line:
                print(f"  🔴 ERROR: {line}")
            elif retry_pattern.search(line):
                print(f"  🔁 RETRY: {line}")
            elif "[INFO]" in line:
                print(f"  ℹ️ INFO: {line}")
            elif "[DEBUG]" in line:
                print(f"  🐞 DEBUG: {line}")

        timestamps = retry_timestamps.get(trace_id, [])
        if timestamps:
            print(f"\n  ⏱️ Retry Analysis:")
            print(f"     🔁 Total retries: {len(timestamps)}")

            if len(timestamps) >= 2:
                intervals = [
                    (timestamps[i] - timestamps[i - 1]).total_seconds()
                    for i in range(1, len(timestamps))
                ]
                for i, interval in enumerate(intervals, start=1):
                    print(f"     ⏳ Retry {i} interval: {interval:.2f} seconds")

                avg_interval = sum(intervals) / len(intervals)
                total_time = (timestamps[-1] - timestamps[0]).total_seconds()
                print(
                    f"     📈 Average retry interval: {avg_interval:.2f} seconds")
                print(
                    f"     📊 Total retry time span: {total_time:.2f} seconds")
        else:
            print("  ⏱️ No retry data for this trace.")
