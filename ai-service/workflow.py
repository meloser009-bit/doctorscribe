"""
LangGraph Workflow
"""

from langgraph.graph import StateGraph, END

from state import ConsultationState
from nodes import (
    extractor_node,
    priority_node,
    missing_node,
    followup_node,
    summary_node
)
from router import route_after_missing


# Create the graph
builder = StateGraph(ConsultationState)

# ==========================
# Add Nodes
# ==========================

builder.add_node("extractor", extractor_node)
builder.add_node("priority", priority_node)
builder.add_node("missing", missing_node)
builder.add_node("followup", followup_node)
builder.add_node("summary", summary_node)

# ==========================
# Entry Point
# ==========================

builder.set_entry_point("extractor")

# ==========================
# Linear Flow
# ==========================

builder.add_edge("extractor", "priority")
builder.add_edge("priority", "missing")

# ==========================
# Conditional Routing
# ==========================

builder.add_conditional_edges(
    "missing",
    route_after_missing,
    {
        "followup": "followup",
        "summary": "summary"
    }
)

# ==========================
# End Nodes
# ==========================

builder.add_edge("followup", END)
builder.add_edge("summary", END)

# ==========================
# Compile Graph
# ==========================

graph = builder.compile()