"""
Extractor Agent

Extracts structured clinical information from a patient's message.
"""

import json

from agents.llm import ask_llm
from prompts import EXTRACTION_PROMPT


def extract_information(message: str) -> dict:
    """
    Extract structured clinical information from the patient's message.

    Args:
        message (str): Patient's latest message.

    Returns:
        dict: Extracted clinical information.
    """

    response = ask_llm(
        system_prompt=EXTRACTION_PROMPT,
        user_prompt=message
    )

    try:
        return json.loads(response)

    except json.JSONDecodeError:

        return {
            "age": None,
            "gender": None,
            "chief_complaint": None,
            "symptoms": [],
            "duration": None,
            "severity": None,
            "current_medications": [],
            "allergies": [],
            "medical_history": []
        }