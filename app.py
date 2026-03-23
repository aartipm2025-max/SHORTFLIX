import streamlit as st
import random
import re
import os
from concurrent.futures import ThreadPoolExecutor
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

def parse_duration(duration_str):
    """Parses ISO 8601 duration (PT#M#S) into total integer minutes."""
    if not duration_str:
        return 0
    # ISO 8601 parsing via regex
    match = re.search(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        return 0
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0
    return (hours * 60) + minutes + (1 if seconds > 30 else 0)

def get_yt_id(url):
    """Extracts the YouTube video ID from a URL."""
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_thumb(url):
    """Extracts high quality YouTube thumbnail with hqdefault fallback."""
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
        box-shadow: 0 4px 6px rgba(0,0,0,0.5);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        color: var(--primary-text);
        position: relative;
        overflow: hidden;
    }
    
    .film-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: var(--primary-color);
        box-shadow: 0 12px 24px rgba(108, 92, 231, 0.2);
    }
    
    .film-card p, .film-card .stMarkdown p {
        color: var(--secondary-text) !important;
        font-size: 0.9rem;
        line-height: 1.4;
    }

    /* Duration Tag */
    .duration-tag {
        background-color: rgba(108, 92, 231, 0.2);
        color: var(--primary-color);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
    }
    
    /* Discovery Indicator */
    .discovery-indicator {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(0,0,0,0.7);
        padding: 2px 8px;
        border-radius: 4px;
        border: 1px solid #FF4B4B;
        z-index: 10;
        backdrop-filter: blur(4px);
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
if 'duration_filter' not in st.session_state:
    st.session_state.duration_filter = "All"

# Automatic API Configuration (no user input needed)
st.session_state.yt_api_key = os.getenv("YOUTUBE_API_KEY")
st.session_state.groq_api_key = os.getenv("GROQ_API_KEY")

# Sidebar - Disabled for cinematic fullscreen experience
# with st.sidebar:
#     st.title("🎬 ShortFlix")


# API Helpers
@st.cache_data(ttl=3600) # Cache summaries for 1 hour
def process_video_metadata(title, description, api_key):
    """Translates title to English and generates a 2-line catchy summary."""
    if not api_key:
        return title, description[:100] + "..." if description else "An amazing cinematic short film."
    
    try:
        client = Groq(api_key=api_key)
        prompt = (
            f"Video Title: '{title}'\n"
            f"Description: '{description[:800]}'\n\n"
            "INSTRUCTIONS:\n"
            "1. Translate the title above to English if it is in another language. Keep the original vibe.\n"
            "2. Write a 2-line summary (under 40 words total) about why this film is absolutely amazing and must-watch.\n\n"
            "Return the result EXACTLY in this format:\n"
            "ENG_TITLE: [The English Title]\n"
            "ENG_SUMMARY: [The 2-line summary]"
        )
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are a cinematic curator. Always follow the requested format perfectly."},
                      {"role": "user", "content": prompt}],
            temperature=0.5
        )
        response_text = completion.choices[0].message.content
        print(f"DEBUG: Groq Response for '{title}':\n{response_text}")
        
        en_title = title
        summary = description[:100] + "..."
        
        # Robust parsing for TITLE
        if "ENG_TITLE:" in response_text:
            en_title = response_text.split("ENG_TITLE:")[1].split("\n")[0].strip()
        
        # Robust parsing for SUMMARY
        if "ENG_SUMMARY:" in response_text:
            summary = response_text.split("ENG_SUMMARY:")[1].strip()
            
        return en_title, summary
    except Exception as e:
        print(f"DEBUG: Groq Error: {e}")
        return title, description[:100] + "..." if description else "An amazing cinematic short film."


def fetch_live_films(genre):
    """Fetches high quality live shorts with parallelized metadata processing and multi-level caching."""
    # Pure YouTube discovery - bypasses local curated dataset entirely as requested
    if not st.session_state.yt_api_key:
        return []
    
    try:
        youtube = build("youtube", "v3", developerKey=st.session_state.yt_api_key)
        # Search query refined for English content specifically
        search_query = f'"{genre}" short film English'
        request = youtube.search().list(
            q=search_query,
            part="snippet",
            maxResults=15, # Increased for better selection pool
            type="video",
            relevanceLanguage="en",
            regionCode="US", 
            safeSearch="moderate"
        )
        response = request.execute()
        
        video_ids = [item["id"]["videoId"] for item in response.get("items", [])]
        if not video_ids:
            return []
            
        # Batch fetch video details
        vid_req = youtube.videos().list(
            id=",".join(video_ids),
            part="snippet,contentDetails"
        )
        vid_resp = vid_req.execute()
        
        # Parallel Metadata Processing
        def process_item(item):
            vid_id = item["id"]
            snippet = item["snippet"]
            content_details = item["contentDetails"]
            
            # Use cached metadata processor
            en_title, summary = process_video_metadata(snippet["title"], snippet["description"], st.session_state.groq_api_key)
            
            # Duration parse
            raw_dur = content_details.get("duration", "PT0M0S")
            duration_min = parse_duration(raw_dur)
            
            return {
                "id": vid_id,
                "title": en_title,
                "youtube_url": f"https://www.youtube.com/watch?v={vid_id}",
                "genre": genre,
                "duration": duration_min, 
                "summary": summary,
                "thumbnail": get_thumb(f"https://www.youtube.com/watch?v={vid_id}"),
                "is_verified": True,
                "is_live": True
            }

        with ThreadPoolExecutor(max_workers=5) as executor:
            p_results = list(executor.map(process_item, vid_resp.get("items", [])))
        
        live_films = [r for r in p_results if r is not None]
        
        # Return pure YouTube results
        random.shuffle(live_films)
        return live_films[:25]
        
    except Exception as e:
        print(f"DEBUG: API Error: {e}")
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
                
                # Exclusively use YouTube Discovery
                with st.spinner(f"🚀 Discovering live {g} shorts..."):
                    st.session_state.filtered_films = fetch_live_films(g)
                
                if not st.session_state.filtered_films:
                    st.error("Could not find any live shorts for this genre. Please check your YouTube API configuration.")
                else:
                    st.session_state.rec_index = 0
                    st.rerun()


# RECOMMENDATIONS PAGE
elif st.session_state.page == 'RECOMMENDATIONS':
    # Filter UI
    col_f1, col_f2 = st.columns([1, 4])
    with col_f1:
        st.button("← Back", on_click=go_home, use_container_width=True)
    with col_f2:
        # Styled Pills / Tabs for Filter
        options = ["All", "Short (<5m)", "Medium (5-15m)", "Long (15m+)"]
        selection = st.radio("Duration", options, horizontal=True, label_visibility="collapsed")
        if selection != st.session_state.duration_filter:
            st.session_state.duration_filter = selection
            st.session_state.rec_index = 0
            st.rerun()

    st.markdown(f"<h1 style='text-align: center; margin-top: -20px; margin-bottom: 20px;'>🍿 {st.session_state.genre} Shorts</h1>", unsafe_allow_html=True)
    
    # Filtering logic
    all_discovered = st.session_state.filtered_films
    
    if st.session_state.duration_filter == "Short (<5m)":
        filtered = [f for f in all_discovered if f['duration'] < 5]
    elif st.session_state.duration_filter == "Medium (5-15m)":
        filtered = [f for f in all_discovered if 5 <= f['duration'] <= 15]
    elif st.session_state.duration_filter == "Long (15m+)":
        filtered = [f for f in all_discovered if f['duration'] > 15]
    else:
        filtered = all_discovered

    if not filtered:
        st.warning("No films found for this genre. If using Live API, try again in a moment.")
    else:
        # Select next 3 unique films
        start = st.session_state.rec_index
        end = start + 3
        
        # If we reached the end, loop back or re-shuffle
        if start >= len(filtered):
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
                    if vid.get('is_live'):
                        st.markdown("<div class='discovery-indicator'><span style='color: #FF4B4B; font-size: 10px; font-weight: bold;'>🔴 LIVE</span></div>", unsafe_allow_html=True)
                    
                    # Use get_thumb helper for EVERY rendering to ensure reliability
                    thumb_url = get_thumb(vid['youtube_url'])
                    st.image(thumb_url, use_column_width=True)
                    
                    st.markdown(f"<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                    st.markdown(f"#### {vid['title']}")
                    st.markdown(f"<div class='duration-tag'>⏱ {vid['duration']} mins</div>", unsafe_allow_html=True)
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
    st.markdown(f"<div class='duration-tag'>⏱ {vid['duration']} mins | {vid['genre']}</div>", unsafe_allow_html=True)
    st.write(f"<div style='margin-top: 10px; color: #9CA3AF;'>{vid['summary']}</div>", unsafe_allow_html=True)
    
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
