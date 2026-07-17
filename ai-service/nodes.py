"""
LangGraph Nodes
"""

from state import ConsultationState

from agents.extractor import extract_information
from agents.priority import assess_priority
from agents.missing import find_missing_information
from agents.followup import generate_followup
from agents.summary import generate_summary


# ==========================================================
# Extractor Node
# ==========================================================

def extractor_node(state: ConsultationState):

    new_message = {
        "role": "user",
        "content": state["latest_message"]
    }

    # Existing conversation
    existing_conversation = state.get("conversation", [])

    # Temporary conversation used for extraction
    full_conversation = existing_conversation + [new_message]

    conversation_text = "\n".join(
        msg["content"]
        for msg in full_conversation
    )

    extracted = extract_information(conversation_text)

    return {
        # Because conversation uses a reducer (Annotated[..., add]),
        # LangGraph will append this message automatically.
        "conversation": [new_message],

        "extracted_data": extracted
    }


# ==========================================================
# Priority Node
# ==========================================================

def priority_node(state: ConsultationState):

    priority = assess_priority(
        state["extracted_data"]
    )

    return {
        "priority": priority
    }


# ==========================================================
# Missing Information Node
# ==========================================================

def missing_node(state: ConsultationState):

    missing = find_missing_information(
        state["extracted_data"]
    )

    return {
        "missing_information": missing["missing_information"]
    }


# ==========================================================
# Follow-up Question Node
# ==========================================================

def followup_node(state: ConsultationState):

    followup = generate_followup(
        state["extracted_data"],
        state["missing_information"]
    )

    return {
        "followup_question": followup["question"],
        "summary": ""
    }


# ==========================================================
# Summary Node
# ==========================================================

def summary_node(state: ConsultationState):

    summary = generate_summary(
        state["extracted_data"]
    )

    return {
        "summary": summary["summary"],
        "followup_question": ""
    }