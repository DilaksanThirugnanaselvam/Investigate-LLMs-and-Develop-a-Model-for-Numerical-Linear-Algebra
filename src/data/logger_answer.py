import logging

from config import BASE_PATH

# Configure logging
LOG_FILE = f"{BASE_PATH}/logs/answer.txt"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(message)s",
    encoding="utf-8",
)


def log_request(timestamp, section, question, model, status_code, error=None):
    log_entry = f"Time: {timestamp} | Section: {section} | Q: {question} | M: {model} | Status: {status_code} | Error: {error}"
    logging.info(log_entry)
