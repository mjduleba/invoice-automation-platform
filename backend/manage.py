#!/usr/bin/env python
"""Django command-line utility for administrative tasks."""

import os
import sys


def main() -> None:
    """Run a Django management command from the command-line arguments.

    Args:
        None; reads the command from sys.argv.

    Raises:
        SystemExit: when the command exits with an error.

    Returns:
        None.
    """
    # Default settings module unless the environment overrides it
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
