import streamlit as st
import random
import re
from data import get_films

def get_yt_id(url):
    """Extracts the YouTube video ID from a URL."""
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_thumb(url):
    """Generates the hqdefault thumbnail URL with a fallback."""
    video_id = get_yt_id(url)
    if video_id:
        return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    return "https://via.placeholder.com/400x225?text=No+Thumbnail"

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
if 'filtered_films' not in st.session_state:
    st.session_state.filtered_films = []
if 'rec_list' not in st.session_state:
    st.session_state.rec_list = []
if 'rec_index' not in st.session_state:
    st.session_state.rec_index = 0
if 'current_playing_index' not in st.session_state:
    st.session_state.current_playing_index = 0

st.session_state.all_films = get_films()

# Navigation handlers
def go_home():
    st.session_state.page = 'HOME'
    st.session_state.genre = None
    st.session_state.video = None
    st.session_state.rec_index = 0

def go_video(vid, index_in_filtered):
    st.session_state.video = vid
    st.session_state.current_playing_index = index_in_filtered
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
                # Initialize and shuffle filtered films for this genre
                films = [f for f in st.session_state.all_films if f['genre'] == g]
                random.shuffle(films)
                st.session_state.filtered_films = films
                st.session_state.rec_index = 0
                st.rerun()

# RECOMMENDATIONS PAGE
elif st.session_state.page == 'RECOMMENDATIONS':
    st.button("← Back to Genres", on_click=go_home)
    st.markdown(f"<h1 style='text-align: center; margin-bottom: 5px;'>🍿 {st.session_state.genre} Shorts</h1>", unsafe_allow_html=True)
    
    # Filter Logic
    filtered = st.session_state.filtered_films

    if not filtered:
        st.warning("No films found for this genre.")
    else:
        # Select next 5 unique films
        start = st.session_state.rec_index
        end = start + 5
        
        # If we reached the end, loop back or re-shuffle
        if start >= len(filtered):
            random.shuffle(st.session_state.filtered_films)
            st.session_state.rec_index = 0
            start = 0
            end = 5
            filtered = st.session_state.filtered_films

        current_recs = filtered[start:end]
        st.session_state.rec_list = current_recs
            
        # Display in columns (max 5)
        num_cols = len(current_recs)
        if num_cols > 0:
            cols = st.columns(num_cols)
            for idx, vid in enumerate(current_recs):
                # Calculate real index in filtered list
                real_idx = start + idx
                with cols[idx]:
                    st.markdown('<div class="film-card">', unsafe_allow_html=True)
                    # Dynamic Thumbnail extracting VIDEO_ID
                    st.image(get_thumb(vid['youtube_url']), use_column_width=True)
                    st.markdown(f"#### {vid['title']}")
                    st.markdown(f"**⏱ {vid['duration']} min**")
                    st.write(vid['summary'])
                    st.button(f"▶ Play", key=f"play_{vid['id']}", on_click=go_video, args=(vid, real_idx), type="primary", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        st.write("")
        if st.button("🔄 Show another 5", use_container_width=True):
            st.session_state.rec_index += 5
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
    filtered = st.session_state.filtered_films
    total_films = len(filtered)
    
    if total_films > 1:
        # Move to next film in the shuffled list
        next_idx = (st.session_state.current_playing_index + 1) % total_films
        next_vid = filtered[next_idx]
        
        st.button("⏭ Next Film", type="primary", use_container_width=True, on_click=go_video, args=(next_vid, next_idx))
    else:
        st.info("No other films available in this genre.")
