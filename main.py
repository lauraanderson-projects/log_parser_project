import os
from parser import analyze_log, summarize, log_by_trace, retry_timestamps, retry_pattern
from exporter import export_to_json
from visualizer import plot_retry_intervals

log_file_path = os.path.join("logs", "api_log_sample_2.txt")

if __name__ == "__main__":
    analyze_log(log_file_path)
    summarize()
    export_to_json(log_by_trace, retry_timestamps, retry_pattern)
    plot_retry_intervals(retry_timestamps)
    # print("✅ Log analysis complete. Results exported and visualized.")
