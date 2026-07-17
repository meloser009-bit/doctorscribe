"""
SOAP Note Generator
"""

import json

from agents.llm import ask_llm
from prompts import SOAP_PROMPT


def generate_soap(clinical_data):

    response = ask_llm(
        system_prompt=SOAP_PROMPT,
        user_prompt=json.dumps(clinical_data, indent=2)
    )

    return json.loads(response)