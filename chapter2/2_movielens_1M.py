#!/usr/bin/env python
from __future__ import print_function
import pandas as pd


def main():
    print("Loading data...")
    unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
    users = pd.read_table('2_users.dat', sep='::', header=None, names=unames)

    rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
    ratings = pd.read_table('2_ratings.dat', sep='::', header=None, names=rnames)

    mnames = ['movie_id', 'title', 'genres']
    movies = pd.read_table('2_movies.dat', sep='::', header=None, names=mnames)

    print("\nMerging...\n")
    data = pd.merge(pd.merge(ratings, users), movies)
    print(data.head())

    print("\nPivoting...\n")
    mean_ratings = data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')
    print(mean_ratings.head())

    print("\nFinding movies with at least 250 ratings...\n")
    ratings_by_title = data.groupby('title').size()
    active_titles = ratings_by_title.index[ratings_by_title >= 250]
    print(active_titles[:5])

    mean_ratings = mean_ratings.ix[active_titles]

    print("\nTop 10 movies as rated by females...\n")
    top_female_ratings = mean_ratings.sort_index(by='F', ascending=False)
    print(top_female_ratings[:10]['F'])

    print("\nMovies with the greatest difference, preferred by women...\n")
    mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
    sorted_by_diff = mean_ratings.sort_index(by='diff')
    print(sorted_by_diff[:15])

    print("\nMovies with the greatest difference, preferred by men...")
    print(sorted_by_diff[::-1][:15])

    print("\nMovies with the most disagreement amongst viewers in general (largest standard deviation in ratings)...\n")
    rating_std_by_title = data.groupby('title')['rating'].std()
    rating_std_by_title = rating_std_by_title[active_titles]
    print(rating_std_by_title.order(ascending=False)[:10])


if __name__ == '__main__':
    main()
