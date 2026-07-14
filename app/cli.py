import click

from app.seeders import seed_database


def register_cli_commands(flask_app):
    @flask_app.cli.command("seed")
    def seed():
        """Seed default roles and sample users."""
        result = seed_database()
        click.echo(
            "Seed complete: "
            f"{result['roles']} roles, "
            f"admin={result['admin']}, "
            f"student={result['student']}, "
            f"faculty={result['faculty']}"
        )
