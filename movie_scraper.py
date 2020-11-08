import requests
import pandas as pd
from bs4 import BeautifulSoup as soup
from imdb import IMDb
import re


def get_wiki_links():
    """
    Make a table of wikipedia links every movie that have ever been remade and
    its corresponding remake.

    Search through the Wikipedia page "List of film remakes (A-M)" and "List of
    film remakes (N-Z)" and find all the movies that have been remade. The
    movies are stored on the wikipedia page in tables by starting letter of
    orgininal movie. For each original movie and its corresponding remake,
    store the wikipedia url in a table. For movies that have had multiple
    remakes, only store the url for the most recent remake.

    Args:
        None
    Returns:
        movie_data::pandas DataFrame
            movie_data is a pandas dataframe that has the following columns:
            "original link" and "remake link"
    """

    # create empty lists for movie wikipedia links
    wiki_original_links = []
    wiki_remake_links = []

    # request raw html from wikipedia pages
    base_url = "https://en.wikipedia.org"
    url1 = "https://en.wikipedia.org/wiki/List_of_film_remakes_(A%E2%80%93M)"
    url2 = "https://en.wikipedia.org/wiki/List_of_film_remakes_(N%E2%80%93Z)"
    wiki_page1 = requests.get(url1)
    wiki_page2 = requests.get(url2)

    # initialize soup object with wiki page html
    soup_page1 = soup(wiki_page1.text, "html.parser")
    soup_page2 = soup(wiki_page2.text, "html.parser")

    # find all tables on page. Ignore first one bc it doensn't contain movies
    table1 = soup_page1.find_all("table")[1:]
    table2 = soup_page2.find_all("table")[1:]

    # combine tables from the two wikipedia pages into one
    wiki_table = table1 + table2

    # Search through main wikipedia table to find all sub-tables of movies
    # alphabetized by first letter
    for letter_table in wiki_table:
        # for each letter sub-table, find all columns of movies
        list_of_movies = letter_table.find_all("tr")
        # ignore first entry in list of movies bc it doesn't contain movie
        for entry in list_of_movies[1:]:
            # Get original movie link
            try:
                original_movie = entry.find_all("a")[0]
                # add wikipedia link to the base url to form complete url and
                # add that to the list of movie urls
                wiki_original_links.append(base_url
                                           + original_movie.get("href"))
            except IndexError:
                # If no movie link is found, record link as "NONE"
                wiki_original_links.append("NONE")
                continue

            # Get remake movie link
            try:
                remake_movie = entry.find_all("a")[1]
                # add wikipedia link to the base url to form complete url and
                # add that to the list of movie urls
                wiki_remake_links.append(base_url + remake_movie.get("href"))
            except IndexError:
                # If no movie link is found, record link as "NONE"
                wiki_remake_links.append("NONE")
                continue

    # combine the two movie url lists into one
    movie_data = list(zip(wiki_original_links, wiki_remake_links))
    column_names = ["original link", "remake link"]

    # create pandas dataframe with movie links
    wiki_dataframe = pd.DataFrame(movie_data, columns=column_names)

    return wiki_dataframe


def get_imdb_numbers(wiki_dataframe):
    """
    Make a table of IMDb numbers for every movie that has ever been remade and
    its corresponding remake.

    Take an input pandas dataframe of Wikipedia links. For each Wikipedia link,
    search page to find external link to main IMDb page for movie. Each IMDb
    movie link contans a unique number that corresponds to only that movie.
    Find this number for each movie.

    Args:
        wiki_dataframe::pandas DataFrame
            A dataframe that contains Wikipedia links for movies. The dataframe
            contains two columns, one for the original movie and one for the
            remake.
    Returns:
        imdb_dataframe::padnas DataFrame
            A dataframe that contains IMDb numbers for movies. The dataframe
            contains two columns, one for the original movie and one for the
            remake.
    """

    # create empty lists for movie imdb links
    imdb_original_numbers = []
    imdb_remake_numbers = []

    # Find imdb numbers for all original movies
    for wiki_link in wiki_dataframe["original link"]:
        # set default imdb_link to be "NONE" in case of error
        imdb_number = "NONE"
        # request raw html from wikipedia pages
        r = requests.get(wiki_link)
        # Check to see if the URL is valid
        if r.status_code == 200:
            # initialize soup object with wiki page html
            wiki_page = soup(r.text, "html.parser")
            # find all links on page with class set as "external text"
            external_links = wiki_page.find_all("a", class_="external text")
            for link in external_links:
                # check to see if the external link is to an IMDb movie page
                if "https://www.imdb.com/title/" in link.get("href"):
                    # get full imdb page url
                    full_movie_url = link.get("href")
                    # find the unique imdb number within url and ovewrite
                    # default number from 'NONE" to this number
                    imdb_number = re.search(r'\d+', full_movie_url).group()
        # Add imdb number to list
        imdb_original_numbers.append(imdb_number)

    # Find imdb numbers for all remake movies
    for wiki_link in wiki_dataframe["remake link"]:
        # set default imdb_link to be "NONE" in case of error
        imdb_number = "NONE"
        # request raw html from wikipedia pages
        r = requests.get(wiki_link)
        # Check to see if the URL is valid
        if r.status_code == 200:
            # initialize soup object with wiki page html
            wiki_page = soup(r.text, "html.parser")
            # find all links on page with class set as "external text"
            external_links = wiki_page.find_all("a", class_="external text")
            for link in external_links:
                # check to see if the external link is to an IMDb movie page
                if "https://www.imdb.com/title/" in link.get("href"):
                    # get full imdb page url
                    full_movie_url = link.get("href")
                    # find the unique imdb number within url and ovewrite
                    # default number from 'NONE" to this number
                    imdb_number = re.search(r'\d+', full_movie_url).group()
        # Add imdb number to list
        imdb_remake_numbers.append(imdb_number)

    # combine two imdb number lists into one
    data = list(zip(imdb_original_numbers, imdb_remake_numbers))
    imdb_dataframe = pd.DataFrame(data, columns=["original", "remake"])

    return imdb_dataframe


def get_movie_data(imdb_dataframe):
    """
    Collect data from IMDb on movies and save data to a dataframe.

    For each imdb number in the argument dataframe, search up the movie and
    scrape data from the IMDb page. Save the resulting data for each movie
    into a pandas Dataframe.

    Args:
        imdb_dataframe::padnas DataFrame
            A dataframe that contains IMDb numbers for movies. The dataframe
            contains two columns, one for the original movie and one for the
            remake.
    Returns:
        movie_data::pandas DataFrame
            A dataframe that contains data on both the original and remake
            movie. The dataframe has 10 columns. They are "Original title",
            "Original year", "Original genre", "Original rating", "Original
            rating", "Original votes", "Remake title", "Remake year", "Remake
            genre", "Remake rating", and "Remake votes".
    """

    # initialize IMDb module
    ia = IMDb()

    # create pandas DataFrame
    index = range(len(imdb_dataframe))

    column_names = ["Original title", "Original year", "Original genre(s)",
                    "Original rating", "Original votes", "Remake title",
                    "Remake year", "Remake genre(s)", "Remake rating",
                    "Remake votes"]

    movie_data = pd.DataFrame(index=index, columns=column_names)

    for row in range(len(imdb_dataframe)):
        try:
            original_movie = ia.get_movie(imdb_dataframe["original"][row])
            original_title = original_movie["title"]
            original_year = original_movie["year"]
            original_genre = original_movie["genre"]
            original_rating = float(original_movie["rating"])
            original_votes = int(original_movie["votes"])

            remake_movie = ia.get_movie(imdb_dataframe["remake"][row])
            remake_title = remake_movie["title"]
            remake_year = remake_movie["year"]
            remake_genre = remake_movie["genre"]
            remake_rating = float(remake_movie["rating"])
            remake_votes = int(remake_movie["votes"])

            row_data = [original_title, original_year, original_genre,
                        original_rating, original_votes, remake_title,
                        remake_year, remake_genre, remake_rating,
                        remake_votes]
        except KeyError:
            row_data = ["NONE" for column in range(10)]

        movie_data.loc[row] = row_data

    return movie_data


def clean_dataframe(dataframe):
    """
    Remove rows in pandas DataFrame if they contain "NONE" in any column

    Args:
        dataframe::pandas DataFrame
    Returns:
        dataframe::pandas DataFrame
            Cleaned up dataframe. Does not contain any "NONE"
    """
    df = dataframe
    for column in list(df):
        none_index = df[df[column] == "NONE"].index
        df = df.drop(none_index)
    df.index = range(len(df))
    return df
