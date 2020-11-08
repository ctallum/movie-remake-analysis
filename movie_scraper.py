import requests
from bs4 import BeautifulSoup as soup

import pandas as pd

def get_remakes():
    """
    Get a list of all movies that have ever been remade and thier wikipedia
    URLs.

    Args:
        None
    Returns:
        movie_data::pandas DataFrame
            movie_data is a pandas dataframe that has the following columns:
            original movie name, original movie wiki link, remake movie name,
            and remake movie wiki link.
    """

    original_name = []
    original_link = []
    remake_name = []
    remake_link = []

    ### Get movie names and links from wiki page -----------------------------------

    # request raw html from wikipedia pages
    base_url = "https://en.wikipedia.org"
    url1 = "https://en.wikipedia.org/wiki/List_of_film_remakes_(A%E2%80%93M)"
    url2 = "https://en.wikipedia.org/wiki/List_of_film_remakes_(N%E2%80%93Z)"
    wiki_page1 = requests.get(url1)
    wiki_page2 = requests.get(url2)

    # initialize soup object with wiki page html
    soup_page1 = soup(wiki_page1.text)
    soup_page2 = soup(wiki_page2.text)

    # find all tables on page. Ignore first one bc it doensn't contain movies
    table1 = soup_page1.find_all("table")[1:]
    table2 = soup_page2.find_all("table")[1:]

    wiki_table = table1 + table2

    # Search through tables to find movie titles and relative urls
    for sub_table in wiki_table:
        letter_table = sub_table.find_all("tr")
        for entry in letter_table[1:]:
            # Original Movie
            try:
                original_movie = entry.find_all("a")[0]
                original_name.append(original_movie.get("title"))
                original_link.append(base_url + original_movie.get("href"))
            except IndexError:
                original_name.append(None)
                original_link.append(None)
                continue
            # Remakes
            try:
                remake_movie = entry.find_all("a")[1]
                remake_name.append(remake_movie.get("title"))
                remake_link.append(base_url + remake_movie.get("href"))
            except IndexError:
                remake_name.append(None)
                remake_link.append(None)
                continue

    movie_data = list(zip(original_name,original_link,remake_name,remake_link))
    column_names = ["Original Name", "Original Link", "Remake Name", "Remake Link"]

    return pd.DataFrame(movie_data, columns=column_names)

print(get_remakes())