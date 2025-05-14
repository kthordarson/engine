import pygame

import os
import sys
from traceback import extract_tb

__all__ = ["error","warning","quit"]


def error(err: Exception, debug: bool) -> None:
    """
    Handles exceptions by printing or showing a popup error box.

    Args:
        err (Exception): The exception instance that was raised.
        debug (bool): If True, print the error details to the console; otherwise, show a GUI message box.
    """
    error_type = type(err).__name__
    error_message = str(err)
    traceback_list = extract_tb(err.__traceback__)

    error_details = [
        f"File: {os.path.basename(tb.filename)}, Line: {tb.lineno}"
        for tb in traceback_list
    ]
    formatted_traceback = (
        "\n".join(error_details) if len(error_details) <= 1
        else "\n" + "\n".join(error_details)
    )

    nice_error_message = (
        f"Type: {error_type}\n"
        f"Message: {error_message}\n"
        f"Traceback: {formatted_traceback}"
    )

    if debug:
        print(
            "-----------------------------------\n"
            "Error: An unexpected error occurred\n"
            f"{nice_error_message}\n"
            "-----------------------------------"
        )
    else:
        pygame.display.message_box(
            "An unexpected error occurred",
            nice_error_message,
            "error"
        )


def warning(message: str) -> None:
    """
    Prints a warning message to the console.

    Args:
        message (str): The warning message to display.
    """
    print(f"Warning: {message}")

# def log(): ...


def quit() -> None:
    """
    Exit the application cleanly.

    Calls `sys.exit()` to terminate the process.
    """
    sys.exit()