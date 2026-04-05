import click
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.main import cli, output_result, success, error, info


@cli.group()
@click.pass_context
def courses(ctx):
    """Manage course platform analytics."""
    pass


@courses.command("list")
@click.pass_context
def list_courses(ctx):
    """List all courses with metrics."""
    from modules.courses.module import CoursesModule

    try:
        module = CoursesModule()
        data = module.get_simulated_data()
        output_result(data["courses"], ctx.obj["output"])
        success(f"Found {len(data['courses'])} courses")
    except Exception as e:
        error(f"Failed to list courses: {e}")


@courses.command("metrics")
@click.pass_context
def course_metrics(ctx):
    """Get course metrics summary."""
    from modules.courses.module import CoursesModule

    try:
        module = CoursesModule()
        data = module.get_simulated_data()
        metrics = {
            "total_revenue": sum(c["revenue"] for c in data["courses"]),
            "total_students": sum(c["students"] for c in data["courses"]),
            "avg_rating": sum(c["rating"] for c in data["courses"])
            / len(data["courses"]),
            "course_count": len(data["courses"]),
        }
        output_result(metrics, ctx.obj["output"])
        success("Metrics calculated")
    except Exception as e:
        error(f"Failed to get metrics: {e}")


@courses.command("revenue")
@click.option(
    "--period",
    "-p",
    default="month",
    type=click.Choice(["month", "year", "all"]),
    help="Time period",
)
@click.pass_context
def course_revenue(ctx, period):
    """Get revenue breakdown by course."""
    from modules.courses.module import CoursesModule

    try:
        module = CoursesModule()
        data = module.get_simulated_data()

        revenue_data = []
        for course in data["courses"]:
            revenue_data.append(
                {
                    "course": course["title"],
                    "revenue": course["revenue"],
                    "students": course["students"],
                    "rating": course["rating"],
                }
            )

        total = sum(r["revenue"] for r in revenue_data)
        revenue_data.append(
            {"course": "TOTAL", "revenue": total, "students": "-", "rating": "-"}
        )

        output_result(revenue_data, ctx.obj["output"])
        success(f"Total revenue: ${total:,}")
    except Exception as e:
        error(f"Failed to get revenue: {e}")


@courses.command("top")
@click.option(
    "--by",
    "-b",
    default="revenue",
    type=click.Choice(["revenue", "students", "rating"]),
    help="Sort by field",
)
@click.option("--limit", "-l", default=5, help="Number of courses")
@click.pass_context
def top_courses(ctx, by, limit):
    """Get top performing courses."""
    from modules.courses.module import CoursesModule

    try:
        module = CoursesModule()
        data = module.get_simulated_data()

        sorted_courses = sorted(data["courses"], key=lambda x: x[by], reverse=True)[
            :limit
        ]

        if ctx.obj["output"] == "json":
            output_result(sorted_courses, "json")
        else:
            click.echo(
                click.style(
                    f"\n=== TOP {limit} COURSES BY {by.upper()} ===",
                    fg="cyan",
                    bold=True,
                )
            )
            for i, course in enumerate(sorted_courses, 1):
                click.echo(f"\n{i}. {click.style(course['title'], fg='yellow')}")
                click.echo(f"   Revenue: ${course['revenue']:,}")
                click.echo(f"   Students: {course['students']:,}")
                click.echo(f"   Rating: {course['rating']}/5.0")
                click.echo(f"   Status: {click.style(course['status'], fg='green')}")

            success("Top courses retrieved")
    except Exception as e:
        error(f"Failed to get top courses: {e}")
