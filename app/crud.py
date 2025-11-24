from sqlmodel import Session, select

from .database import engine
from .models import Summary


def save_summary(original_text: str, summary_text: str, length: str) -> Summary:
    """
    Create and store a Summary row in the database.
    Returns the saved Summary instance (including the auto-generated id).
    """

    # Create a database session (a connection to the DB)
    with Session(engine) as session:
        summary = Summary(
            original_text=original_text,
            summary_text=summary_text,
            length=length,
        )

        # Add it to the DB
        session.add(summary)
        session.commit()
        session.refresh(summary)   # refresh to get auto-generated id

        return summary


def get_all_summaries() -> list[Summary]:
    """
    Return every Summary row in the database, newest first.
    """
    with Session(engine) as session:
        statement = select(Summary).order_by(Summary.created_at.desc())
        results = session.exec(statement).all()
        return results