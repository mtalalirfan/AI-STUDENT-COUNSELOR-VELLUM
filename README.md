# Avenor — Study Abroad Assessment

Premium dossier-themed Streamlit app: an 11-section suitability questionnaire, a university
ranking comparator (QS / THE / ARWU / US News / CWUR), and a Gemini-generated dossier with
Markdown, PDF, and mailto export.

## Run locally

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # add your Gemini key, optional
streamlit run app.py
```

Without a Gemini key the app still runs — it falls back to a local heuristic preview so the
flow can be demoed end to end, then clearly labels the result as a placeholder.

## Files

- `app.py` — navigation, questionnaire flow, comparator, dossier rendering
- `theme.py` — the navy/brass/teal/crimson glass CSS, gradient drift + stamp-reveal animations
- `questions.py` — the 11 assessment sections (merged from the original 16 to cut fatigue)
- `rankings_data.py` — sample ranking dataset + comparator helpers. **The bundled ranks are
  illustrative sample data for demo purposes.** Swap in real figures by dropping a `rankings.csv`
  next to this file with columns `University,Country,QS,THE,ARWU,US News,CWUR` — it's picked up
  automatically over the sample data.
- `gemini_client.py` — calls `gemini-flash-latest` (Google's rolling alias for the current GA
  Flash model) with `responseMimeType: application/json` for a structured dossier.
- `report_generator.py` — Markdown and PDF (reportlab) renderers for the final dossier.

## Deploy to Streamlit Community Cloud

1. Push this folder to a GitHub repo.
2. On share.streamlit.io, point to `app.py`.
3. In app settings → Secrets, paste `GEMINI_API_KEY = "..."`.

## Notes

- Email handoff is a `mailto:` link (no SMTP/OAuth), pre-filled with subject + a truncated
  body — mail clients cap URL length, so the PDF has to be attached manually. This is called out
  in the UI.
- The comparator's composite score is the mean rank across whichever sources have data for a
  given university (lower is better).
