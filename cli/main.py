import click
import json
import sys
from typing import Optional
from datetime import datetime


@click.group()
@click.option(
    "--config", "-c", type=click.Path(), default=".env", help="Path to config file"
)
@click.option(
    "--output",
    "-o",
    type=click.Choice(["json", "table", "plain"]),
    default="table",
    help="Output format",
)
@click.option("--api-url", "-u", default="http://localhost:8000", help="API base URL")
@click.version_option(version="1.0.0", prog_name="CreatorERP CLI")
@click.pass_context
def cli(ctx, config, output, api_url):
    """CreatorERP CLI - Manage your creator business from the command line."""
    ctx.ensure_object(dict)
    ctx.obj["config"] = config
    ctx.obj["output"] = output
    ctx.obj["api_url"] = api_url
    ctx.obj["headers"] = {"Content-Type": "application/json"}


def output_result(data, output_format, headers=None):
    """Format and display output based on format type."""
    if output_format == "json":
        click.echo(json.dumps(data, indent=2, default=str))
    elif output_format == "plain":
        if isinstance(data, dict):
            for key, value in data.items():
                click.echo(f"{key}: {value}")
        elif isinstance(data, list):
            for item in data:
                click.echo(str(item))
        else:
            click.echo(str(data))
    else:
        if isinstance(data, dict):
            if "items" in data or any(isinstance(v, list) for v in data.values()):
                _print_table(data, headers)
            else:
                _print_dict_table(data)
        elif isinstance(data, list):
            _print_list_table(data, headers)
        else:
            click.echo(data)


def _print_dict_table(data):
    """Print a dictionary as a simple table."""
    max_key_len = max(len(str(k)) for k in data.keys())
    for key, value in data.items():
        click.echo(f"{str(key).ljust(max_key_len)} : {value}")


def _print_list_table(data, headers):
    """Print a list of dicts as a table."""
    if not data:
        click.echo("No data")
        return

    if isinstance(data[0], dict):
        all_keys = list(data[0].keys())
        keys = headers if headers else all_keys

        widths = {
            k: max(len(str(k)), max(len(str(d.get(k, ""))) for d in data)) for k in keys
        }

        header = " | ".join(k.ljust(widths[k]) for k in keys)
        click.echo(header)
        click.echo("-" * len(header))

        for item in data:
            row = " | ".join(str(item.get(k, "")).ljust(widths[k]) for k in keys)
            click.echo(row)
    else:
        for item in data:
            click.echo(str(item))


def _print_table(data, headers):
    """Print complex data as table."""
    if "items" in data:
        items = data["items"]
    else:
        items = data
    _print_list_table(items if isinstance(items, list) else [items], headers)


def success(message):
    """Print success message."""
    click.echo(click.style(f"[OK] {message}", fg="green", bold=True))


def error(message):
    """Print error message."""
    click.echo(click.style(f"[ERROR] {message}", fg="red", bold=True), err=True)


def info(message):
    """Print info message."""
    click.echo(click.style(f"[INFO] {message}", fg="cyan"))


def warning(message):
    """Print warning message."""
    click.echo(click.style(f"[WARN] {message}", fg="yellow"))


app = cli
