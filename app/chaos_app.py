import json
import logging
import os
import random
import time
from datetime import datetime, timezone

# Resolve log directory dynamically with fallback to local directory
LOG_DIR = os.getenv("LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")


class StructuredJsonFormatter(logging.Formatter):
    """Custom logging formatter to output log records as structured JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": "order-service",
            "environment": "production",
            "message": record.getMessage(),
        }

        # Attach error details if explicitly provided via extra parameters
        if hasattr(record, "error_details"):
            log_payload["error_details"] = record.error_details

        return json.dumps(log_payload)


# Initialize custom logger
logger = logging.getLogger("ChaosSimulator")
logger.setLevel(logging.INFO)

# File handler for writing logs to shared volume
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(StructuredJsonFormatter())
logger.addHandler(file_handler)

# Console handler for container standard output (stdout)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(StructuredJsonFormatter())
logger.addHandler(stream_handler)

# Simulated failure scenarios pool
SIMULATED_ERRORS = [
    {
        "code": "DB_CONN_TIMEOUT",
        "message": "Failed to connect to PostgreSQL primary host at 10.0.4.12:5432 after 5000ms",
        "stack_trace": "psycopg2.OperationalError: timeout expired\n  at db_pool.get_connection() line 42",
    },
    {
        "code": "REDIS_CONNECTION_REFUSED",
        "message": "Error 111 connecting to 127.0.0.1:6379. Connection refused.",
        "stack_trace": "redis.exceptions.ConnectionError\n  at redis.client.execute() line 108",
    },
    {
        "code": "PAYMENT_GATEWAY_ERROR",
        "message": "Upstream service payment-v2.internal returned 502 Bad Gateway",
        "stack_trace": "requests.exceptions.HTTPError: 502 Server Error\n  at payment_service.checkout() line 89",
    },
]


def simulate_traffic() -> None:
    """Generates synthetic application traffic with randomized error rates."""
    logger.info("Processing incoming checkout request for UserID: 84920")

    # 30% probability of triggering a simulated service failure
    if random.random() < 0.30:
        selected_error = random.choice(SIMULATED_ERRORS)
        logger.error(
            f"Request failed: {selected_error['message']}",
            extra={"error_details": selected_error},
        )
    else:
        logger.info("Order processed successfully. HTTP 200 OK")


if __name__ == "__main__":
    logger.info("Chaos Engineering Simulator initializing...")
    while True:
        simulate_traffic()
        time.sleep(random.uniform(3, 7))