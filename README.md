# Task 1

This project implements the requirements shown in the assessment screenshot:

- `read_logs(path)` generator
- `@timer` decorator using `functools.wraps`
- `@retry(times=3)` decorator
- Lazy generator pipeline:
  `read_logs -> filter_errors -> count_by_service`
- Context manager for safe file handling
- `Counter` for top 5 error-producing services
- Excel export with pandas
- 3 pytest tests

## Assumed log format

Each line uses this format:

`timestamp,service,level,message`

Example:

`2026-10-07 10:00:00,payment,ERROR,Payment failed`

Malformed lines are skipped and counted.

## Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python log_tools.py
```

Run tests:

```bash
pytest -v
```

The program creates:

`error_report.xlsx`
