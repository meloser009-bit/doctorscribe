"""
Follow-up Question Agent
"""

import json

from agents.llm import ask_llm
from prompts import FOLLOWUP_PROMPT


def generate_followup(clinical_data, missing_fields):

    payload = {
        "clinical_data": clinical_data,
        "missing": missing_fields
    }

    response = ask_llm(
        system_prompt=FOLLOWUP_PROMPT,
        user_prompt=json.dumps(payload, indent=2)
    )

    return json.loads(response)