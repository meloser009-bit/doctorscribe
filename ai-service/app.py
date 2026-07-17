from flask import Flask, request, jsonify

from workflow import graph

app = Flask(__name__)

# ==========================================
# In-memory session storage
# ==========================================

# Stores each consultation using a session_id
sessions = {}


# ==========================================
# Default Consultation State
# ==========================================

def create_new_state():
    return {
        "conversation": [],
        "latest_message": "",
        "extracted_data": {},
        "priority": {},
        "missing_information": [],
        "followup_question": "",
        "summary": "",
        "soap_note": {},
        "consultation_completed": False,
    }


# ==========================================
# Chat Endpoint
# ==========================================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    # -----------------------------
    # Validate Request
    # -----------------------------
    if not data:
        return jsonify({
            "error": "Request body is missing."
        }), 400

    if "session_id" not in data:
        return jsonify({
            "error": "session_id is required."
        }), 400

    if "message" not in data:
        return jsonify({
            "error": "message is required."
        }), 400

    session_id = data["session_id"]
    message = data["message"]

    # -----------------------------
    # Create session if new
    # -----------------------------
    if session_id not in sessions:
        sessions[session_id] = create_new_state()

    state = sessions[session_id]

    # Update latest message
    state["latest_message"] = message

    try:

        result = graph.invoke(state)

        # Save updated state
        sessions[session_id] = result

        # Return only required fields
        return jsonify({

            "priority": result.get("priority", {}),

            "extracted_data": result.get("extracted_data", {}),

            "missing_information": result.get(
                "missing_information",
                []
            ),

            "followup_question": result.get(
                "followup_question",
                ""
            ),

            "summary": result.get(
                "summary",
                ""
            ),

            "consultation_completed": result.get(
                "consultation_completed",
                False
            )

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# Finalize / SOAP Note Endpoint
# ==========================================

@app.route("/finalize", methods=["POST"])
def finalize():
    data = request.get_json()

    # -----------------------------
    # Validate Request
    # -----------------------------
    if not data:
        return jsonify({
            "error": "Request body is missing."
        }), 400

    if "session_id" not in data:
        return jsonify({
            "error": "session_id is required."
        }), 400

    session_id = data["session_id"]

    # Check if the active session exists
    if session_id not in sessions:
        return jsonify({
            "error": "Active session not found. Start a chat session first."
        }), 404

    state = sessions[session_id]

    try:
        # Run final state compilation through your graph workflow matrix
        result = graph.invoke(state)
        
        # Save finalized state
        sessions[session_id] = result

        # Return targeted elements required for the SOAP targets mapping
        return jsonify({
            "summary": result.get("summary", ""),
            "soap_note": result.get("soap_note", {
                "S": "",
                "O": "",
                "A": "",
                "P": ""
            })
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# Health Check Endpoint
# ==========================================

@app.route("/", methods=["GET"])
def health():

    return jsonify({
        "status": "running",
        "service": "Clinical AI Agent",
        "version": "1.0"
    })


# ==========================================
# Run Flask
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)
