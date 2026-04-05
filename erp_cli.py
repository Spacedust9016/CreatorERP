#!/usr/bin/env python
"""
CreatorERP CLI - Command Line Interface for Creator Business Management

Usage:
    erp --help
    erp status
    erp dashboard
    erp social summary
    erp courses list
    erp ai analyze "What are my top revenue sources?"
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli.commands import cli

if __name__ == "__main__":
    cli()
