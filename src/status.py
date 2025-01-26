from termcolor import colored

def error(message: str, show_emoji: bool = True) -> None:
    """
    Prints an error message in red.

    Args:
        message (str): The error message to display.
        show_emoji (bool): Whether to include an emoji in the message.

    Returns:
        None
    """
    emoji = "❌" if show_emoji else ""
    print(colored(f"{emoji} {message}", "red"))

def success(message: str, show_emoji: bool = True) -> None:
    """
    Prints a success message in green.

    Args:
        message (str): The success message to display.
        show_emoji (bool): Whether to include an emoji in the message.

    Returns:
        None
    """
    emoji = "✅" if show_emoji else ""
    print(colored(f"{emoji} {message}", "green"))

def info(message: str, show_emoji: bool = True) -> None:
    """
    Prints an informational message in magenta.

    Args:
        message (str): The info message to display.
        show_emoji (bool): Whether to include an emoji in the message.

    Returns:
        None
    """
    emoji = "ℹ️" if show_emoji else ""
    print(colored(f"{emoji} {message}", "magenta"))

def warning(message: str, show_emoji: bool = True) -> None:
    """
    Prints a warning message in yellow.

    Args:
        message (str): The warning message to display.
        show_emoji (bool): Whether to include an emoji in the message.

    Returns:
        None
    """
    emoji = "⚠️" if show_emoji else ""
    print(colored(f"{emoji} {message}", "yellow"))

def question(message: str, show_emoji: bool = True) -> str:
    """
    Displays a question message in magenta and captures user input.

    Args:
        message (str): The question message to display.
        show_emoji (bool): Whether to include an emoji in the message.

    Returns:
        str: The user's input.
    """
    emoji = "❓" if show_emoji else ""
    return input(colored(f"{emoji} {message}", "magenta"))
