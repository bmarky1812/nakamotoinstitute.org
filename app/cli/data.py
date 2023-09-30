import click
from flask import Blueprint

from app.cli.importers import (
    import_author,
    import_email,
    import_email_thread,
    import_episode,
    import_forum_post,
    import_forum_thread,
    import_library,
    import_mempool,
    import_mempool_series,
    import_quote,
    import_quote_category,
    import_skeptic,
    import_translator,
)
from app.cli.utils import color_text, flush_db

bp = Blueprint("data", __name__)

bp.cli.help = "Update database."


@bp.cli.command()
def seed():
    """Initialize and seed database."""
    flush_db()
    import_author()
    import_translator()
    import_email()
    import_email_thread()
    import_forum_post()
    import_forum_thread()
    import_quote_category()
    import_quote()
    import_library()
    import_mempool_series()
    import_mempool()
    import_skeptic()
    import_episode()
    click.echo(color_text("Finished importing data!"))
