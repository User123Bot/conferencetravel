#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def setup_ssl_certification():

    if sys.platform == "darwin":
        import certifi

        os.environ["SSL_CERT_FILE"] = certifi.where()
    else:
        print("No SSL Certification Verification Required.")


def main():
    """Run administrative tasks."""
    setup_ssl_certification()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ctetproject.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
