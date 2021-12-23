import streamlit as st
from helper import get_price_string, shorten_string, sanitize_string, get_star_string, get_matches

title = "🎮 Games search with Jina"

st.set_page_config(page_title=title, layout="wide")


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
st.sidebar.markdown(
    """
This is an example game/app store search engine using the [Jina neural search framework](https://github.com/jina-ai/jina/).

**Note: click the search button instead of hitting Enter. This is a Streamlit issue, not Jina!**

- Backend: [Jina](https://github.com/jina-ai/jina/)
- Frontend: [Streamlit](https://www.streamlit.io/)
- Dataset: [Kaggle](https://www.kaggle.com/tristan581/17k-apple-app-store-strategy-games)

Only the search engine part of this game store works. We don't host apps, and we certainly don't sell them!

[Visit the repo](https://github.com/alexcg1/jina-app-store-example)

<a href="https://github.com/jina-ai/jina/"><img src="https://github.com/alexcg1/jina-app-store-example/blob/a8f64332c6a5b3ae42df07d4bd615ff1b7ece4d9/frontend/powered_by_jina.png?raw=true" width=256></a>
""",
    unsafe_allow_html=True,
)

st.title(title)

query = st.text_input(
    label="Search mobile games by keywords or category e.g. fun games, knights and warriors, etc."
)

if st.button(label="Search"):
    if not query:
        st.markdown("Please enter a query")
    else:

        matches = get_matches(input=query)

        for match in matches:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(match.tags["Icon URL"])

            with col2:
                app_name = f'**[{sanitize_string(match.tags["Name"])}]({match.tags["URL"]})**'
                app_rating = f'{get_star_string(match.tags["Average User Rating"])}'
                app_genres = f'<small>{match.tags["Genres"]}</small>'
                app_desc = shorten_string(sanitize_string(match.text), word_count=50)

                st.markdown(
                    f"""
                            {app_name}\t{app_rating}\n
                            {app_genres}\n
                            {app_desc}
                            """,
                    unsafe_allow_html=True,
                )

                st.button(
                    label=get_price_string(match.tags["Price"]), key=match.id
                )
