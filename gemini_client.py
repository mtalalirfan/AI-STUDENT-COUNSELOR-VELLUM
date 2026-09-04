import json
import requests

DEFAULT_MODEL = "gemini-flash-latest"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

SYSTEM_INSTRUCTIONS = """You are the assessment engine for Avenor, a study-abroad readiness dossier.
Given a respondent's raw questionnaire answers, produce a rigorous, honest, non-flattering
assessment of their suitability for studying abroad. Be specific, cite the respondent's own
answers where relevant, and do not hedge with generic advice. Return ONLY valid JSON, no
markdown fences, no commentary, matching exactly this schema:

{
  "overall_score": integer 0-100,
  "verdict": short string, e.g. "Strong candidate" / "Promising with gaps" / "High risk without changes",
  "summary": 3-5 sentence executive summary,
  "strengths": array of 3-6 short strings,
  "risks": array of 3-6 short strings,
  "financial_reality_check": 2-4 sentence paragraph,
  "recommended_pathways": array of objects {"path": string, "why": string, "timeline": string},
  "country_fit": array of objects {"region_or_country": string, "fit_score": integer 0-100, "reason": string},
  "immediate_next_steps": array of 4-6 short imperative strings,
  "single_most_important_risk": one sentence
}
"""


def build_user_payload(answers: dict) -> str:
    lines = []
    for key, value in answers.items():
        if value in (None, "", [], "None"):
            continue
        lines.append(f"{key}: {value}")
    return "\n".join(lines)


def generate_report(answers: dict, api_key: str, model: str = DEFAULT_MODEL) -> dict:
    url = f"{API_BASE}/{model}:generateContent?key={api_key}"
    payload = {
        "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTIONS}]},
        "contents": [
            {"role": "user", "parts": [{"text": build_user_payload(answers)}]}
        ],
        "generationConfig": {
            "temperature": 0.4,
            "responseMimeType": "application/json",
        },
    }
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)
