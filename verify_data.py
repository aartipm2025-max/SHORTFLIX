import json
import urllib.request

raw_data = """[
  {"title":"The OceanMaker","youtube_url":"https://www.youtube.com/watch?v=8sG4xJq7Yq0","genre":"sci-fi","duration":10,"summary":"A pilot fights to bring water back to Earth.","thumbnail":"https://img.youtube.com/vi/8sG4xJq7Yq0/hqdefault.jpg"},
  {"title":"FTL","youtube_url":"https://www.youtube.com/watch?v=t8LD0iUYv80","genre":"sci-fi","duration":15,"summary":"First faster-than-light jump goes wrong.","thumbnail":"https://img.youtube.com/vi/t8LD0iUYv80/hqdefault.jpg"},
  {"title":"The Black Hole","youtube_url":"https://www.youtube.com/watch?v=P5_Msrdg3Hk","genre":"sci-fi","duration":3,"summary":"A black hole appears on paper.","thumbnail":"https://img.youtube.com/vi/P5_Msrdg3Hk/hqdefault.jpg"},
  {"title":"Sight","youtube_url":"https://www.youtube.com/watch?v=lK_cdkpazjI","genre":"sci-fi","duration":8,"summary":"AR dating blurs reality.","thumbnail":"https://img.youtube.com/vi/lK_cdkpazjI/hqdefault.jpg"},
  {"title":"Hyperlight","youtube_url":"https://www.youtube.com/watch?v=Jw0RYlq-6k8","genre":"sci-fi","duration":9,"summary":"Astronaut survival mission.","thumbnail":"https://img.youtube.com/vi/Jw0RYlq-6k8/hqdefault.jpg"},
  {"title":"R'ha","youtube_url":"https://www.youtube.com/watch?v=4PUIxEWmsvI","genre":"sci-fi","duration":7,"summary":"Alien interrogation turns intense.","thumbnail":"https://img.youtube.com/vi/4PUIxEWmsvI/hqdefault.jpg"},
  {"title":"The Machine","youtube_url":"https://www.youtube.com/watch?v=2Jq23mSDh9U","genre":"sci-fi","duration":12,"summary":"AI evolves beyond control.","thumbnail":"https://img.youtube.com/vi/2Jq23mSDh9U/hqdefault.jpg"},
  {"title":"Plurality","youtube_url":"https://www.youtube.com/watch?v=IzryBRPwsog","genre":"sci-fi","duration":14,"summary":"Identity theft in digital future.","thumbnail":"https://img.youtube.com/vi/IzryBRPwsog/hqdefault.jpg"},
  {"title":"Cargo SciFi","youtube_url":"https://www.youtube.com/watch?v=9v-33jcEDk4","genre":"sci-fi","duration":6,"summary":"Cargo transport gone wrong.","thumbnail":"https://img.youtube.com/vi/9v-33jcEDk4/hqdefault.jpg"},
  {"title":"The iMom","youtube_url":"https://www.youtube.com/watch?v=9uR8t1k7Rzg","genre":"sci-fi","duration":10,"summary":"AI parenting experiment.","thumbnail":"https://img.youtube.com/vi/9uR8t1k7Rzg/hqdefault.jpg"},
  {"title":"Uncanny Valley","youtube_url":"https://www.youtube.com/watch?v=sU0oZsqeGz4","genre":"sci-fi","duration":9,"summary":"Reality simulation confusion.","thumbnail":"https://img.youtube.com/vi/sU0oZsqeGz4/hqdefault.jpg"},
  {"title":"World Builder","youtube_url":"https://www.youtube.com/watch?v=9E9Q0e6JXgA","genre":"sci-fi","duration":8,"summary":"Man builds virtual reality world.","thumbnail":"https://img.youtube.com/vi/9E9Q0e6JXgA/hqdefault.jpg"},

  {"title":"Validation","youtube_url":"https://www.youtube.com/watch?v=Cbk980jV7Ao","genre":"comedy","duration":16,"summary":"Man spreads happiness.","thumbnail":"https://img.youtube.com/vi/Cbk980jV7Ao/hqdefault.jpg"},
  {"title":"Snack Attack","youtube_url":"https://www.youtube.com/watch?v=38y_1EWIE9I","genre":"comedy","duration":5,"summary":"Snack misunderstanding twist.","thumbnail":"https://img.youtube.com/vi/38y_1EWIE9I/hqdefault.jpg"},
  {"title":"The Gunfighter","youtube_url":"https://www.youtube.com/watch?v=cWs4WA--eKU","genre":"comedy","duration":9,"summary":"Narrator ruins western duel.","thumbnail":"https://img.youtube.com/vi/cWs4WA--eKU/hqdefault.jpg"},
  {"title":"Spider","youtube_url":"https://www.youtube.com/watch?v=Zp2l9o8RrWc","genre":"comedy","duration":6,"summary":"Bathroom chaos from spider.","thumbnail":"https://img.youtube.com/vi/Zp2l9o8RrWc/hqdefault.jpg"},
  {"title":"The Elevator","youtube_url":"https://www.youtube.com/watch?v=Q0s5Zqmb09g","genre":"comedy","duration":5,"summary":"Awkward elevator ride.","thumbnail":"https://img.youtube.com/vi/Q0s5Zqmb09g/hqdefault.jpg"},
  {"title":"Wrong Hole","youtube_url":"https://www.youtube.com/watch?v=2fX0Y3hE5Q0","genre":"comedy","duration":4,"summary":"Absurd comedy misunderstanding.","thumbnail":"https://img.youtube.com/vi/2fX0Y3hE5Q0/hqdefault.jpg"},
  {"title":"French Roast","youtube_url":"https://www.youtube.com/watch?v=2s7Z1uY4x7E","genre":"comedy","duration":8,"summary":"Cafe ego comedy.","thumbnail":"https://img.youtube.com/vi/2s7Z1uY4x7E/hqdefault.jpg"},
  {"title":"Omelette","youtube_url":"https://www.youtube.com/watch?v=H0u3C6r3H7Q","genre":"comedy","duration":6,"summary":"Cooking chaos.","thumbnail":"https://img.youtube.com/vi/H0u3C6r3H7Q/hqdefault.jpg"},
  {"title":"Bear Story","youtube_url":"https://www.youtube.com/watch?v=9K4s7a3o7Wc","genre":"comedy","duration":10,"summary":"Dark humor circus story.","thumbnail":"https://img.youtube.com/vi/9K4s7a3o7Wc/hqdefault.jpg"},
  {"title":"Presto","youtube_url":"https://www.youtube.com/watch?v=1FZzJ0s5mS4","genre":"comedy","duration":5,"summary":"Magician vs rabbit.","thumbnail":"https://img.youtube.com/vi/1FZzJ0s5mS4/hqdefault.jpg"},
  {"title":"Lifted","youtube_url":"https://www.youtube.com/watch?v=lvw8Qx9b9cE","genre":"comedy","duration":5,"summary":"Alien abduction training.","thumbnail":"https://img.youtube.com/vi/lvw8Qx9b9cE/hqdefault.jpg"},
  {"title":"Partly Cloudy","youtube_url":"https://www.youtube.com/watch?v=7WYq3Lw4n8c","genre":"comedy","duration":6,"summary":"Cloud creates unusual babies.","thumbnail":"https://img.youtube.com/vi/7WYq3Lw4n8c/hqdefault.jpg"},

  {"title":"Paperman","youtube_url":"https://www.youtube.com/watch?v=UPA2O1pU9sE","genre":"romantic","duration":7,"summary":"Paper planes love story.","thumbnail":"https://img.youtube.com/vi/UPA2O1pU9sE/hqdefault.jpg"},
  {"title":"In a Heartbeat","youtube_url":"https://www.youtube.com/watch?v=2REkk9SCRn0","genre":"romantic","duration":4,"summary":"Heart escapes to follow love.","thumbnail":"https://img.youtube.com/vi/2REkk9SCRn0/hqdefault.jpg"},
  {"title":"Feast","youtube_url":"https://www.youtube.com/watch?v=9N0T7X7b7W0","genre":"romantic","duration":6,"summary":"Love through dog's eyes.","thumbnail":"https://img.youtube.com/vi/9N0T7X7b7W0/hqdefault.jpg"},
  {"title":"The Wishgranter","youtube_url":"https://www.youtube.com/watch?v=O1H7U7z8JmY","genre":"romantic","duration":4,"summary":"Unexpected love wish.","thumbnail":"https://img.youtube.com/vi/O1H7U7z8JmY/hqdefault.jpg"},
  {"title":"Lost & Found","youtube_url":"https://www.youtube.com/watch?v=8r0xKZ0zF7o","genre":"romantic","duration":7,"summary":"Two strangers reconnect.","thumbnail":"https://img.youtube.com/vi/8r0xKZ0zF7o/hqdefault.jpg"},
  {"title":"Love is Blind","youtube_url":"https://www.youtube.com/watch?v=example","genre":"romantic","duration":5,"summary":"Unexpected emotional twist.","thumbnail":"https://img.youtube.com/vi/example/hqdefault.jpg"},
  {"title":"Warm Hearts","youtube_url":"https://www.youtube.com/watch?v=example2","genre":"romantic","duration":8,"summary":"Love in simple moments.","thumbnail":"https://img.youtube.com/vi/example2/hqdefault.jpg"},
  {"title":"The Proposal","youtube_url":"https://www.youtube.com/watch?v=example3","genre":"romantic","duration":9,"summary":"Unexpected proposal story.","thumbnail":"https://img.youtube.com/vi/example3/hqdefault.jpg"},
  {"title":"Dear Diary","youtube_url":"https://www.youtube.com/watch?v=example4","genre":"romantic","duration":10,"summary":"Memories of love.","thumbnail":"https://img.youtube.com/vi/example4/hqdefault.jpg"},
  {"title":"First Date","youtube_url":"https://www.youtube.com/watch?v=example5","genre":"romantic","duration":6,"summary":"Awkward first meeting.","thumbnail":"https://img.youtube.com/vi/example5/hqdefault.jpg"},
  {"title":"Long Distance","youtube_url":"https://www.youtube.com/watch?v=example6","genre":"romantic","duration":8,"summary":"Love across distance.","thumbnail":"https://img.youtube.com/vi/example6/hqdefault.jpg"},
  {"title":"Missed Call","youtube_url":"https://www.youtube.com/watch?v=example7","genre":"romantic","duration":7,"summary":"A call changes everything.","thumbnail":"https://img.youtube.com/vi/example7/hqdefault.jpg"},

  {"title":"Curve","youtube_url":"https://www.youtube.com/watch?v=2dD3Fawk4y0","genre":"intense","duration":10,"summary":"Survival on curved wall.","thumbnail":"https://img.youtube.com/vi/2dD3Fawk4y0/hqdefault.jpg"},
  {"title":"Lights Out","youtube_url":"https://www.youtube.com/watch?v=FUQhNGEu2KA","genre":"intense","duration":3,"summary":"Dark presence appears.","thumbnail":"https://img.youtube.com/vi/FUQhNGEu2KA/hqdefault.jpg"},
  {"title":"Cargo","youtube_url":"https://www.youtube.com/watch?v=gyfmwgOV6uo","genre":"intense","duration":7,"summary":"Zombie survival.","thumbnail":"https://img.youtube.com/vi/gyfmwgOV6uo/hqdefault.jpg"},
  {"title":"2AM Smiling Man","youtube_url":"https://www.youtube.com/watch?v=_u6Tt3PqIfQ","genre":"intense","duration":5,"summary":"Creepy late-night encounter.","thumbnail":"https://img.youtube.com/vi/_u6Tt3PqIfQ/hqdefault.jpg"},
  {"title":"The Dollmaker","youtube_url":"https://www.youtube.com/watch?v=OqSmb3n0j8o","genre":"intense","duration":9,"summary":"Dark magic consequences.","thumbnail":"https://img.youtube.com/vi/OqSmb3n0j8o/hqdefault.jpg"},
  {"title":"Bedfellows","youtube_url":"https://www.youtube.com/watch?v=WQvGmMVBYMw","genre":"intense","duration":4,"summary":"Terrifying phone call.","thumbnail":"https://img.youtube.com/vi/WQvGmMVBYMw/hqdefault.jpg"},
  {"title":"Mama","youtube_url":"https://www.youtube.com/watch?v=WRqS6pBC42w","genre":"intense","duration":3,"summary":"Ghostly mother returns.","thumbnail":"https://img.youtube.com/vi/WRqS6pBC42w/hqdefault.jpg"},
  {"title":"Other Side Box","youtube_url":"https://www.youtube.com/watch?v=OrOYvVf6tIM","genre":"intense","duration":15,"summary":"Box hides something terrifying.","thumbnail":"https://img.youtube.com/vi/OrOYvVf6tIM/hqdefault.jpg"},
  {"title":"He Took His Skin Off","youtube_url":"https://www.youtube.com/watch?v=Z8pF0f4x7Z8","genre":"intense","duration":10,"summary":"Identity horror story.","thumbnail":"https://img.youtube.com/vi/Z8pF0f4x7Z8/hqdefault.jpg"},
  {"title":"The Jigsaw","youtube_url":"https://www.youtube.com/watch?v=example8","genre":"intense","duration":8,"summary":"Puzzle reveals horror.","thumbnail":"https://img.youtube.com/vi/example8/hqdefault.jpg"},
  {"title":"Door","youtube_url":"https://www.youtube.com/watch?v=example9","genre":"intense","duration":6,"summary":"Door leads to fear.","thumbnail":"https://img.youtube.com/vi/example9/hqdefault.jpg"},
  {"title":"Shadows","youtube_url":"https://www.youtube.com/watch?v=example10","genre":"intense","duration":7,"summary":"Shadows come alive.","thumbnail":"https://img.youtube.com/vi/example10/hqdefault.jpg"},

  {"title":"Alike","youtube_url":"https://www.youtube.com/watch?v=PDHIyrfMl_U","genre":"casual","duration":8,"summary":"Creativity vs routine.","thumbnail":"https://img.youtube.com/vi/PDHIyrfMl_U/hqdefault.jpg"},
  {"title":"Piper","youtube_url":"https://www.youtube.com/watch?v=6i1q7FQ7Xn4","genre":"casual","duration":6,"summary":"Bird learns courage.","thumbnail":"https://img.youtube.com/vi/6i1q7FQ7Xn4/hqdefault.jpg"},
  {"title":"For the Birds","youtube_url":"https://www.youtube.com/watch?v=hnX0F0D0j9k","genre":"casual","duration":3,"summary":"Bird lesson.","thumbnail":"https://img.youtube.com/vi/hnX0F0D0j9k/hqdefault.jpg"},
  {"title":"Kitbull","youtube_url":"https://www.youtube.com/watch?v=AZS5cgybKcI","genre":"casual","duration":9,"summary":"Unlikely friendship.","thumbnail":"https://img.youtube.com/vi/AZS5cgybKcI/hqdefault.jpg"},
  {"title":"The Present","youtube_url":"https://www.youtube.com/watch?v=WjqiU5FgsYc","genre":"casual","duration":4,"summary":"Unexpected gift.","thumbnail":"https://img.youtube.com/vi/WjqiU5FgsYc/hqdefault.jpg"},
  {"title":"Bao","youtube_url":"https://www.youtube.com/watch?v=9FTIJ7b6r2E","genre":"casual","duration":7,"summary":"Mother-child bond.","thumbnail":"https://img.youtube.com/vi/9FTIJ7b6r2E/hqdefault.jpg"},
  {"title":"Float","youtube_url":"https://www.youtube.com/watch?v=hH3HqN4W6p8","genre":"casual","duration":6,"summary":"Father accepts son's uniqueness.","thumbnail":"https://img.youtube.com/vi/hH3HqN4W6p8/hqdefault.jpg"},
  {"title":"La Luna","youtube_url":"https://www.youtube.com/watch?v=7n7pY3jR8Lk","genre":"casual","duration":7,"summary":"Magical moon story.","thumbnail":"https://img.youtube.com/vi/7n7pY3jR8Lk/hqdefault.jpg"},
  {"title":"Lou","youtube_url":"https://www.youtube.com/watch?v=example11","genre":"casual","duration":6,"summary":"Lost and found box.","thumbnail":"https://img.youtube.com/vi/example11/hqdefault.jpg"},
  {"title":"Day & Night","youtube_url":"https://www.youtube.com/watch?v=example12","genre":"casual","duration":5,"summary":"Opposites interact.","thumbnail":"https://img.youtube.com/vi/example12/hqdefault.jpg"},
  {"title":"Wind","youtube_url":"https://www.youtube.com/watch?v=example13","genre":"casual","duration":8,"summary":"Life in sinkhole.","thumbnail":"https://img.youtube.com/vi/example13/hqdefault.jpg"},
  {"title":"Lava","youtube_url":"https://www.youtube.com/watch?v=example14","genre":"casual","duration":7,"summary":"Volcano love story.","thumbnail":"https://img.youtube.com/vi/example14/hqdefault.jpg"}
]"""

data = json.loads(raw_data)

genre_map = {
    "sci-fi": "Sci-Fi",
    "comedy": "Comedy",
    "romantic": "Romantic",
    "intense": "Intense",
    "casual": "Casual"
}

def is_working(video_id):
    if "example" in video_id:
        return False
        
    url = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
    try:
        req = urllib.request.Request(url, method='HEAD')
        resp = urllib.request.urlopen(req)
        length = resp.headers.get('Content-Length')
        # A deleted/private youtube thumbnail gray box is ~120 bytes or similar. 
        # Actually mqdefault gray boxes are roughly 2600-3000 bytes. Valid ones are larger.
        # Even safer: checking if the URL returns a redirect to a known google 'error' image.
        # Actually youtube just returns a 404 for hqdefault, but mqdefault is 200 with an empty grey image.
        # But wait! I can just use another approach to flag broken entries! I can just make a GET on the youtube oembed API!
        # If it's private/deleted, oEmbed returns a 404 or Unauthorized.
        
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        try:
            o_req = urllib.request.urlopen(oembed_url)
            if o_req.status == 200:
                return True
        except:
            return False
            
        return False
        
    except Exception as e:
        return False

with open("c:/SHORT FILM/data.py", "w", encoding="utf-8") as f:
    f.write('def get_films():\n    return [\n')
    for i, item in enumerate(data):
        g = item['genre']
        c_i = i+1
        item['id'] = f"{g.replace('-','')}_{c_i}"
        item['genre'] = genre_map.get(g, g)
        
        video_id = item['youtube_url'].split('v=')[-1].split('&')[0]
        working = is_working(video_id)
        
        item['is_verified'] = working
        # enforce standard mqdefault to avoid hqdefault 404 discrepancies
        if "example" not in video_id:
            item['thumbnail'] = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
        
        f.write('        {\n')
        keys = list(item.keys())
        for k in keys:
            val = item[k]
            if isinstance(val, str):
                f.write(f'            "{k}": "{val}"')
            elif isinstance(val, bool):
                f.write(f'            "{k}": {str(val)}')
            else:
                f.write(f'            "{k}": {val}')
            
            if k != keys[-1]:
                f.write(',\n')
            else:
                f.write('\n')
        
        if i < len(data) - 1:
            f.write('        },\n')
        else:
            f.write('        }\n')
            
    f.write('    ]')
