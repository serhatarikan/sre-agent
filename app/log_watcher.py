import json
import os
import sys
import time
from app.llm_analyzer import analyze_log

# Resolve target log file path.
LOG_FILE_PATH = os.path.join("logs", "app.log")


def watch_logs():
    """Monitors the log file in real-time and filters for ERROR level entries."""

    # Verify log file exists
    if not os.path.exists(LOG_FILE_PATH):
        sys.stderr.write(
            f"{LOG_FILE_PATH} doesn't exist. Please provide a valid file path.\n"
            )
        sys.exit(1)

    print(f"[*] Starting Log Watcher on {LOG_FILE_PATH}...")

    # Open log file in read mode and move cursor to the end (tailing mode)
    with open(LOG_FILE_PATH, "r") as file:
        file.seek(0, os.SEEK_END)
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.5)
                continue
            try:
                log_data = json.loads(line)
                if log_data.get("level") == "ERROR":
                    print(
                        f"\n[ALERT]: Critical ERROR detected!\nMessage:"
                        f"{log_data.get('message')}\nDetails:"
                        f"{log_data.get('error_details')}\n"
                        f"SRE AGENT ANALYZING..."\n"
                        )
                    ai_analysis = analyze_log(log_data)
                    print("----------------------------------------")
                    print(ai_analysis)
                    print("----------------------------------------\n")
            except json.JSONDecodeError:
                continue
if __name__ == "__main__":
    watch_logs()