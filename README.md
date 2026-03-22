# 🎬 ShortFlix

ShortFlix is a streamlined, fast-loading discovery platform designed to alleviate decision fatigue for short film viewing. With beautifully curated genres, users can click what they are in the mood for and immediately dive into high-quality open-source and cinematic short films without leaving the platform.

## Features
- **Instant Discovery:** 5 massive genre categories (Sci-Fi, Romantic, Intense, Comedy, Casual).
- **Curated Selection:** Filters movies instantly by length (Under 10 mins, 10-20 mins) to adapt to the user's free time.
- **In-App Streaming:** Natively streams HD YouTube short films right inside the UI; no pop-ups, no external tabs.
- **Cinematic Aesthetic:** Completely tailored True Black Dark Mode UI utilizing Deep Purple accents, plush 3D button hovering effects, and rounded cinematic cards.

## Installation & Setup

1. Ensure you have Python installed globally.
2. Open your terminal in the root directory.
3. Install the primary required dependencies:
```bash
pip install streamlit
```
4. Run the application locally via the Streamlit server:
```bash
streamlit run app.py
```
5. ShortFlix will automatically open in your browser at `http://localhost:8501`.

## Technologies Used
- **Frontend & State Routing**: [Streamlit](https://streamlit.io/)
- **Data Engine**: Python dictionaries (`data.py`) mapped to verified, functioning Open-Source Cinema YouTube endpoints.
- **UI System**: Raw CSS injected into Streamlit to override baseweb themes and build native responsive grid layouts.
