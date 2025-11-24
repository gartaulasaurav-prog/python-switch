from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .ai_client import summarize_text
from .database import create_db_and_tables
from .crud import save_summary, get_all_summaries




app = FastAPI()
@app.on_event("startup")
def on_startup():
    """
    This function runs once when the FastAPI app starts.

    It tells SQLModel to create all tables defined in our models
    (like the Summary table) if they don't already exist.
    """
    create_db_and_tables()


templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/summarize", response_class=HTMLResponse)
async def summarize(
    request: Request,
    text: str = Form(...),
    length: str = Form("medium"),
):
    """
    Handle the form submission from the HTML page.
    """

    # 1) Convert the selected length into a max_words value
    if length == "short":
        max_words = 40
    elif length == "long":
        max_words = 200
    else:
        max_words = 80

    # 2) Call the AI helper – with error handling
    try:
        result_text = summarize_text(text, max_words=max_words)
    except Exception:
        result_text = (
            "Sorry, something went wrong while generating the summary. "
            "Please try again in a moment."
        )

    # 3) Save to the database (best-effort)
    try:
        save_summary(
            original_text=text,
            summary_text=result_text,
            length=length,
        )
    except Exception:
        # For now we silently ignore DB errors so the app still works
        # even if the DB has a problem.
        pass

    # 4) Render the template as before
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "original_text": text,
            "result": result_text,
            "length": length,
            "max_words": max_words,
        }
    )

@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):
    summaries = get_all_summaries()

    return templates.TemplateResponse(
        "history.html",
        {
            "request": request,
            "summaries": summaries
        }
    )

