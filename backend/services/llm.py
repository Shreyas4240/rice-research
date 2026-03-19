"""
LLM client wrapper — uses Together AI when TOGETHER_API_KEY is set,
falls back to mock/stub responses automatically when not set.
Also supports Gemini API for specific use cases.
"""
import os
import json

_together_client = None
_gemini_client = None
MOCK_MODE = not bool(os.getenv("TOGETHER_API_KEY"))
GEMINI_MOCK_MODE = not bool(os.getenv("GEMINI_API_KEY"))

# Debug: Print which APIs are available
print(f"[LLM] TOGETHER_API_KEY available: {bool(os.getenv('TOGETHER_API_KEY'))}")
print(f"[LLM] GEMINI_API_KEY available: {bool(os.getenv('GEMINI_API_KEY'))}")
print(f"[LLM] MOCK_MODE: {MOCK_MODE}")
print(f"[LLM] GEMINI_MOCK_MODE: {GEMINI_MOCK_MODE}")
TOGETHER_MODEL = "ServiceNow-AI/Apriel-1.6-15b-Thinker"
GEMINI_MODEL = "gemma-3-4b-it"

def _get_together_client():
    global _together_client
    if _together_client is None:
        from together import Together
        _together_client = Together()
    return _together_client

def _get_gemini_client():
    global _gemini_client
    if _gemini_client is None:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        _gemini_client = genai.GenerativeModel(GEMINI_MODEL)
    return _gemini_client


def chat(system: str, user: str, max_tokens: int = 1024) -> str:
    """Call Together AI and return the response text. Falls back to empty string in mock mode."""
    if MOCK_MODE:
        raise RuntimeError("LLM not available: TOGETHER_API_KEY is not set.")
    client = _get_together_client()
    response = client.chat.completions.create(
        model=TOGETHER_MODEL,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )
    return response.choices[0].message.content


def chat_gemini(system: str, user: str, max_tokens: int = 1024) -> str:
    """Call Gemini API and return the response text. Falls back to empty string in mock mode."""
    if GEMINI_MOCK_MODE:
        raise RuntimeError("Gemini not available: GEMINI_API_KEY is not set.")
    client = _get_gemini_client()
    
    # Combine system and user messages for Gemini
    combined_prompt = f"System: {system}\n\nUser: {user}"
    
    response = client.generate_content(
        combined_prompt,
        generation_config={
            "max_output_tokens": max_tokens,
            "temperature": 0.7,
        }
    )
    return response.text


def chat_json(system: str, user: str, max_tokens: int = 1024) -> dict:
    """Call Together AI and parse the JSON response."""
    text = chat(system, user, max_tokens)
    # Strip markdown code fences if present
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0].strip()
    return json.loads(text)


def chat_gemini_json(system: str, user: str, max_tokens: int = 1024) -> dict:
    """Call Gemini API and parse the JSON response."""
    text = chat_gemini(system, user, max_tokens)
    # Strip markdown code fences if present
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0].strip()
    return json.loads(text)
