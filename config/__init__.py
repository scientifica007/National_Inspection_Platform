"""Project configuration package for the National Inspection Platform."""

from pathlib import Path

from dotenv import load_dotenv

# Load the repository-root `.env` (if present) before settings read the
# environment. `.env` is git-ignored; only `.env.example` is versioned.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
