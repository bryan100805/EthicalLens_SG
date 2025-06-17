from agno.models.google import Gemini

def get_model(model_id: str, api_key: str):
    """
    Returns an LLM instance based on model_id.
    Supports GPT, Gemini, Claude, or Groq as fallback.
    """
    model_id_lower = model_id.lower()

    # Google Gemini (via Agno)
    if "gemini" in model_id_lower:
        return Gemini(
            id="gemini-2.0-flash",
            api_key="",
            # optional flags:
            # grounding=True,
            # search=True,
            # vertexai=False,
        )

    # Fallback to Gemini 2.0 Flash
    return Gemini(
            id="gemini-2.0-flash",
            api_key="",
            # optional flags:
            # grounding=True,
            # search=True,
            # vertexai=False,
        )