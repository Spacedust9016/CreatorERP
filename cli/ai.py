import click
import sys
import os
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.main import cli, output_result, success, error, info


@cli.group()
@click.pass_context
def ai(ctx):
    """AI-powered analysis and insights."""
    pass


@ai.command("analyze")
@click.argument("query")
@click.option(
    "--provider",
    "-p",
    default="local",
    type=click.Choice(["local", "openai", "anthropic", "opencode", "custom"]),
    help="AI provider",
)
@click.option("--model", "-m", default=None, help="Model name")
@click.pass_context
def ai_analyze(ctx, query, provider, model):
    """Analyze data with AI. Usage: erp ai analyze "your query"."""

    async def run_query():
        from modules.ai_investigator.module import AIClient

        client = AIClient()
        result = await client.investigate(query, provider, model)
        return result

    try:
        info(f"Query: {query}")
        info(f"Provider: {provider}")

        result = asyncio.run(run_query())

        if ctx.obj["output"] == "json":
            output_result(result, "json")
        else:
            click.echo(click.style("\n=== AI ANALYSIS ===", fg="cyan", bold=True))
            click.echo(click.style(f"Provider: {result['provider']}", fg="yellow"))
            click.echo(click.style(f"Model: {result['model']}", fg="yellow"))
            click.echo("\n" + click.style(result["result"], fg="white"))
            success("Analysis complete")
    except Exception as e:
        error(f"Analysis failed: {e}")


@ai.command("dashboard")
@click.option("--provider", "-p", default="local", help="AI provider")
@click.pass_context
def analyze_dashboard(ctx, provider):
    """Analyze dashboard metrics with AI."""

    async def run():
        from modules.ai_investigator.module import AIClient
        from modules.social.module import SocialModule
        from modules.courses.module import CoursesModule
        from modules.finance.module import FinanceModule

        client = AIClient()
        context = {
            "social": SocialModule().get_simulated_data(),
            "courses": CoursesModule().get_simulated_data(),
            "finance": FinanceModule().get_simulated_data(),
        }
        query = """Analyze my creator business dashboard and provide:
1. Key performance insights
2. Areas of strength
3. Areas needing improvement
4. Recommended actions for growth"""

        result = await client.investigate(query, provider, context=context)
        return result

    try:
        info("Analyzing dashboard...")
        result = asyncio.run(run())

        if ctx.obj["output"] == "json":
            output_result(result, "json")
        else:
            click.echo(
                click.style("\n=== DASHBOARD ANALYSIS ===", fg="cyan", bold=True)
            )
            click.echo(
                click.style(
                    f"Provider: {result['provider']} | Model: {result['model']}",
                    fg="yellow",
                )
            )
            click.echo("\n" + click.style(result["result"], fg="white"))
            success("Dashboard analysis complete")
    except Exception as e:
        error(f"Analysis failed: {e}")


@ai.command("content")
@click.option("--provider", "-p", default="local", help="AI provider")
@click.pass_context
def analyze_content(ctx, provider):
    """Analyze content strategy with AI."""

    async def run():
        from modules.ai_investigator.module import AIClient
        from modules.calendar.module import CalendarModule

        client = AIClient()
        context = {
            "upcoming_content": CalendarModule().get_simulated_data()["upcoming"]
        }
        query = """Analyze my content calendar and provide:
1. Content strategy assessment
2. Platform mix optimization
3. Best posting times
4. Content ideas based on gaps"""

        result = await client.investigate(query, provider, context=context)
        return result

    try:
        info("Analyzing content strategy...")
        result = asyncio.run(run())

        if ctx.obj["output"] == "json":
            output_result(result, "json")
        else:
            click.echo(click.style("\n=== CONTENT ANALYSIS ===", fg="cyan", bold=True))
            click.echo(
                click.style(
                    f"Provider: {result['provider']} | Model: {result['model']}",
                    fg="yellow",
                )
            )
            click.echo("\n" + click.style(result["result"], fg="white"))
            success("Content analysis complete")
    except Exception as e:
        error(f"Analysis failed: {e}")


@ai.command("providers")
@click.pass_context
def list_providers(ctx):
    """List available AI providers."""
    try:
        providers = [
            {
                "name": "local",
                "description": "Local LLM via Ollama",
                "config_key": "AI_API_BASE",
                "default_model": "llama2",
            },
            {
                "name": "openai",
                "description": "OpenAI GPT models",
                "config_key": "OPENAI_API_KEY",
                "default_model": "gpt-4-turbo",
            },
            {
                "name": "anthropic",
                "description": "Anthropic Claude models",
                "config_key": "ANTHROPIC_API_KEY",
                "default_model": "claude-3-opus",
            },
            {
                "name": "opencode",
                "description": "OpenCode AI models",
                "config_key": "OPENCODE_API_KEY",
                "default_model": "opencode-4",
            },
            {
                "name": "custom",
                "description": "Custom API endpoint",
                "config_keys": ["AI_API_BASE", "AI_API_KEY"],
            },
        ]

        if ctx.obj["output"] == "json":
            output_result(providers, "json")
        else:
            click.echo(click.style("\n=== AI PROVIDERS ===", fg="cyan", bold=True))
            for p in providers:
                click.echo(f"\n{click.style(p['name'], fg='yellow', bold=True)}")
                click.echo(f"  Description: {p['description']}")
                click.echo(
                    f"  Config: {p.get('config_key', p.get('config_keys', 'N/A'))}"
                )
                click.echo(f"  Default Model: {p.get('default_model', 'varies')}")
            success("Providers listed")
    except Exception as e:
        error(f"Failed to list providers: {e}")
