from typing import Annotated, TypedDict, List, Dict, Any
from operator import add


class ConsultationState(TypedDict):

    conversation: Annotated[List[Dict[str, str]], add]

    latest_message: str

    extracted_data: Dict[str, Any]

    priority: Dict[str, Any]

    missing_information: List[str]

    followup_question: str

    summary: str

    soap_note: Dict[str, Any]

    consultation_completed: bool