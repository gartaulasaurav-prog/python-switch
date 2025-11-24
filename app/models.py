from datetime import datetime
from sqlmodel import SQLModel, Field

class Summary(SQLModel, table=True):
    """
    Represents one saved summary in the database.

    Each row in the "summary" table will have:
    - an id
    - the original text
    - the summarized text
    - the chosen length option
    - when it was created
    """

    id: int | None = Field(default=None, primary_key=True)
    original_text: str = Field(index=True)
    summary_text: str
    length: str = Field(default="medium")
    created_at: datetime = Field(default_factory=datetime.utcnow)