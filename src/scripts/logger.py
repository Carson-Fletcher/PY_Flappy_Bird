"""Module for logging runtime information to a given source.
Does not block runtime exceptions from stopping the execution of the program.

Classes:
    LoggingLevels: Contains the different logging levels avalible.
    Logger: Class for handling the writing of logs to an output source.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from traceback import extract_stack


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


class Logger:
    """Class for handling the writing of logs to an output source.

    Properties:
        logger_name: Name used to indentify the logger which printed a statement.
        default_src: Path to the logging output file.
        logging_state: Toggle whether the logger will output anything regardless of method calls.

    Methods:
        set_logging_settings: Sets the default behaviour of the output string when logging.
        get_logging_settings: Gets the current settings.
        log: Logs information given to the output source.
        log_exception: Allows the logging of runtime exceptions to the default output source.
    """
    def __init__(self, default_src: str, name: str = "") -> None:
        self.logger_name = name
        self.defualt_src = default_src
        self.logging_state = True
        self.__settings = {
            "name": True,
            "date_time": True,
            "logging_level": True,
            "stack_trace": True
        }

    def set_logging_settings(
        self,
        name: bool,
        date_time: bool,
        logging_level: bool,
        stack_trace: bool
    ) -> None:
        """Toggle what the logger will output by default.

        Args:
            name: Toggle the name.
            date_time: Toggle the date time.
            logging_level: Toggle the logging level.
            stack_trace: Toggle the stack trace.
        """
        for setting_key, new_setting in zip(
            self.__settings.keys(),
            (name, date_time, logging_level, stack_trace)
        ):
            self.__settings[setting_key] = new_setting

    def get_logging_settings(self) -> dict[str, bool]:
        """Returns the current settings."""
        return self.__settings

    def __get_logging_string(
            self,
            msg: tuple[str],
            name: bool,
            date_time: bool,
            logging_level: LoggingLevels | None,
            stack_trace: bool
        ) -> str:
        """Generates a string with logging information.

        Args:
            msg: Optional msg in a tuple.
            name: Toggle the output of the name.
            date_time: Toggle the output of the date time.
            logging_level: Toggle the output of the logging level.
            stack_trace: Toggle the output of the stack trace.
        """
        output_string = ""
        if name and self.logger_name:
            output_string += f"{self.logger_name}: "

        if date_time:
            output_string += f"[{datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}]"

        if logging_level is not None:
            output_string += f"[{logging_level.value}]"

        if stack_trace:
            output_string += "".join(
                str(value) for value in extract_stack() if value.name not in (
                    "__get_logging_string", "log"
                )
            )

        if msg:
            output_string += '"' + ", ".join(msg) + '"'

        # Itterates throught the output string and inserts spaces after every section seperator
        for index in range(len(output_string) - 1):
            if output_string[index] in (
                "]", ">"
            ) and output_string[index] + output_string[index + 1] != ">>":
                output_string = output_string[:index + 1] + " " + output_string[index + 1:]

        if not output_string:
            output_string += "[EMPTY LOG]"

        return output_string + "\n"


    def log(
            self,
            *msg: str,
            src: str | None = None,
            name: bool | None = None,
            date_time: bool | None = None,
            logging_level: LoggingLevels | None = None,
            stack_trace: bool | None = None
        ) -> None:
        """Writes the logging data to the output source.

        Args:
            msg: Optional msg.
            src: Path to the logging file, if None uses default src.
            name: Toggle the name, if None uses the default settings.
            date_time: Toggle the date time, if None uses the default settings.
            logging_level: Logging level for the output, if None & settings uses LoggingLevls.LOG.
            stack_trace: Toggle the stack_trace, if None uses the default settings.
        """
        if not self.logging_state:
            return

        if src is None:
            src = self.defualt_src

        if name is None:
            name = self.__settings["name"]

        if date_time is None:
            date_time = self.__settings["date_time"]

        if logging_level is None:
            if not self.__settings["logging_level"]:
                logging_level = None
            else:
                logging_level = LoggingLevels.LOG

        if stack_trace is None:
            stack_trace = self.__settings["stack_trace"]

        with open(src, "a", encoding="UTF-8") as file:
            file.write(
                self.__get_logging_string(msg, name, date_time, logging_level, stack_trace)
            )


    def log_exception(self, *msg: str) -> None:
        """Logs runtime exceptions of the default src of the class

        To do this you need to: 1. from sys import stderr, 2. stderr.write = [Logger].log_exception
        """
        with open(self.defualt_src, "a", encoding="UTF-8") as file:
            file.write(*msg)
