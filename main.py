from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# Allow your GUI app to read this API safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    # A read-only API endpoint returning dynamic data
    quotes = [
        "Simplify, then add lightness.",
        "Make it work, make it right, make it fast.",
        "Before software can be reusable it first has to be usable.",
        "Computers are good at following instructions, but not at reading your mind."
    ]
    return {
        "status": "online",
        "api_type": "Read-Only Cloud API",
        "quote_of_the_day": random.choice(quotes)
    }