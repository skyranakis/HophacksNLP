import sys
import requests
import json
import numpy as np
import pandas as pd


def create_query_line(queries):
    line = '{"queries": ["'
    for i, query in enumerate(queries[:-1]):
        line += query
        line += '", "'
    line += queries[-1]
    line += '"]}'
    return line


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.sqrt(np.sum(np.square(a))) * np.sqrt(np.sum(np.square(b))))


nolan = ['Memento', 'Batman Begins', 'The Prestige', 'The Dark Knight',
         'Inception', 'The Dark Knight Rises', 'Interstellar', 'Dunkirk']
tarantino = ['Reservoir Dogs', 'Pulp Fiction', 'Jackie Brown', 'Kill Bill',  'Inglourious Basterds',
             'Django Unchained', 'The Hateful Eight', 'Once Upon a Time in Hollywood']
scorsese = ['Mean Streets', 'Taxi Driver', 'Raging Bull', 'Cape Fear', 'Goodfellas', 'Casino',
            'Gangs of New York', 'The Departed', 'The Wolf of Wall Street']
spielberg = ['Jaws', 'Close Encounters of the Third Kind', 'ET: the Extra-Terrestrial',
             'Jurassic Park', 'Schindler\'s List', 'Saving Private Ryan', 'Catch Me if You Can',
             'The Terminal', 'Lincoln', 'Ready Player One']
kubrik = ['Spartacus', '2001: A Space Odyssey', 'A Clockwork Orange', 'Full Metal Jacket',
          'The Shining', 'Eyes Wide Shut']
wright = ['Shaun of the Dead', 'Hot Fuzz', 'Scott Pilgrim vs. the World', 'The World\'s End', 'Baby Driver']
hitchcock = ['Rear Window', 'North by Northwest', 'The Birds', 'Psycho', 'Strangers on a Train', 'Vertigo']
scott = ['Alien', 'Blade Runner', 'Gladiator', 'Black Hawk Down', 'The Martian']

movies = nolan + tarantino + scorsese + spielberg + kubrik + wright + hitchcock + scott

queries = ["Who directed {}?".format(movie) for movie in movies]

headers = {
    'Ocp-Apim-Subscription-Key': sys.argv[1],
}
response = requests.post('https://api.msturing.org/gen/encode',
                         headers=headers,
                         data=create_query_line(queries))
data = json.loads(response.text)
print(data)
vector_dict = {}
for i in range(len(movies)):
    vector_dict[movies[i]] = data[i]['vector']

num_movies = len(movies)
similarity = np.zeros((num_movies, num_movies))
for i in range(num_movies):
    for j in range(i, num_movies):
        similarity[i][j] = cosine_similarity(vector_dict[movies[i]], vector_dict[movies[j]])

df = pd.DataFrame(similarity)
df.columns = movies
df.rows = movies

df.to_csv('movies_by_director.csv')
