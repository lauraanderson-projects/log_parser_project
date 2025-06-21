import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def plot_retry_intervals(retry_timestamps):
    output_dir = "summary_output/plot_output/"

    for trace_id, timestamps in retry_timestamps.items():
        if len(timestamps) < 2:
            continue  # Not enough data to plot

        # Calculate intervals
        intervals = [
            (timestamps[i] - timestamps[i - 1]).total_seconds()
            for i in range(1, len(timestamps))
        ]

        # Plotting
        plt.figure(figsize=(8, 4))
        plt.bar(range(1, len(intervals) + 1), intervals, color='skyblue')
        plt.title(f"Retry Intervals for Trace ID: {trace_id}")
        plt.xlabel("Retry Attempt")
        plt.ylabel("Interval (seconds)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{output_dir}retry_chart_{trace_id}.png")
        print(f"📊 Chart saved as: {output_dir}retry_chart_{trace_id}.png")
        plt.close()


# --- TEST ENTRY POINT 1 ---
#
# if __name__ == "__main__":
#    # Fake test data
#    retry_timestamps = {
#        "abc123": [
#            datetime(2025, 6, 18, 9, 0, 1),
#            datetime(2025, 6, 18, 9, 0, 5),
#            datetime(2025, 6, 18, 9, 0, 10),
#        ],
#        "def456": [
#            datetime(2025, 6, 18, 9, 1, 2),
#            datetime(2025, 6, 18, 9, 1, 6),
#        ]
#    }

#    plot_retry_intervals(retry_timestamps)


# --- TEST ENTRY POINT 2 ---
# if __name__ == "__main__":
#    from datetime import datetime, timedelta

#    base = datetime(2025, 6, 18, 9, 0, 0)
#    retry_timestamps = {
#        "abc123": [
#            base,
#            base + timedelta(seconds=3),
#            base + timedelta(seconds=8),
#            base + timedelta(seconds=15),
#        ]
#    }

#    print(f"abc123 timestamps: {len(retry_timestamps['abc123'])}")
#    plot_retry_intervals(retry_timestamps)
