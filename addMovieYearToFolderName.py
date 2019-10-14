#!/usr/bin/env python3

import argparse
import logging
import os
import re

import tmdbsimple as tmdb

MOVIE_FILE_LOCATION = '/mnt/video/Movies'
TMDP_API_KEY = ''


parser = argparse.ArgumentParser()
parser.add_argument('--test', '-t',
                    help='Dry run...don\'t actually rename the folder',
                    action='store_true')
parser.add_argument('--lucky', '-l',
                    help='Feeling luckly. If there are multiple years found for the query, pick the first one. '
                         'Note, this will be logged as a Warning in the log.',
                    action='store_true')
parser.add_argument('--interactive', '-i',
                    help='If multiple movies years are found, will prompt you to enter the one you want',
                    action='store_true')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO,
                    filename='/tmp/addYearToMovieFolder.log',
                    filemode='a',
                    format='%(levelname)s - %(asctime)s - %(message)s')

def get_movie_folder_names():
    logging.info('Getting folder names')
    movie_names = []
    # for _, dir, _ in os.walk(MOVIE_FILE_LOCATION):
    dir = os.listdir(MOVIE_FILE_LOCATION)
    for name in dir:
        if os.path.isdir(os.path.join(MOVIE_FILE_LOCATION, name)):
            if name.startswith('@'):
                logging.info('Found invalid folder ({}). Skipping...'.format(name))
                continue
            if len(os.listdir(MOVIE_FILE_LOCATION + '/' + name)) < 1:
                logging.info('{} is empty. Skipping'.format(name))
                continue
            movie_names.append(name)
    logging.info('Found {} movies'.format(len(movie_names)))
    return movie_names


def get_movie_year(movie_name):
    tmdb.API_KEY = TMDP_API_KEY
    search = tmdb.Search()
    response = search.movie(query=movie_name)
    movie_data = response['results']
    if movie_data:
        potential_valid_yrs = []
        for i in movie_data:
            if 'release_date' in i:

                # If we find an exact match then we assume it's the right one. Note, this
                # could have issues if a movie of the same name has been done more than once
                if i['title'].lower() == movie_name.lower():
                    logging.info('Found an exact match for movie "{}".'.format(movie_name))
                    potential_valid_yrs.append(i['release_date'].split('-')[0])
                    break
                else:
                    release_year = i['release_date'].split('-')[0]
                    potential_valid_yrs.append(release_year)
        return potential_valid_yrs


if args.lucky and args.interactive:
    print('You cannot be lucky and interactive at the same time. Sorry.')
    exit(1)
movie_list = get_movie_folder_names()
pattern = re.compile('.*\d{4}\)$')
for movie in movie_list:
    # Check to see if the movie already has a date at then end
    if pattern.match(movie):
        logging.info('The movie {} already seems to have a date at the end. Skipping.'.format(movie))
        continue
    movie_year = get_movie_year(movie)
    if not movie_year:
        logging.warning('Could not find a movie year for movie: {}'.format(movie))
        continue
    if len(movie_year) > 1 and args.interactive:
        selected_year = ''
        while selected_year not in movie_year:
            text = 'Found multiple possible years for \"{}\": '.format(movie)
            for year in movie_year:
                text += '{} '.format(year)
            text += '\n'
            selected_year = input(text)
            if selected_year not in movie_year:
                print('Not a valid year. You must choose one from the list above.\n')
        logging.info('User has selected {} for the year.'.format(selected_year))
        new_folder_name = movie + ' (' + selected_year + ')'
    elif len(movie_year) > 1 and not args.interactive and args.lucky:
        logging.info('Autoselecting first year found for movie: {} ({})'.format((movie), movie_year[0]))
        new_folder_name = movie + ' (' + movie_year[0] + ')'
    else:
        logging.warning('Found multiple possible years for movie: {}. Skipping.'.format(movie))
        continue
    if args.test:
        print(os.path.join(MOVIE_FILE_LOCATION, movie) + ' ---> ' + os.path.join(MOVIE_FILE_LOCATION, new_folder_name))
    else:
        logging.info('Renaming {} to {}'.format(movie, new_folder_name))
        try:
            os.rename(os.path.join(MOVIE_FILE_LOCATION, movie), os.path.join(MOVIE_FILE_LOCATION, new_folder_name))
        except OSError as e:
            logging.error('Could not rename {} to {}: {}'.format(movie, new_folder_name, e))
            continue


