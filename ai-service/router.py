"""
Routing logic for LangGraph.
"""

from state import ConsultationState


def route_after_missing(state: ConsultationState):

    if state["missing_information"]:
        return "followup"

    return "summary"