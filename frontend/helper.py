from config import SERVER, PORT, TOP_K
from jina import Client, Document
import requests

def get_data(query: str, endpoint: str, top_k: int) -> dict:
    headers = {
        "Content-Type": "application/json",
    }

    data = '{"top_k":' + str(top_k) + ',"mode":"search","data":["' + query + '"]}'

    response = requests.post(endpoint, headers=headers, data=data)
    content = response.json()

    matches = content["data"]["docs"][0]["matches"]

    return matches

def get_matches(input, server=SERVER, port=PORT, limit=TOP_K):
    client = Client(host=server, protocol="http", port=port)
    response = client.search(
        Document(text=input),
        return_results=True,
        parameters={"limit": limit},
        show_progress=True,
    )
    matches = response[0].docs[0].matches

    return matches



def shorten_string(string, word_count=20, suffix="..."):
    words = string.split(" ")
    output = " ".join(words[:word_count]) + suffix

    return output


def sanitize_string(string: str) -> str:
    escaped_string = string.encode("utf-8").decode("unicode_escape")

    return escaped_string


def get_star_string(rating, max_rating=5, full_star="★", empty_star="☆"):
    try:
        rating = float(rating)
        full_stars = round(rating)
    except:
        full_stars = 3

    empty_stars = max_rating - full_stars
    star_string = full_star * full_stars + empty_star * empty_stars

    return star_string


def get_price_string(price, currency="$"):
    if float(price) == 0.0:
        price_string = "Free"
    else:
        price_string = currency + price

    return price_string
