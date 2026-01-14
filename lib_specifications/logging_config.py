"""Logging configuration for lib-specifications package."""

import logging
import sys
from typing import Any


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name.

    Args:
        name: Logger name (typically __name__ of the module)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(f"lib_specifications.{name}")


def setup_logging(
    level: int = logging.WARNING,
    format_string: str | None = None,
    stream: Any | None = None,
) -> None:
    """Configure logging for the lib-specifications package.

    Args:
        level: Logging level (default: WARNING)
        format_string: Custom format string. If None, uses default format.
        stream: Output stream. If None, uses sys.stderr.
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    if stream is None:
        stream = sys.stderr

    # Configure root logger for lib_specifications
    logger = logging.getLogger("lib_specifications")
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(stream)
    handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    # Prevent propagation to root logger to avoid duplicate messages
    logger.propagate = False


# Default logger for the package
logger = get_logger(__name__)
