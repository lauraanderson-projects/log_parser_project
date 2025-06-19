import json


def export_to_json(log_by_trace, retry_timestamps, retry_pattern, output_path="summary_output/log_summary.json"):
    summary = {}  # Initialize the summary dictionary

    print(log_by_trace)

    for trace_id, lines in log_by_trace.items():
        trace_summary = {
            "errors": [],
            "retries": [],
            "info": [],
            "debug": [],
            "retry_analysis": [],
        }

        for line in lines:
            if "[ERROR]" in line:
                trace_summary["errors"].append(line)
            elif retry_pattern.search(line):
                trace_summary["retries"].append(line)
            elif "[INFO]" in line:
                trace_summary["info"].append(line)
            elif "[DEBUG]" in line:
                trace_summary["debug"].append(line)

# Retry timing stats
        timestamps = retry_timestamps.get(trace_id, [])
        if len(timestamps) >= 2:
            intervals = [
                (timestamps[i] - timestamps[i - 1]).total_seconds()
                for i in range(1, len(timestamps))
            ]
            trace_summary["retry_analysis"] = intervals

        summary[trace_id] = trace_summary

    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"Log summary exported to {output_path}")
