#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks on PORT 8082 by default."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csa.settings.development')
    
    # ✅ SET DEFAULT PORT TO 8082
    from django.core.management.commands.runserver import Command as runserver
    runserver.default_port = "8082"
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Install/update using 'pip install django'. "
            "Did you forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
