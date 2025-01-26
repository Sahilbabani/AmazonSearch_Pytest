from datetime import datetime
import logging


class Logger:
    @staticmethod
    def loggen():
        current_date_format = datetime.now().strftime("%d-%m-%Y")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(f"./logs/detailed_test_logs_{current_date_format}.log"),
                logging.StreamHandler(),
            ],
        )
        logging.info("Logging configuration initialized.")
        return logging
