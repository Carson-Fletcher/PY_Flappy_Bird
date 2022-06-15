"""Module for logging runtime information to a given source.
Does not block runtime exceptions from stopping the execution of the program.

Classes:
    LoggingLevels: Contains the different logging levels avalible.
    Logger: Class for handling the writing of logs to an output source.

Version: 1.0
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pprint import pformat
from traceback import extract_stack
from typing import Any, Iterable, Literal, Optional


class LoggingLevels(Enum):
    """Contains the different logging levels avalible."""
    LOG = "LOG"
    INFO = "INFO"
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    WARN = "WARNING"
    ERR = "ERROR"
    FATAL = "FATAL"

    @staticmethod
    def get_logging_levels() -> tuple[LoggingLevels]:
        """Returns logging levels."""
        return tuple(logging_level for logging_level in LoggingLevels)


@dataclass
class _LoggerSettings:
    """
    Private dataclass for storing the logger settings.

    Properties:
        name: Toggle the name.
        default_date_format: Default strftime date format [yyyy-mm-dd, hh:mm:ss]
        date_time: date_time[0] -> toggle the date time, date_time[1] -> strftime format.
        default_logging_level: Default logging level [LoggingLevels.LOG
        logging_level: logging_level[0] -> Toggle the logging level,\
        logging_level[1] -> Default logging level.
        stack_trace: Toggle the stack trace.

    Methods:
        get_settings: Returns the settings as a dict.
    """
    name: bool = True
    default_date_format = "%Y-%m-%d, %H:%M:%S"
    date_time: tuple[bool, str] = field(
        default=(True, default_date_format)
    )
    default_logging_level = LoggingLevels.LOG
    logging_level: tuple[bool, LoggingLevels] = field(
        default=(True, default_logging_level)
    )
    stack_trace: bool = True

    def get_settings(self) -> dict[str, Any]:
        """Returns the current settings as dict."""
        return {
            "name": self.name,
            "date_time": self.date_time,
            "logging_level": self.logging_level,
            "stack_trace": self.stack_trace
        }

class Logger:
    """
    Class for handling the writing of logs to an output source.

    Properties:
        logger_name: Name used to indentify the logger which printed a statement.
        default_src: Path to the logging output file.

    Methods:
        set_settings: Sets the default behaviour of the output string when logging.
        get_settings: Gets the current settings.
        set_logging_state: Sets the logging state to the new state.
        get_logging_state: Gets the current logging state.
        log: Logs information given to the output source.
        log_exception: Allows the logging of runtime exceptions to the default output source.
    """
    def __init__(self, default_src: str, name: str = "") -> None:
        self.logger_name = name
        self.defualt_src = default_src
        self._logging_state = True
        self._settings = _LoggerSettings()

    def set_settings(
        self,
        *,
        name: bool,
        date_time: tuple[bool, Optional[str]],
        logging_level: tuple[bool, Optional[LoggingLevels]],
        stack_trace: bool
    ) -> None:
        """
        Toggle what the logger will output by default.

        Args:
            name: Toggle the name.
            date_time: date_time[0] -> toggle the date time, date_time[1] -> strftime format.
            logging_level: logging_level[0] -> toggle the logging level,\
            logging_level[1] -> default logging level.
            stack_trace: Toggle the stack trace.
        """
        self._settings.name = name
        self._settings.date_time = (
            date_time[0],
            date_time[1] if date_time[1] is not None else self._settings.default_date_format
        )
        self._settings.logging_level = (
            logging_level[0],
            logging_level[1] if logging_level[1] is not
                None else self._settings.default_logging_level
        )
        self._settings.stack_trace = stack_trace

    def get_settings(self) -> dict[str, Any]:
        """Returns the current settings as a dict."""
        return self._settings.get_settings()

    def get_logging_state(self) -> bool:
        """Returns the current logging state."""
        return self._logging_state

    def set_logging_state(self, state: bool) -> None:
        """Sets the logging state to the new state."""
        self._logging_state = state

    def _get_logging_string(
            self,
            objects: Iterable[object],
            name: bool,
            date_time: bool,
            logging_level: LoggingLevels | Literal[False],
            stack_trace: bool
        ) -> str:
        """
        Generates a string with logging information.

        Args:
            msg: Optional msg in a tuple.
            name: Toggle the output of the name.
            date_time: Toggle the output of the date time.
            logging_level: Toggle the output of the logging level.
            stack_trace: Toggle the output of the stack trace.
        """
        output_string = ""
        if name and self.logger_name:
            output_string += f"{self.logger_name}:"

        if date_time:
            output_string += f"[{datetime.now().strftime(self._settings.date_time[1])}]"

        if logging_level is not False:
            output_string += f"[{logging_level.value}]"

        if stack_trace:
            output_string += pformat(
                [i for i in extract_stack() if i.name not in ("_get_logging_string", "log")]
            )

        if objects:
            output_string += pformat(objects, underscore_numbers=True)

        if not output_string:
            output_string += "[EMPTY LOG]"

        return output_string + "\n"


    def log(
            self,
            *msg: object,
            src: Optional[str] = None,
            name: Optional[bool] = None,
            date_time: Optional[bool] = None,
            logging_level: Optional[LoggingLevels | Literal[False]] = None,
            stack_trace: Optional[bool] = None
        ) -> None:
        """
        Writes the logging data to the output source.

        Args:
            objects: Optional msg.
            src: Path to the logging file, if None uses default src.
            name: Toggle the name, if None uses the default settings.
            date_time: Toggle the date time, if None uses the default settings.
            logging_level: Logging level for the output, if None uses the default settings.
            stack_trace: Toggle the stack_trace, if None uses the default settings.
        """
        if not self._logging_state:
            return

        if src is None:
            src = self.defualt_src

        if name is None:
            name = self._settings.name

        if date_time is None:
            date_time = self._settings.date_time[0]

        if logging_level is None:
            if self._settings.logging_level[0]:
                logging_level = self._settings.logging_level[1]
            else:
                logging_level = self._settings.default_logging_level

        if stack_trace is None:
            stack_trace = self._settings.stack_trace

        with open(src, "a", encoding="UTF-8") as file:
            file.write(
                self._get_logging_string(list(msg), name, date_time, logging_level, stack_trace)
            )


    def log_exception(self, *msg: str) -> None:
        """
        Logs runtime exceptions of the default src of the class

        To do this you need to:\n
            1. from sys import stderr
            2. stderr.write = logger.log_exception
        """
        with open(self.defualt_src, "a", encoding="UTF-8") as file:
            file.write(*msg)
