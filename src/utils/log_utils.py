#!/usr/bin/env python3

"""
This module implements the logging functionality.
Logging is based on the 'logging' module in Python3.
It creates a hierarchy of logging handlers where two handlers
ensures that logs are written to a log file in the /log directory
as well as console based log output for testing/development purposes.
"""

import logging
import sys
import time
import os
from typing import List, Any
from datetime import datetime


def get_console_handler(formatter: str) -> logging.StreamHandler:
    """
    Setup and returns the console handler with a formatting variable
    :param formatter: The format of the log.
    :return: The logging StreamHandler wrt. console logging
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(formatter))
    return console_handler


def get_file_handler(path: str, file: str, formatter: str, config: Any) -> logging.FileHandler:
    """
    Setup and returns the file handler with a given formatting.
    :param path: The absolute path for where the log is written to.
    :param file: The file name of the log.
    :param formatter: The format of the log.
    :param config: The Configuration object
    :return: The logging FileHandler.
    """
    filename, ext = file.split('.')
    filepath = path + '/' + filename + '_' + time.strftime("%Y%m%d-%H%M") + '.' + ext
    file_handler = logging.FileHandler(filepath)
    config.add_key_value('logfilepath', filepath)
    file_handler.setFormatter(logging.Formatter(formatter))
    return file_handler


def get_logger(log_name: str, f_name: str, path: str, f_std: str, f_file: str, config: Any) -> logging.Logger:
    """
    Parent function that creates the logging hierarchy and returns the Logger object.
    :param log_name: Name of the logger.
    :param f_name: Filename of the logger.
    :param path: The absolute path of where to FileHandler log should be written to.
    :param f_std: The format of the log for stdout.
    :param f_file: The format of the log for file writes.
    :param config: The configurator object
    :return: Logger object to orchestrate log entries from pipeline events in execution time.
    """
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler(f_std))
    logger.addHandler(get_file_handler(path, f_name, f_file, config))
    logger.propagate = False
    return logger


def close_logger() -> None:
    """
    Closes down all handlers from logging hierarchy.
    :return: None
    """
    logger = logging.getLogger()
    for handlers in logger.handlers:
        print(handlers)
        handlers.close()


def rename_and_move_file(log_path: str, files: List[str]) -> None:
    """
    Renames a logfile and moves it to archive.
    :param log_path: The relative path to log files
    :param files: The list of logfiles.
    :return: None
    """
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H:%M")
    folder = os.path.join(log_path, "archive/run_" + dt_string)
    os.makedirs(os.path.join(log_path, folder))
    for file in files:
        os.rename(os.path.join(log_path, file), os.path.join(folder, file))


def shutdown_and_move_logfiles(log_path: str) -> None:
    """
    Closes down loggers, renames logfiles to include a datetime object and moves the files to the archive.
    :param log_path: The
    :return: None
    """
    close_logger()
    log_files = [f for f in os.listdir(log_path) if os.path.isfile((os.path.join(log_path, f)))]
    rename_and_move_file(log_path, log_files)
