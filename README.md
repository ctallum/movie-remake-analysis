# Data Mining Project - An Analysis of Movie Remakes
## **About**
In this project, I attempted to answer the question: "Are movie remakes really worse than the original?". To try and answer this, I gathered data on over 400 movies that have been remade and their remakes. With this data, I graphed the quality of the remake over time, by genre, and by length of time since the original's release. 

## **Requirements**
### IMDbPY
This projects relies on IMDbPY, a Python package for retrieving and managing the data of the IMDb movie database about movies, people and companies.

Install IMDbPy one of two ways:

`pip install git+https://github.com/alberanid/imdbpy`

or 

`pip install imdbpy`

## **Usage**
This project contains the following files: 
- movie_scraper.py
- graph_data.py
- movie_scraper.ipynb
- test_data.py

*movie_scraper.py* contains all the nescessary functions needed to collect data on movies and their remakes. *graph_data.py* contains a few function that graph the movie data. Laslty, *movie_scraper.ipynb* is a computational essay that provides a complete rundown of how to use the data scraping functions and how to graph the data. 

*test_data.py* is a pytest file that tests to ensure that the scraped datatable doesn't have any issues or inconsistencies.