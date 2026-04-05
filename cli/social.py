import click
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.main import cli, output_result, success, error, info


@cli.group()
@click.pass_context
def social(ctx):
    """Manage social media analytics."""
    pass


@social.command("platforms")
@click.pass_context
def get_platforms(ctx):
    """Get all social media platform metrics."""
    from modules.social.module import SocialModule

    try:
        module = SocialModule()
        data = module.get_simulated_data()
        output_result(data["platforms"], ctx.obj["output"])
        success("Platform data retrieved")
    except Exception as e:
        error(f"Failed to get platforms: {e}")


@social.command("posts")
@click.option("--limit", "-l", default=10, help="Number of posts to show")
@click.pass_context
def get_posts(ctx, limit):
    """Get top performing posts."""
    from modules.social.module import SocialModule

    try:
        module = SocialModule()
        data = module.get_simulated_data()
        posts = data["top_posts"][:limit]
        output_result(posts, ctx.obj["output"])
        success(f"Retrieved {len(posts)} posts")
    except Exception as e:
        error(f"Failed to get posts: {e}")


@social.command("trend")
@click.pass_context
def get_trend(ctx):
    """Get engagement trend data."""
    from modules.social.module import SocialModule

    try:
        module = SocialModule()
        data = module.get_simulated_data()
        output_result(
            {"platforms": data["platforms"], "top_posts": data["top_posts"]},
            ctx.obj["output"],
        )
        success("Trend data retrieved")
    except Exception as e:
        error(f"Failed to get trend: {e}")


@social.command("summary")
@click.pass_context
def social_summary(ctx):
    """Get social media summary dashboard."""
    from modules.social.module import SocialModule

    try:
        module = SocialModule()
        data = module.get_simulated_data()

        if ctx.obj["output"] == "json":
            output_result(data, "json")
        else:
            click.echo(
                click.style("\n=== SOCIAL MEDIA SUMMARY ===", fg="cyan", bold=True)
            )

            for platform in data["platforms"]:
                click.echo(
                    f"\n{click.style(platform['platform'], fg='yellow', bold=True)}"
                )
                click.echo(f"  Followers: {platform['followers']:,}")
                click.echo(f"  Impressions (7d): {platform['impressions_7d']:,}")
                click.echo(f"  Engagements: {platform['engagements']:,}")
                engagement_color = (
                    "green" if platform["engagement_rate"] > 3 else "yellow"
                )
                click.echo(
                    f"  Engagement Rate: {click.style(str(platform['engagement_rate']) + '%', fg=engagement_color)}"
                )

            click.echo(click.style("\n--- Top Posts ---", fg="cyan"))
            for post in data["top_posts"]:
                click.echo(
                    f"  [{post['platform']}] {post['content'][:40]}... - {post['reach']:,} reach, {post['engagement_rate']}% eng."
                )

            success("Summary complete")
    except Exception as e:
        error(f"Failed to generate summary: {e}")
