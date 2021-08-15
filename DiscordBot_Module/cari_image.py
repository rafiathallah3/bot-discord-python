from serpapi import GoogleSearch
import requests
import random
import string

def run_image(inp): 
    params = {
        "q": f"{inp}",
        "tbm": "isch",
        "ijn": "0",
        "api_key": "d7c7a142c7587aca3a2739fc6b454587d619a8c23d3509e57094f6003521bb6b"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    try:
        images_results = results['images_results']
        r = requests.get(images_results[random.randint(0, len(images_results)-2)]["original"])
        random_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        file_name = f"SPOILER_{random_name}.png"

        file = open(file_name, "wb")
        file.write(r.content)
        file.close()

        return file_name
    except KeyError:
        return None
