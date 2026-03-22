import json

user_data = [
  {
    "id": "scifi_1",
    "title": "The OceanMaker",
    "youtube_url": "https://www.youtube.com/watch?v=8sG4xJq7Yq0",
    "genre": "Sci-Fi",
    "duration": 10,
    "summary": "A lone pilot fights to bring water back to a dying Earth."
  },
  {
    "id": "scifi_2",
    "title": "FTL",
    "youtube_url": "https://www.youtube.com/watch?v=t8LD0iUYv80",
    "genre": "Sci-Fi",
    "duration": 15,
    "summary": "Humanity’s first faster-than-light jump leads to unexpected consequences."
  },
  {
    "id": "scifi_3",
    "title": "The Black Hole",
    "youtube_url": "https://www.youtube.com/watch?v=P5_Msrdg3Hk",
    "genre": "Sci-Fi",
    "duration": 3,
    "summary": "A mysterious black hole appears on a photocopied sheet."
  },
  {
    "id": "scifi_4",
    "title": "Sight",
    "youtube_url": "https://www.youtube.com/watch?v=lK_cdkpazjI",
    "genre": "Sci-Fi",
    "duration": 8,
    "summary": "A futuristic dating system blurs the line between reality and illusion."
  },
  {
    "id": "scifi_5",
    "title": "Hyperlight",
    "youtube_url": "https://www.youtube.com/watch?v=Jw0RYlq-6k8",
    "genre": "Sci-Fi",
    "duration": 9,
    "summary": "A lone astronaut navigates survival after a catastrophic failure."
  },
  {
    "id": "comedy_1",
    "title": "Validation",
    "youtube_url": "https://www.youtube.com/watch?v=Cbk980jV7Ao",
    "genre": "Comedy",
    "duration": 16,
    "summary": "A parking attendant spreads joy through free validation."
  },
  {
    "id": "comedy_2",
    "title": "The Elevator",
    "youtube_url": "https://www.youtube.com/watch?v=Q0s5Zqmb09g",
    "genre": "Comedy",
    "duration": 5,
    "summary": "An awkward elevator ride turns hilariously unpredictable."
  },
  {
    "id": "comedy_3",
    "title": "Snack Attack",
    "youtube_url": "https://www.youtube.com/watch?v=38y_1EWIE9I",
    "genre": "Comedy",
    "duration": 5,
    "summary": "A misunderstanding over snacks leads to a surprising twist."
  },
  {
    "id": "comedy_4",
    "title": "The Gunfighter",
    "youtube_url": "https://www.youtube.com/watch?v=cWs4WA--eKU",
    "genre": "Comedy",
    "duration": 9,
    "summary": "A narrator disrupts a classic western showdown."
  },
  {
    "id": "comedy_5",
    "title": "Spider",
    "youtube_url": "https://www.youtube.com/watch?v=Zp2l9o8RrWc",
    "genre": "Comedy",
    "duration": 6,
    "summary": "A simple spider causes absolute chaos in a bathroom."
  },
  {
    "id": "romantic_1",
    "title": "Paperman",
    "youtube_url": "https://www.youtube.com/watch?v=UPA2O1pU9sE",
    "genre": "Romantic",
    "duration": 7,
    "summary": "A man tries to reconnect with a woman using paper planes."
  },
  {
    "id": "romantic_2",
    "title": "The Notebook Short",
    "youtube_url": "https://www.youtube.com/watch?v=YE7VzlLtp-4",
    "genre": "Romantic",
    "duration": 10,
    "summary": "A fleeting romance leaves a lasting emotional impact."
  },
  {
    "id": "romantic_3",
    "title": "Love at First Sight",
    "youtube_url": "https://www.youtube.com/watch?v=eRsGyueVLvQ",
    "genre": "Romantic",
    "duration": 8,
    "summary": "Two strangers connect instantly in a crowded space."
  },
  {
    "id": "romantic_4",
    "title": "Before Sunrise Short",
    "youtube_url": "https://www.youtube.com/watch?v=R6MlUcmOul8",
    "genre": "Romantic",
    "duration": 9,
    "summary": "A chance meeting leads to deep conversations overnight."
  },
  {
    "id": "romantic_5",
    "title": "The Last Letter",
    "youtube_url": "https://www.youtube.com/watch?v=NdZvd4GD2nc",
    "genre": "Romantic",
    "duration": 11,
    "summary": "A heartfelt letter rekindles a lost relationship."
  },
  {
    "id": "intense_1",
    "title": "Curve",
    "youtube_url": "https://www.youtube.com/watch?v=2dD3Fawk4y0",
    "genre": "Intense",
    "duration": 10,
    "summary": "A woman struggles to survive on a steep endless curve."
  },
  {
    "id": "intense_2",
    "title": "Cargo",
    "youtube_url": "https://www.youtube.com/watch?v=gyfmwgOV6uo",
    "genre": "Intense",
    "duration": 7,
    "summary": "A father struggles to save his baby during a zombie outbreak."
  },
  {
    "id": "intense_3",
    "title": "Lights Out",
    "youtube_url": "https://www.youtube.com/watch?v=FUQhNGEu2KA",
    "genre": "Intense",
    "duration": 3,
    "summary": "A terrifying presence appears whenever the lights go off."
  },
  {
    "id": "intense_4",
    "title": "2 AM: The Smiling Man",
    "youtube_url": "https://www.youtube.com/watch?v=_u6Tt3PqIfQ",
    "genre": "Intense",
    "duration": 5,
    "summary": "A late-night walk turns into a chilling encounter."
  },
  {
    "id": "intense_5",
    "title": "The Dollmaker",
    "youtube_url": "https://www.youtube.com/watch?v=OqSmb3n0j8o",
    "genre": "Intense",
    "duration": 9,
    "summary": "A grieving couple turns to dark magic with terrifying consequences."
  },
  {
    "id": "casual_1",
    "title": "Alike",
    "youtube_url": "https://www.youtube.com/watch?v=PDHIyrfMl_U",
    "genre": "Casual",
    "duration": 8,
    "summary": "A father and son try to preserve creativity in a rigid world."
  },
  {
    "id": "casual_2",
    "title": "Piper",
    "youtube_url": "https://www.youtube.com/watch?v=6i1q7FQ7Xn4",
    "genre": "Casual",
    "duration": 6,
    "summary": "A young bird learns to overcome fear of the ocean."
  },
  {
    "id": "casual_3",
    "title": "For the Birds",
    "youtube_url": "https://www.youtube.com/watch?v=hnX0F0D0j9k",
    "genre": "Casual",
    "duration": 3,
    "summary": "Small birds learn a lesson when a big bird joins them."
  },
  {
    "id": "casual_4",
    "title": "The Present",
    "youtube_url": "https://www.youtube.com/watch?v=WjqiU5FgsYc",
    "genre": "Casual",
    "duration": 4,
    "summary": "A boy’s perspective changes after receiving an unexpected gift."
  },
  {
    "id": "casual_5",
    "title": "Kitbull",
    "youtube_url": "https://www.youtube.com/watch?v=AZS5cgybKcI",
    "genre": "Casual",
    "duration": 9,
    "summary": "An unlikely friendship forms between a stray cat and a pitbull."
  }
]

import urllib.parse

def generate_data_py():
    with open('c:/SHORT FILM/data.py', 'w', encoding='utf-8') as f:
        f.write("def get_films():\\n    return [\n")
        for i, item in enumerate(user_data):
            v_id = item['youtube_url'].split('v=')[-1].split('&')[0]
            # Use high res YT thumbnail to ensure zero CORS issues
            thumb = f"https://img.youtube.com/vi/{v_id}/mqdefault.jpg"
            item['thumbnail'] = thumb
            
            f.write("      {\n")
            keys = list(item.keys())
            for k in keys:
                val = item[k]
                if isinstance(val, str):
                    f.write(f'        "{k}": "{val}"')
                else:
                    f.write(f'        "{k}": {val}')
                if k != keys[-1]:
                    f.write(",\n")
                else:
                    f.write("\n")
            if i < len(user_data) - 1:
                f.write("      },\n")
            else:
                f.write("      }\n")
        f.write("    ]\n")

generate_data_py()
