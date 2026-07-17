"""
Missing Information Agent

Checks which required clinical fields are still missing.
"""

from schema import REQUIRED_FIELDS


def find_missing_information(clinical_data: dict) -> dict:
    missing = []

    for field, required in REQUIRED_FIELDS.items():

        if not required:
            continue

        value = clinical_data.get(field)

        if value is None:
            missing.append(field)

        elif isinstance(value, list) and len(value) == 0:
            missing.append(field)

        elif isinstance(value, str) and value.strip() == "":
            missing.append(field)

    return {
        "missing_information": missing
    }