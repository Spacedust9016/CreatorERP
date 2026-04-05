import click
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.main import cli, output_result, success, error, info


@cli.group()
@click.pass_context
def finance(ctx):
    """Manage financial tracking."""
    pass


@finance.command("overview")
@click.pass_context
def finance_overview(ctx):
    """Get financial overview."""
    from modules.finance.module import FinanceModule

    try:
        module = FinanceModule()
        data = module.get_simulated_data()

        overview = {
            "monthly_revenue": data["monthly_revenue"],
            "revenue_sources": {s["source"]: s["amount"] for s in data["sources"]},
        }

        if ctx.obj["output"] == "json":
            output_result(overview, "json")
        else:
            click.echo(
                click.style("\n=== FINANCIAL OVERVIEW ===", fg="cyan", bold=True)
            )
            click.echo(f"\nMonthly Revenue: ${data['monthly_revenue']:,}")
            click.echo(click.style("\nRevenue Sources:", fg="yellow"))
            for source in data["sources"]:
                pct = (source["amount"] / data["monthly_revenue"]) * 100
                click.echo(f"  {source['source']}: ${source['amount']:,} ({pct:.1f}%)")
            success("Financial overview retrieved")
    except Exception as e:
        error(f"Failed to get overview: {e}")


@finance.command("revenue")
@click.option(
    "--period",
    "-p",
    default="month",
    type=click.Choice(["month", "year"]),
    help="Time period",
)
@click.pass_context
def revenue_breakdown(ctx, period):
    """Get revenue breakdown."""
    from modules.finance.module import FinanceModule

    try:
        module = FinanceModule()
        data = module.get_simulated_data()
        output_result(
            {
                "period": period,
                "total": data["monthly_revenue"],
                "breakdown": data["sources"],
            },
            ctx.obj["output"],
        )
        success("Revenue breakdown retrieved")
    except Exception as e:
        error(f"Failed to get revenue: {e}")


@finance.command("transactions")
@click.option("--limit", "-l", default=10, help="Number of transactions")
@click.pass_context
def list_transactions(ctx, limit):
    """List recent transactions."""
    try:
        transactions = [
            {
                "date": "2026-04-05",
                "description": "New video published",
                "amount": 0,
                "category": "Content",
                "type": "expense",
            },
            {
                "date": "2026-04-04",
                "description": "Newsletter #48 sent",
                "amount": 0,
                "category": "Marketing",
                "type": "expense",
            },
            {
                "date": "2026-04-04",
                "description": "12 new enrollments",
                "amount": 180,
                "category": "Courses",
                "type": "income",
            },
            {
                "date": "2026-04-01",
                "description": "AdSense payout",
                "amount": 620,
                "category": "Ads",
                "type": "income",
            },
            {
                "date": "2026-03-28",
                "description": "Sponsorship deal",
                "amount": 260,
                "category": "Sponsors",
                "type": "income",
            },
        ]
        output_result(transactions[:limit], ctx.obj["output"])
        success(f"Showing {min(limit, len(transactions))} transactions")
    except Exception as e:
        error(f"Failed to list transactions: {e}")


@finance.command("export")
@click.option(
    "--format",
    "-f",
    "fmt",
    default="csv",
    type=click.Choice(["csv", "json"]),
    help="Export format",
)
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.pass_context
def export_finance(ctx, fmt, output):
    """Export financial data."""
    try:
        from modules.finance.module import FinanceModule

        module = FinanceModule()
        data = module.get_simulated_data()

        if output:
            with open(output, "w") as f:
                if fmt == "json":
                    json.dump(data, f, indent=2)
                else:
                    f.write("Source,Amount\n")
                    for s in data["sources"]:
                        f.write(f"{s['source']},{s['amount']}\n")
            success(f"Exported to {output}")
        else:
            if fmt == "json":
                output_result(data, "json")
            else:
                click.echo("Source,Amount")
                for s in data["sources"]:
                    click.echo(f"{s['source']},{s['amount']}")
            success("Data exported")
    except Exception as e:
        error(f"Failed to export: {e}")
