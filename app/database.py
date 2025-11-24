from sqlmodel import SQLModel, create_engine

DATABASE_URL = "sqlite:///./summaries.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,  # log SQL to the terminal so we can see what happens
)

# 👇 ADD THIS IMPORT
# Import the models so that SQLModel knows about Summary
from .models import Summary  # noqa: F401
# The "noqa" comment just tells linters: "Yes, I know this looks unused,
# but we are importing it for the side effect of registering the table."


def create_db_and_tables():
    """
    Create all tables defined as SQLModel classes.
    This runs once when the app starts.
    """
    SQLModel.metadata.create_all(engine)
