"""
Priority Agent

Determines the clinical urgency of the patient's condition.
"""

import json

from agents.llm import ask_llm
from prompts import PRIORITY_PROMPT


def assess_priority(clinical_data: dict) -> dict:

    response = ask_llm(
        system_prompt=PRIORITY_PROMPT,
        user_prompt=json.dumps(clinical_data, indent=2)
    )

    return json.loads(response)