import streamlit as st
import random
import re
import os
from dotenv import load_dotenv
from data import get_films

# Load local .env variables
load_dotenv()

# API Clients (will use if keys are provided)
try:
    from googleapiclient.discovery import build
    from groq import Groq
except ImportError:
    pass

def get_yt_id(url):
    """Extracts the YouTube video ID from a URL."""
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_thumb(url):
    """Generates the mqdefault thumbnail URL (more reliable than hqdefault)."""
    video_id = get_yt_id(url)
    if video_id:
        return f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
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
if 'use_live_api' not in st.session_state:
    st.session_state.use_live_api = False

# Sidebar for API Settings
with st.sidebar:
    st.title("⚙️ API Settings")
    # Priority: 1. Manual User Input, 2. ENV File, 3. None
    env_yt = os.getenv("YOUTUBE_API_KEY", "")
    env_groq = os.getenv("GROQ_API_KEY", "")
    
    yt_key = st.text_input("YouTube API Key", value=env_yt, type="password", help="To fetch live shorts directly from YouTube.")
    groq_key = st.text_input("Groq API Key", value=env_groq, type="password", help="For AI-powered catchy summaries.")
    
    st.session_state.yt_api_key = yt_key if yt_key else None
    st.session_state.groq_api_key = groq_key if groq_key else None
    
    if st.session_state.yt_api_key:
        st.session_state.use_live_api = st.checkbox("Enable Live Discovery", value=False, help="Switch between hand-picked classics and live YouTube discovery.")
        st.success("YouTube API Connected!")
    
    st.divider()
    st.markdown("Developed by **ShortFlix Labs**")

st.session_state.all_films = get_films()

# API Helpers
def get_ai_summary(title, description):
    if not st.session_state.groq_api_key:
        return description[:100] + "..." if description else "A intriguing cinematic short film."
    
    try:
        client = Groq(api_key=st.session_state.groq_api_key)
        prompt = f"Write a 1-sentence, highly engaging hook summary for a film titled '{title}' with description: '{description}'. Key rules: Catchy, curious, max 15 words."
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except:
        return description[:80] + "..."

def fetch_live_films(genre):
    if not st.session_state.yt_api_key:
        return []
    
    try:
        youtube = build("youtube", "v3", developerKey=st.session_state.yt_api_key)
        # Broadening query and removing restrictive duration for better discovery
        search_query = f"{genre} short film"
        request = youtube.search().list(
            q=search_query,
            part="snippet",
            maxResults=15,
            type="video",
            relevanceLanguage="en",
            safeSearch="moderate"
        )
        response = request.execute()
        
        live_films = []
        for item in response.get("items", []):
            vid_id = item["id"]["videoId"]
            snippet = item["snippet"]
            
            # Use Groq if available for summary
            summary = get_ai_summary(snippet["title"], snippet["description"])
            
            live_films.append({
                "id": vid_id,
                "title": snippet["title"],
                "youtube_url": f"https://www.youtube.com/watch?v={vid_id}",
                "genre": genre,
                "duration": "??", # Search API doesn't give duration instantly without another call
                "summary": summary,
                "thumbnail": f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg",
                "is_verified": True
            })
        return live_films
    except Exception as e:
        st.error(f"API Error: {e}")
        return []

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
                
                # Dynamic Fetching Logic
                films = []
                if st.session_state.use_live_api:
                    with st.spinner(f"🚀 Discovering live {g} shorts..."):
                        films = fetch_live_films(g)
                    if not films:
                        st.info("No live results found. Showing our hand-picked collection instead.")
                        films = [f for f in st.session_state.all_films if f['genre'] == g]
                else:
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
        st.warning("No films found for this genre. If using Live API, try again in a moment.")
    else:
        # Select next 3 unique films
        start = st.session_state.rec_index
        end = start + 3
        
        # If we reached the end, loop back or re-shuffle
        if start >= len(filtered):
            if not st.session_state.use_live_api:
                random.shuffle(st.session_state.filtered_films)
            st.session_state.rec_index = 0
            start = 0
            end = 3
            filtered = st.session_state.filtered_films

        current_recs = filtered[start:end]
        st.session_state.rec_list = current_recs
            
        # Display in columns (3)
        num_cols = len(current_recs)
        if num_cols > 0:
            cols = st.columns(3) # Explicitly use 3 columns
            for idx, vid in enumerate(current_recs):
                # Calculate real index in filtered list
                real_idx = start + idx
                with cols[idx]:
                    st.markdown('<div class="film-card">', unsafe_allow_html=True)
                    # Use get_thumb helper for EVERY rendering to ensure reliability
                    thumb_url = get_thumb(vid['youtube_url'])
                    st.image(thumb_url, use_column_width=True)
                    st.markdown(f"#### {vid['title']}")
                    st.markdown(f"**⏱ {vid['duration']} min**")
                    st.write(vid['summary'])
                    st.button(f"▶ Play", key=f"play_{vid['id']}", on_click=go_video, args=(vid, real_idx), type="primary", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        st.write("")
        if st.button("🔄 Show another 3", use_container_width=True):
            st.session_state.rec_index += 3
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
