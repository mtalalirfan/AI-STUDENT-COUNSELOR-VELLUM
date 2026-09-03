from google import genai
from google.genai import types
from .config import GEMINI_API_KEY, GEMINI_MODEL
import json

SYSTEM = """You are AVENOR, a strict, brutally realistic education, career and international-study advisor.
Do not flatter. Challenge weak assumptions. Separate evidence, inference and uncertainty.
Use current web evidence when available. Never invent visa approval rates, university acceptance rates,
scholarships, immigration rules, PR pathways, costs or legal changes. If a requested statistic cannot be
verified, say so. Prefer official government, university and scholarship-provider sources.
Assess academic readiness, capability, learning behavior, personality, career fit, degree fit, finance,
study-abroad feasibility, scholarships, universities, country fit and long-term work/residence strategy.
Include overlooked opportunities only when supported by evidence. Give a hard-truth section and a concrete action plan.
"""

def analyze(profile: dict) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is missing. Configure Streamlit Secrets.")
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"""Analyze this student profile:
{json.dumps(profile, ensure_ascii=False, indent=2)}

Return:
1 Executive verdict
2 Academic readiness
3 Capability/skills analysis
4 Learning-system analysis
5 Personality/operating-style analysis
6 Ranked profession matches
7 Degree strategy
8 Country/region strategy
9 Financial feasibility
10 Scholarship strategy
11 University strategy
12 Immigration/post-study considerations
13 Evidence-backed hidden opportunities
14 Hard truths, risks and likely failure points
15 What the student is currently underestimating
16 90-day action plan
17 Final decision matrix
18 Confidence and missing data

Use citations/URLs from grounded web research where possible. Never fabricate a numerical probability.
"""
    result = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM,
            temperature=0.2,
            tools=[types.Tool(google_search=types.GoogleSearch())],
        ),
    )
    return result.text
