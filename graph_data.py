import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# dictionary to store column names
col = {"original_name": 0, "original_date": 1, "original_genre": 2,
       "original_rating": 3, "original_votes": 4, "remake_name": 5,
       "remake_date": 6, "remake_genre": 7, "remake_rating": 8,
       "remake_votes": 9}


def graph_rating_change_by_time(movie_data, col=col):
    """
    Graph difference in remake movie rating compared to original rating over
    time.

    Args:
        movie_data::numpy array
            An numpy array that contains data on both the original and remake
            movie. The dataframe has 10 columns. They are "Original title",
            "Original year", "Original genre", "Original rating", "Original
            rating", "Original votes", "Remake title", "Remake year", "Remake
            genre", "Remake rating", and "Remake votes".
        col::dict
            Default is a dictionary whos keys are a description of the column
            data and the values are the column number.
    Returns:
        A plot
    """

    # renaming movie_data as df
    df = movie_data

    # calculate change in rating as difference between new movie and old movie
    d_rating = df[:, col["remake_rating"]] - df[:, col["original_rating"]]

    plt.plot(df[:, col["remake_date"]], d_rating, "b.")
    plt.title("Remake movies vs originals over time")
    plt.xlabel("Year of remake movie")
    plt.ylabel("Change in IMDb score compared to original")


def find_popular_genres(movie_data, number, col=col):
    """
    Find the most popular movie genres in dataset.

    Args:
        movie_data::numpy array
            An numpy array that contains data on both the original and remake
            movie. The dataframe has 10 columns. They are "Original title",
            "Original year", "Original genre", "Original rating", "Original
            rating", "Original votes", "Remake title", "Remake year", "Remake
            genre", "Remake rating", and "Remake votes".
        number::int
            Number of genres to return. Function will return the top "number"
            genres. Default is to return top 8 genres.
        col::dict
            Default is a dictionary whos keys are a description of the column
            data and the values are the column number.
    Returns:
        top_genres::list
            A dictionary whose keys are the movie genres and whose values are
            the number of times that genre apeared in the dataset. The dict
            is sorted from most popular to least populal.
    """
    # initialize empty dicitonary
    top_categories = {}

    for movie in movie_data[:, col["original_genre"]]:
        for genre in movie:
            # if genre is not yet in dicitonary, add it and give it value of 1
            if genre not in top_categories:
                top_categories[genre] = 1
            # if genre is in dictionary, add to count
            else:
                top_categories[genre] += 1

    # sort the dictionary by my popular genres of movie
    categories = sorted(top_categories, key=top_categories.get, reverse=True)

    # return the most popular categories
    return categories[0:number]


def graph_rating_change_by_genre(movie_data, bars=8, col=col):
    """
    Graph change in ratings of movie remakes by genre of original movie.

    Args:
        movie_data::numpy array
            An numpy array that contains data on both the original and remake
            movie. The dataframe has 10 columns. They are "Original title",
            "Original year", "Original genre", "Original rating", "Original
            rating", "Original votes", "Remake title", "Remake year", "Remake
            genre", "Remake rating", and "Remake votes".
        bars::int
            Number of movie genres to display in bar graph.
        col::dict
            Default is a dictionary whos keys are a description of the column
            data and the values are the column number.
    Returns:
        A plot
    """

    # renaming movie_data as df
    df = movie_data

    # calculate change in rating as difference between new movie and old movie
    d_rating = df[:, col["remake_rating"]] - df[:, col["original_rating"]]

    # get movie genres
    genres = find_popular_genres(movie_data, bars)

    # list of change in ratings by genre
    d_ratings_genre = []

    for genre in genres:
        # find index of movies with specic genre
        movie_index = [movie for movie in range(len(df)) if genre in
                       df[movie, col["original_genre"]]]
        # find average change in score for movies with specific genre
        average_d_rating = sum(d_rating[movie_index]) / \
            len(d_rating[movie_index])
        # append list
        d_ratings_genre.append(average_d_rating)

    # create bar graph
    plt.bar(genres, d_ratings_genre)
    plt.title("Quality of movie remakes by genre")
    plt.xlabel("Genre of original movie")
    plt.ylabel("Change in IMDb score compared to original")


def graph_rating_change_by_genre_full(movie_data, bars=8, col=col):
    """
    Graph average orignal and remake rating of movie by genre.

    Args:
        movie_data::numpy array
            An numpy array that contains data on both the original and remake
            movie. The dataframe has 10 columns. They are "Original title",
            "Original year", "Original genre", "Original rating", "Original
            rating", "Original votes", "Remake title", "Remake year", "Remake
            genre", "Remake rating", and "Remake votes".
        bars::int
            Number of movie genres to display in bar graph.
        col::dict
            Default is a dictionary whos keys are a description of the column
            data and the values are the column number.
    Returns:
        A plot
    """

    # renaming movie_data as df
    df = movie_data

    # create empty list for remake movies ratings and bar height (d_rating)
    remake_ratings = []
    d_ratings = []

    # get movie genres
    genres = find_popular_genres(movie_data, bars)

    for genre in genres:
        # find index of movies with specic genre
        movie_index = [movie for movie in range(len(df)) if genre in
                       df[movie, col["original_genre"]]]
        # find average remake rating
        remake_rating = df[:, col["remake_rating"]][movie_index]
        remake_ratings.append(sum(remake_rating) / len(remake_rating))
        # find change in ratings
        d_rating = df[:, col["original_rating"]][movie_index] - \
            df[:, col["remake_rating"]][movie_index]
        d_ratings.append(sum(d_rating) / len(d_rating))

    plt.bar(genres, height=d_ratings, bottom=remake_ratings)
    plt.title("Average rating of original and remake movies by genre")
    plt.xlabel("Genre of original movie")
    plt.ylabel("Rating of original and remake movie")
    plt.legend(["Top = Original; Bottom = Remake"])


def graph_rating_change_by_year_dif(movie_data, col=col):
    """
    Graph difference in remake movie rating compared to original rating by
    length of time between original movie and remake

    Args:
        movie_data::numpy array
            An numpy array that contains data on both the original and remake
            movie. The dataframe has 10 columns. They are "Original title",
            "Original year", "Original genre", "Original rating", "Original
            rating", "Original votes", "Remake title", "Remake year", "Remake
            genre", "Remake rating", and "Remake votes".
        col::dict
            Default is a dictionary whos keys are a description of the column
            data and the values are the column number.
    Returns:
        A plot
    """

    # renaming movie_data as df
    df = movie_data

    # calculate change in rating as difference between new movie and old movie
    d_rating = df[:, col["remake_rating"]] - df[:, col["original_rating"]]

    # calculate difference in year made between new and old movie
    d_year = df[:, col["remake_date"]] - df[:, col["original_date"]]

    # plot graph
    plt.plot(d_year, d_rating, "b.")
    plt.title("Quality of movie remakes by years between remake and original")
    plt.xlabel("Time difference between original and remake (yrs)")
    plt.ylabel("Change in IMDb score compared to original")
