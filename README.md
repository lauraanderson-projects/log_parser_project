Recommended Folder structure:

log_parser_project/
├── logs/
│ └── api_log_sample_2.txt
├── main.py
├── parser.py # analyze_log, summarize
├── exporter.py # export_to_json
├── visualizer.py # (next) matplotlib charts
└── tests/
└ ── test_parser.py # pytest unit tests

Dependencies:
pip install pytest

To run a test_parser.py, from root:
python -m pytest

From root, cleanup pycache files:

Below is commented out:

<!--find . -name "__pycache__" -exec rm -r {} +-->
