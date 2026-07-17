"""
Summary Agent
"""

import json

from agents.llm import ask_llm
from prompts import SUMMARY_PROMPT


def generate_summary(clinical_data):

    response = ask_llm(
        system_prompt=SUMMARY_PROMPT,
        user_prompt=json.dumps(clinical_data, indent=2)
    )

    return json.loads(response)