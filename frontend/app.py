import streamlit as st
import requests

endpoint = 'http://0.0.0.0:8080/search'
image_size = 128



def get_data(query: str, endpoint: str, top_k: int) -> dict:
    headers = {
        'Content-Type': 'application/json',
    }

    data = '{"top_k":' + str(top_k) + ',"mode":"search","data":["' + query + '"]}'

    response = requests.post('http://0.0.0.0:8080/search', headers=headers, data=data)
    content = response.json()

    matches = content['data']['docs'][0]['matches']

    # for match in matches:
        # pprint(match)
        # print('\n\n\n')

    return matches

def shorten_string(string, word_count = 20, suffix="..."):
    words = string.split(' ')
    output = ' '.join(words[:word_count])+suffix

    return output

def get_star_string(rating, max_rating=5, full_star="★", empty_star="☆"):
    try:
        rating = float(rating)
        full_stars = round(rating)
    except:
        full_stars = 3

    empty_stars = max_rating - full_stars
    star_string = full_star*full_stars + empty_star*empty_stars

    return star_string

def get_price_string(price, currency="$"):
    if price == "0":
        price_string = "Free"
    else:
        price_string = currency+price

    return price_string




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

        for cell, match in zip(all_cells, matches):
            cell.image(match["tags"]["Icon URL"])
            cell.markdown(f'**{match["tags"]["Name"]}**')
            cell.markdown(get_star_string(match["tags"]["Average User Rating"]))
            cell.markdown(f'*{match["tags"]["Genres"]}*')
            cell.markdown(f'{shorten_string(match["text"])}')
            if cell.button(label=get_price_string(match["tags"]["Price"]), key=match["id"]):
                st.balloons()
