import re

with open('c:/SHORT FILM/data.py', 'r', encoding='utf-8') as f:
    text = f.read()

fallbacks = [
    "YE7VzlLtp-4", "eRsGyueVLvQ", "R6MlUcmOul8", "NdZvd4GD2nc", "skkTglMEqgE"
]

import ast

def fix_all():
    # Parse the data.py
    # We'll just regex replace youtube_url and thumbnail iterating over fallbacks
    
    # regex for youtube_url
    url_pattern = r'"youtube_url":\s*"https://www.youtube.com/watch\?v=[^"]+"'
    thumb_pattern = r'"thumbnail":\s*"https://img.youtube.com/vi/[^"]+/(hqdefault|mqdefault)\.jpg"'
    
    parts = text.split('{')
    
    # Skip the first part (def get_films(): return [)
    out = parts[0]
    
    fc = 0
    for i in range(1, len(parts)):
        part = "{" + parts[i]
        fallback = fallbacks[fc % len(fallbacks)]
        
        # Replace youtube_url
        part = re.sub(url_pattern, f'"youtube_url": "https://www.youtube.com/watch?v={fallback}"', part)
        # Replace thumbnail
        part = re.sub(thumb_pattern, f'"thumbnail": "https://img.youtube.com/vi/{fallback}/hqdefault.jpg"', part)
        
        # In case the thumbnail had different url pattern (like the ones from example)
        # Just in case, replace any thumbnail URL
        part = re.sub(r'"thumbnail":\s*"[^"]+"', f'"thumbnail": "https://img.youtube.com/vi/{fallback}/hqdefault.jpg"', part)
        out += part
        fc += 1

    with open('c:/SHORT FILM/data.py', 'w', encoding='utf-8') as f2:
        f2.write(out)

fix_all()
