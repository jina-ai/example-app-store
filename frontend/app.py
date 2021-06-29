import streamlit as st
from frontend_config import endpoint, top_k
import requests

image_size = 128


def get_data(query: str, endpoint: str, top_k: int) -> dict:
    headers = {
        "Content-Type": "application/json",
    }

    data = '{"top_k":' + str(top_k) + ',"mode":"search","data":["' + query + '"]}'

    response = requests.post(endpoint, headers=headers, data=data)
    content = response.json()

    matches = content["data"]["docs"][0]["matches"]

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
    if price == "0":
        price_string = "Free"
    else:
        price_string = currency + price

    return price_string


# layout
max_width = 1200
padding = 2


st.markdown(
    f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {max_width}px;
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }}
    .reportview-container .main {{
        color: "#111";
        background-color: "#eee";
    }}
</style>
""",
    unsafe_allow_html=True,
)

# Setup sidebar
st.sidebar.title("Jina App Store Search")

settings = st.sidebar.beta_expander(label="Settings", expanded=False)
with settings:
    endpoint = st.text_input(label="Endpoint", value=endpoint)
    top_k = st.number_input(label="Top K", value=top_k, step=1)

st.sidebar.markdown(
    """
This is an example app store search engine using the [Jina neural search framework](https://github.com/jina-ai/jina/).

**Note: click the search button instead of hitting Enter. We're working on fixing this!**

- Backend: [Jina](https://github.com/jina-ai/jina/)
- Frontend: [Streamlit](https://www.streamlit.io/)
- Dataset: [Kaggle](https://www.kaggle.com/tristan581/17k-apple-app-store-strategy-games)

Only the search engine part of this app store works. We don't host apps, and we certainly don't sell them!

[Visit the repo](https://github.com/alexcg1/jina-app-store-example)

<a href="https://github.com/jina-ai/jina/"><img src="https://github.com/alexcg1/jina-app-store-example/blob/a8f64332c6a5b3ae42df07d4bd615ff1b7ece4d9/frontend/powered_by_jina.png?raw=true" width=256></a>
""",
    unsafe_allow_html=True,
)

st.title("Jina App Store Search")

query = st.text_input(
    label="Search mobile games by keywords or category e.g. fun games, knights and warriors, etc."
)

if st.button(label="Search"):
    if not query:
        st.markdown("Please enter a query")
    else:

        matches = get_data(query=query, endpoint=endpoint, top_k=top_k)
        cell1, cell2, cell3 = st.beta_columns(3)
        cell4, cell5, cell6 = st.beta_columns(3)
        cell7, cell8, cell9 = st.beta_columns(3)

        all_cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]

        for match in matches:
            col1, col2 = st.beta_columns([1, 4])
            with col1:
                st.image(match["tags"]["Icon URL"])

            with col2:
                app_name = f'**[{sanitize_string(match["tags"]["Name"])}]({match["tags"]["URL"]})**'
                app_rating = f'{get_star_string(match["tags"]["Average User Rating"])}'
                app_genres = f'<small>{match["tags"]["Genres"]}</small>'
                app_desc = shorten_string(sanitize_string(match["text"]), word_count=50)

                st.markdown(
                    f"""
                            {app_name}\t{app_rating}\n
                            {app_genres}\n
                            {app_desc}
                            """,
                    unsafe_allow_html=True,
                )

                # st.markdown(
                # f'**[{sanitize_string(match["tags"]["Name"])}]({match["tags"]["URL"]})**     {get_star_string(match["tags"]["Average User Rating"])}'
                # )
                # st.markdown(f'<small>{match["tags"]["Genres"]}</small>', unsafe_allow_html=True)
                # st.markdown(
                # f'{shorten_string(sanitize_string(match["text"]), word_count=50)}'
                # )
                st.button(
                    label=get_price_string(match["tags"]["Price"]), key=match["id"]
                )

