import pytest
import numpy as np
import pandas as pd

# Note: My project doesn't lend itself particularly well to unit testing. The
# only form of unit testing that I can think of that is viable for this project
# is to check that the data that I scraped is valid. To do this, I am going to
# check that every single entry in the dataframe is the correct data type. This
# will simulatniously check that the data doens't have any inconsistencies that
# would cause the plotting functions to break such as NaN or blank spaces.

# import data to test
data = pd.read_pickle("./movie_data.pkl").to_numpy()


def test_valid_name():
    # check that the title of each movie entry is a string
    valid_names = True  # set default as all True
    for row in range(len(data)):
        # check originals
        if not isinstance(data[row, 0], str):
            valid_names = False  # if a title is not a string, change to False
        # check remakes
        if not isinstance(data[row, 5], str):
            valid_names = False
    assert valid_names is True


def test_valid_years():
    # check that all of the years in the data table are integers
    valid_years = True  # set default as all True
    for row in range(len(data)):
        # check originals
        if not isinstance(data[row, 1], int):
            valid_years = False  # if years isnt int, change to False
        # Check remakes
        if not isinstance(data[row, 6], int):
            valid_years = False
    assert valid_years is True


def test_valid_genres():
    # check that all of the genres in the datatable are lists filled with str
    valid_genres = True  # set default as all True
    for row in range(len(data)):
        # Check originals
        if not isinstance(data[row, 2], list):
            valid_genres = False  # if genre isnt list, change to False
        else:
            for genre in data[row, 2]:  # check every genre to see if type str
                if not isinstance(genre, str):
                    valid_genres = False
        # Check remakes
        if not isinstance(data[row, 7], list):
            valid_genres = False
        else:
            for genre in data[row, 7]:
                if not isinstance(genre, str):
                    valid_genres = False
    assert valid_genres is True


def test_valid_ratings():
    # check that all of the ratings in the data table are floats
    valid_ratings = True  # set default as all True
    for row in range(len(data)):
        # check originals
        if not isinstance(data[row, 3], float):
            valid_ratings = False  # if ratngs aren't float, change to False
        # Check remakes
        if not isinstance(data[row, 8], float):
            valid_ratings = False
    assert valid_ratings is True


def test_valid_votes():
    # check that all of the votes in the data table are ints
    valid_votes = True  # set default as all True
    for row in range(len(data)):
        # check originals
        if not isinstance(data[row, 4], int):
            valid_votes = False  # if votes aren't int, change to False
        # Check remakes
        if not isinstance(data[row, 9], int):
            valid_votes = False
    assert valid_votes is True
