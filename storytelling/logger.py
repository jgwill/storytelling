import json
import logging
import os
from datetime import datetime
from typing import Any, List

from termcolor import colored


class Logger:
    """
    A custom logger for the WillWrite application that handles session-based
    directory creation, console logging, file logging, and LLM interaction tracing.
    """

    def __init__(self, config: Any) -> None:
        self.config = config
        self.session_dir = ""
        self.debug_dir = ""
        self._setup_directories()
        self._setup_logger()

    def _setup_directories(self) -> None:
        """Creates the logging directories for the current session."""
        base_log_dir = "Logs"
        if not os.path.exists(base_log_dir):
            os.makedirs(base_log_dir)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        self.session_dir = os.path.join(base_log_dir, f"Generation_{timestamp}")
        os.makedirs(self.session_dir, exist_ok=True)

        self.debug_dir = os.path.join(self.session_dir, "LangchainDebug")
        os.makedirs(self.debug_dir, exist_ok=True)

    def _setup_logger(self) -> None:
        """Configures the root logger for console and file output."""
        self.logger = logging.getLogger("WillWrite")
        self.logger.setLevel(logging.DEBUG if self.config.debug else logging.INFO)

        # Prevent duplicate handlers if logger is re-initialized
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Console Handler
        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File Handler
        log_file_path = os.path.join(self.session_dir, "Main.log")
        file_handler = logging.FileHandler(log_file_path)
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def save_interaction(self, name: str, messages: List[Any]) -> None:
        """
        Saves the history of an LLM interaction to JSON and Markdown files.

        Args:
            name: A descriptive name for the interaction (e.g., "0_Main.GenerateOutline").
            messages: A list of message objects from the LLM interaction.
        """
        base_filepath = os.path.join(self.debug_dir, name)

        # Save as JSON
        json_filepath = f"{base_filepath}.json"
        try:
            with open(json_filepath, "w", encoding="utf-8") as f:
                # Handle non-serializable content if necessary, e.g. AIMessage objects
                serializable_messages = [
                    msg.dict() if hasattr(msg, "dict") else msg for msg in messages
                ]
                json.dump(serializable_messages, f, indent=2)
        except Exception as e:
            self.error(f"Failed to save JSON interaction log for {name}: {e}")

        # Save as Markdown
        md_filepath = f"{base_filepath}.md"
        try:
            with open(md_filepath, "w", encoding="utf-8") as f:
                f.write(f"# LLM Interaction: {name}\n\n")
                for msg in messages:
                    role = (
                        msg.get("type", "unknown")
                        if isinstance(msg, dict)
                        else getattr(msg, "type", "unknown")
                    )
                    content = (
                        msg.get("content", "")
                        if isinstance(msg, dict)
                        else getattr(msg, "content", "")
                    )
                    f.write(f"## Role: {role}\n\n")
                    f.write(f"```\n{content}\n```\n\n---\n\n")
        except Exception as e:
            self.error(f"Failed to save Markdown interaction log for {name}: {e}")

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)


class ColoredFormatter(logging.Formatter):
    """
    A custom formatter to add colors to log messages.
    """

    COLORS = {
        "WARNING": "yellow",
        "INFO": "green",
        "DEBUG": "blue",
        "CRITICAL": "red",
        "ERROR": "red",
    }

    def format(self, record: logging.LogRecord) -> str:
        log_message = super().format(record)
        return colored(log_message, self.COLORS.get(record.levelname))


if __name__ == "__main__":
    # Example Usage
    class MockConfig:
        debug = True

    config = MockConfig()
    logger = Logger(config)

    logger.info("This is an info message.")
    logger.debug("This is a debug message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")

    # Example interaction data
    mock_messages = [
        {"type": "system", "content": "You are a helpful assistant."},
        {"type": "human", "content": "Hello, world!"},
        {"type": "ai", "content": "Hello! How can I help you today?"},
    ]
    logger.save_interaction("0_Example.Test", mock_messages)
    print(f"Logs saved in: {logger.session_dir}")
