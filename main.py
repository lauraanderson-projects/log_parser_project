import os
import re

# Path to the log file
log_file_path = os.path.join("logs", "api_log_sample.txt")


def find_api_issues_regex(file_path):
    pattern = re.compile(r"ERROR.*(connect|Timeout)", re.IGNORECASE)
    with open(file_path, 'r') as file:
        for line in file:
            if pattern.search(line):
                print(line.strip())


if __name__ == "__main__":
    find_api_issues_regex(log_file_path)
