import streamlit as st
from appstore_config import my_endpoint
import requests

image_size = 128


def get_data(query: str, endpoint: str, top_k: int) -> dict:
    headers = {
        "Content-Type": "application/json",
    }

    data = '{"top_k":' + str(top_k) + ',"mode":"search","data":["' + query + '"]}'

    response = requests.post(my_endpoint, headers=headers, data=data)
    content = response.json()

    matches = content["data"]["docs"][0]["matches"]

    return matches


def shorten_string(string, word_count=20, suffix="..."):
    words = string.split(" ")
    output = " ".join(words[:word_count]) + suffix

    return output


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
    if price == "0":
        price_string = "Free"
    else:
        price_string = currency + price

    return price_string


# layout
max_width = 1200
padding_top = 2
padding_bottom = 2
padding_left = 2
padding_right = 2


st.markdown(
    f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {max_width}px;
        padding-top: {padding_top}rem;
        padding-right: {padding_right}rem;
        padding-left: {padding_left}rem;
        padding-bottom: {padding_bottom}rem;
    }}
    .reportview-container .main {{
        color: "#111";
        background-color: "#eee";
    }}
</style>
""",
    unsafe_allow_html=True,
)

st.title("Jina App Store Search")

query = st.text_input(label="Search", help="What kind of game are you looking for?")

if st.button(label="Search"):
    if not query:
        st.markdown("Please enter a query")
    else:

        matches = get_data(query=query, endpoint=endpoint, top_k=10)
        cell1, cell2, cell3 = st.beta_columns(3)
        cell4, cell5, cell6 = st.beta_columns(3)
        cell7, cell8, cell9 = st.beta_columns(3)

        all_cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]

        for match in matches:
            col1, col2 = st.beta_columns([1, 4])
            with col1:
                st.image(match["tags"]["Icon URL"])

            with col2:
                st.markdown(
                    f'**[{match["tags"]["Name"]}]({match["tags"]["URL"]})**     {get_star_string(match["tags"]["Average User Rating"])}'
                )
                st.markdown(f'*{match["tags"]["Genres"]}*')
                st.markdown(f'{shorten_string(match["text"], word_count=50)}')
                st.button(
                    label=get_price_string(match["tags"]["Price"]), key=match["id"]
                )

st.sidebar.title("Jina App Store Search")
st.sidebar.markdown(
    """
This is an example app store search engine.

- Backend: [Jina](https://github.com/jina-ai/jina/)
- Frontend: [Streamlit](https://www.streamlit.io/)
- Dataset: [Kaggle](https://www.kaggle.com/tristan581/17k-apple-app-store-strategy-games)

Only the search engine part of this app store works. We don't host apps, and we certainly don't sell them!

[Visit the repo](https://github.com/alexcg1/jina-app-store-example)
"""
)
