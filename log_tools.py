import time
import functools
from collections import Counter
from contextlib import contextmanager

import pandas as pd


bad_lines = 0


@contextmanager
def log_file(path):
    """Open a log file and always close it, even if an error happens."""
    file = open(path, "r", encoding="utf-8")
    try:
        yield file
    finally:
        file.close()


def read_logs(path):
    """Yield one parsed log line at a time."""
    global bad_lines

    with log_file(path) as file:
        for line in file:
            try:
                parts = line.strip().split(",", 3)

                if len(parts) != 4:
                    raise ValueError("Bad log line")

                yield {
                    "timestamp": parts[0],
                    "service": parts[1],
                    "level": parts[2],
                    "message": parts[3],
                }

            except (ValueError, IndexError):
                bad_lines += 1


def timer(func):
    """Print how long a function takes to run."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f} seconds")
        return result

    return wrapper


def retry(times=3):
    """Retry a function when it raises an exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    last_error = error
                    print(f"Retry {attempt}/{times}")

            raise last_error

        return wrapper

    return decorator


@retry(times=3)
def read_file(path):
    """Simple file reader used to demonstrate the retry decorator."""
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def filter_errors(logs):
    """Yield only ERROR log records."""
    for log in logs:
        if log["level"].upper() == "ERROR":
            yield log


def count_by_service(logs):
    """Count error records by service and yield the results."""
    counts = Counter()

    for log in logs:
        counts[log["service"]] += 1

    for service, count in counts.items():
        yield service, count


def top_services(path):
    """Return the top five services with the most errors."""
    logs = read_logs(path)
    errors = filter_errors(logs)
    counts = Counter(dict(count_by_service(errors)))
    return counts.most_common(5)


def export_excel(results, output="error_report.xlsx"):
    """Export the error counts to Excel."""
    df = pd.DataFrame(results, columns=["Service", "Error Count"])
    df.to_excel(output, index=False)
    print(f"Saved to {output}")


@timer
def main():
    global bad_lines
    bad_lines = 0

    path = "logs.txt"
    results = top_services(path)

    print("Top services:")
    for service, count in results:
        print(service, count)

    print("Bad lines:", bad_lines)

    export_excel(results)


if __name__ == "__main__":
    main()
