"""
Shared Groq client for all AI agents.

Every agent should import the client from here instead of
creating its own instance.
"""

import os

from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Please add it to your .env file."
    )

# Initialize Groq client
client = Groq(api_key=API_KEY)