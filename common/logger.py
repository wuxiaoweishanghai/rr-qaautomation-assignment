import logging
import os
import traceback
from datetime import datetime
import allure
import sys

class StepLogger:
    _loggers = {}

    def __init__(self, test_name="default_test", page=None):
        self.test_name = test_name
        self.page = page
        self.logger = self._get_logger()

    def _get_logger(self):
        if self.test_name in StepLogger._loggers:
            return StepLogger._loggers[self.test_name]

        logger = logging.getLogger(self.test_name)
        logger.setLevel(logging.INFO)
        logger.propagate = False  # Prevent duplicate logs

        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

        # Console handler - only log messages without exception traceback
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        # Filter to block logs that have exception info, so tracebacks won't print to console
        console_handler.addFilter(lambda record: record.exc_info is None)
        logger.addHandler(console_handler)

        # File handler - write all logs including exception tracebacks
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H")
        log_file = os.path.join("logs", f"{timestamp}_{self.test_name}.log")
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        StepLogger._loggers[self.test_name] = logger
        return logger

    def step(self, message: str):
        """Log a normal step and add an Allure step name (not a context manager)"""
        self.logger.info(f"[STEP] {message}")
        allure.step(message)  # Log step name, no context block

    def error(self, message: str, exception: Exception = None):
        """Log error message without printing traceback to console,
        attach full traceback to log file and Allure report"""
        # Log error message normally (no exception info, so no traceback in console)
        self.logger.error(f"[ERROR] {message}")

        if exception:
            # Format the exception traceback string
            tb_list = traceback.format_exception(type(exception), exception, exception.__traceback__)
            tb_str = "".join(tb_list)

            # Manually emit the traceback only to file handlers, suppress on console
            for handler in self.logger.handlers:
                if isinstance(handler, logging.FileHandler):
                    handler.emit(logging.makeLogRecord({
                        "level": logging.ERROR,
                        "msg": tb_str,
                        "args": (),
                        "exc_info": None,
                    }))

            # Attach traceback to Allure report
            allure.attach(tb_str, name="Error Traceback", attachment_type=allure.attachment_type.TEXT)
