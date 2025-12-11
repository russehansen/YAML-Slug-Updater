#!/usr/bin/env python3
"""Small runner wrapper to match README usage.

This imports the core CLI from `update_quickbase_slugs.py` so users can run:

    python run_slug_update.py [--dry-run]

Using the wrapper keeps the README instructions accurate.
"""
from update_quickbase_slugs import cli


if __name__ == "__main__":
    cli()
