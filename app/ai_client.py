import os
from dotenv import load_dotenv
from google import genai

# Load .env file so GEMINI_API_KEY is in the environment
load_dotenv()

# Create a single global client; it will read GEMINI_API_KEY from env
client = genai.Client()

DEFAULT_MODEL = "gemini-2.5-flash-lite"  # good fast model for text tasks


def summarize_text(text: str, max_words: int = 120) -> str:
    """
    Call Gemini to summarize the given text in at most max_words words.
    """
    if not text or not text.strip():
        return "No text provided."

    prompt = (
        "You are a concise, helpful summarization assistant.\n\n"
        f"Summarize the following text in at most {max_words} words.\n"
        "Preserve the key points and main ideas. Use simple language.\n\n"
        f"Text:\n{text}"
    )

    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
    )
    # The SDK gives a response with .text helper to extract main text. :contentReference[oaicite:4]{index=4}
    return response.text
