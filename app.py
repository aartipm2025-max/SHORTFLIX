import streamlit as st
import random
from data import get_films

st.set_page_config(page_title="ShortFlix", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Light Theme and Card UI
st.markdown("""
<style>
    :root {
        --primary-color: #6C5CE7;
        --primary-hover: #5A4FCF;
        --secondary-color: #A78BFA;
        --accent-color: #1E1B4B;
        --background-color: #000000;
        --card-background: #111111;
        --primary-text: #FFFFFF;
        --secondary-text: #9CA3AF;
    }
    
    .stApp {
        background-color: var(--background-color);
        color: var(--primary-text);
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
    }
    
    /* Native streamli text override for proper light theme rendering */
    .stMarkdown, .stText, h1, h2, h3, h4, p {
        color: var(--primary-text) !important;
    }
    
    /* Global primary button (applied via type="primary") */
    button[kind="primary"] {
        background-color: var(--primary-color) !important;
        color: white !important;
        border-color: var(--primary-color) !important;
        border-radius: 12px;
        transition: all 0.2s;
    }
    button[kind="primary"]:hover {
        background-color: var(--primary-hover) !important;
        border-color: var(--primary-hover) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(108, 92, 231, 0.3);
    }
    
    /* Global secondary button (default streamlit buttons) */
    button[kind="secondary"] {
        background-color: var(--accent-color) !important;
        color: var(--secondary-color) !important;
        border-color: var(--accent-color) !important;
        border-radius: 12px;
        transition: all 0.2s;
    }
    button[kind="secondary"]:hover {
        background-color: #2D235D !important;
        border-color: #2D235D !important;
        transform: translateY(-2px);
    }
    
    .film-card {
        background-color: var(--card-background);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid #333333;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); /* Light soft shadow */
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
        color: var(--primary-text);
    }
    
    .film-card:hover {
        transform: scale(1.02); /* Slight scale */
        box-shadow: 0 10px 15px rgba(0,0,0,0.1); /* shadow increase */
    }
    
    .film-card p, .film-card .stMarkdown p {
        color: var(--secondary-text) !important;
    }
</style>
""", unsafe_allow_html=True)

# State Management
if 'page' not in st.session_state:
    st.session_state.page = 'HOME'
if 'genre' not in st.session_state:
    st.session_state.genre = None
if 'video' not in st.session_state:
    st.session_state.video = None
if 'rec_list' not in st.session_state:
    st.session_state.rec_list = []
if 'duration_filter' not in st.session_state:
    st.session_state.duration_filter = "All"
if 'refresh_rec' not in st.session_state:
    st.session_state.refresh_rec = True
st.session_state.all_films = get_films()

# Navigation handlers
def go_home():
    st.session_state.page = 'HOME'
    st.session_state.genre = None
    st.session_state.video = None
    st.session_state.refresh_rec = True

def go_video(vid):
    st.session_state.video = vid
    st.session_state.page = 'VIDEO'
    
def go_recs():
    st.session_state.page = 'RECOMMENDATIONS'
    st.session_state.video = None

# HOME PAGE
if st.session_state.page == 'HOME':
    st.markdown("""
    <style>
        /* Specific override for genre square buttons on Home page */
        [data-testid="stButton"] button {
            aspect-ratio: 1 / 1;
            height: auto;
            min-height: 150px;
            width: 100%;
            border-radius: 16px !important;
            border: 1px solid #333333 !important;
            background-color: #111111 !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.5) !important;
            transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s !important;
        }
        [data-testid="stButton"] button:hover {
            transform: scale(1.03) translateY(-2px) !important;
            box-shadow: 0 10px 20px rgba(108, 92, 231, 0.15) !important;
            border-color: #A78BFA !important;
            color: #6C5CE7 !important;
        }
        [data-testid="stButton"] button p {
            font-size: 24px !important;
            font-weight: bold !important;
            color: inherit !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h1 style='color: purple;'>🎬 ShortFlix</h1>
            <h3>What do you feel like watching?</h3>
            <p style='color: #9CA3AF;'>Select a genre and start watching instantly.</p>
        </div>
    """, unsafe_allow_html=True)
    
    genres = ["Sci-Fi", "Romantic", "Intense", "Comedy", "Casual"]
    
    cols = st.columns(len(genres))
    for idx, g in enumerate(genres):
        with cols[idx]:
            if st.button(g.upper(), use_container_width=True, key=f"btn_{g}"):
                st.session_state.genre = g
                st.session_state.page = 'RECOMMENDATIONS'
                st.session_state.refresh_rec = True
                st.rerun()

# RECOMMENDATIONS PAGE
elif st.session_state.page == 'RECOMMENDATIONS':
    st.button("← Back to Genres", on_click=go_home)
    st.markdown(f"<h1 style='text-align: center; margin-bottom: 5px;'>🍿 {st.session_state.genre} Shorts</h1>", unsafe_allow_html=True)
    
    # Filter Logic
    filtered = [f for f in st.session_state.all_films if f['genre'] == st.session_state.genre]

    if not filtered:
        st.warning("No films found for this genre.")
    else:
        if st.session_state.refresh_rec:
            verified = [x for x in filtered if x.get('is_verified', False)]
            unverified = [x for x in filtered if not x.get('is_verified', False)]
            random.shuffle(verified)
            random.shuffle(unverified)
            combined = verified + unverified
            
            sample_size = min(3, len(combined))
            st.session_state.rec_list = combined[:sample_size]
            st.session_state.refresh_rec = False
            
        cols = st.columns(3)
        for idx, vid in enumerate(st.session_state.rec_list):
            with cols[idx]:
                st.markdown('<div class="film-card">', unsafe_allow_html=True)
                st.image(vid['thumbnail'], use_column_width=True)
                st.markdown(f"#### {vid['title']}")
                st.markdown(f"**⏱ {vid['duration']} min**")
                st.write(vid['summary'])
                st.button(f"▶ Play", key=f"play_{vid['id']}", on_click=go_video, args=(vid,), type="primary", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        st.write("")
        if st.button("🔄 Show next 3", use_container_width=True):
            st.session_state.refresh_rec = True
            st.rerun()

# VIDEO PAGE
elif st.session_state.page == 'VIDEO':
    st.button("← Back to list", on_click=go_recs)
    vid = st.session_state.video
    
    # Standard 16:9 ratio embedded player style
    st.video(vid['youtube_url'])
    
    st.title(vid['title'])
    st.markdown(f"**⏱ {vid['duration']} min | {vid['genre']}**")
    st.write(vid['summary'])
    
    st.markdown("---")
    
    # Next video logic
    filtered = [f for f in st.session_state.all_films if f['genre'] == st.session_state.genre and f['id'] != vid['id']]

    if filtered:
        next_vid = random.choice(filtered)
        st.button("⏭ Next Film", type="primary", use_container_width=True, on_click=go_video, args=(next_vid,))
    else:
        st.info("No more films available in this genre.")
