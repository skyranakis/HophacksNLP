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


def compare_in_classes(labels, queries, save):
    headers = {
        'Ocp-Apim-Subscription-Key': sys.argv[1],
    }
    response = requests.post('https://api.msturing.org/gen/encode',
                             headers=headers,
                             data=create_query_line(queries))
    data = json.loads(response.text)
    vector_dict = {}
    for i in range(len(labels)):
        vector_dict[labels[i]] = data[i]['vector']

    num_labels = len(labels)
    similarity = np.zeros((num_labels, num_labels))
    for i in range(num_labels):
        for j in range(i, num_labels):
            similarity[i][j] = cosine_similarity(vector_dict[labels[i]], vector_dict[labels[j]])

    df = pd.DataFrame(similarity)
    df.columns = labels
    df.rows = labels

    df.to_csv(save)


nolan = ['memento', 'batman begins', 'the prestige', 'the dark knight',
         'inception', 'the dark knight rises', 'interstellar', 'dunkirk']
tarantino = ['reservoir dogs', 'pulp fiction', 'jackie brown', 'kill bill', 'inglourious basterds',
             'django unchained', 'the hateful eight', 'once upon a time in hollywood']
scorsese = ['mean streets', 'taxi driver', 'raging bull', 'cape fear', 'goodfellas', 'casino',
            'gangs of new york', 'the departed', 'shutter island', 'the wolf of wall street']
spielberg = ['jaws', 'close encounters of the third kind', 'et: the extra-terrestrial',
             'jurassic park', 'schindler\'s list', 'saving private ryan', 'catch me if you can',
             'the terminal', 'lincoln', 'ready player one']
kubrik = ['spartacus', '2001: a space odyssey', 'a clockwork orange', 'full metal jacket',
          'the shining', 'eyes wide shut']
wright = ['shaun of the dead', 'hot fuzz', 'scott pilgrim vs. the world', 'the world\'s end', 'baby driver']
hitchcock = ['rear window', 'north by northwest', 'the birds', 'psycho', 'strangers on a train', 'vertigo']
scott = ['alien', 'blade runner', 'gladiator', 'black hawk down', 'the martian']

movies_by_director = nolan + tarantino + scorsese + spielberg + kubrik + wright + hitchcock + scott
movies_by_director_queries = ["who directed {}?".format(movie) for movie in movies_by_director]

compare_in_classes(movies_by_director, movies_by_director_queries, 'movies_by_director.csv')

m_2010 = ['inception', 'the social network', 'iron man 2', 'the king\'s speech',
          'scott pilgrim vs. the world', 'shutter island', 'black swan', 'the fighter']
m_2011 = ['the help', 'drive', 'moneyball', 'hugo', 'source code', 'thor',
          'x-men: first class', 'rise of the planet of the apes', 'fast five']
m_2012 = ['the avengers', 'looper', 'the dark knight rises', 'lincoln', 'django unchained',
          'argo', 'the hunger games', 'moonrise kingdom', 'brave', 'zero dark thirty']
m_2013 = ['man of steel', 'gravity', 'iron man 3', 'the conjuring', '12 years a slave',
          'despicable me 2', 'pacific rim', 'world war z', 'american hustle', 'gatsby']
m_2014 = ['gone girl', 'grand budapest hotel', 'edge of tomorrow', 'guardians of the galaxy',
          'captain america: the winter soldier', 'nightcrawler', 'interstellar', 'unbroken', 'birdman', 'whiplash']
m_2015 = ['spotlight', 'the hateful eight', 'mad max:fury road', 'inside out', 'jurassic world', 'the martian',
          'the big short', 'the revenant', 'star wars: the force awakens', 'sicario']
m_2016 = ['la la land', 'doctor strange', 'zootopia', 'moana', 'arrival', 'deadpool',
          'moonlight', 'finding dory', 'suicide squad', 'the nice guys', 'jason bourne']
m_2017 = ['it', 'get out', 'dunkirk', 'wonder woman', 'thor: ragnarok', 'lady bird', 'call me by your name',
          'baby driver', 'the shape of water', 'logan', 'blade runner 2049', 'phantom thread']
m_2018 = ['black panther', 'avengers: infinity war', 'a star is born', 'spider-man: into the spider-verse',
          'a quiet place', 'deadpool 2', 'annihilation', 'bohemian rhapsody', 'venom']

movies_by_year = m_2010 + m_2011 + m_2012 + m_2013 + m_2014 + m_2015 + m_2016 + m_2017 + m_2018
movies_by_year_queries = ["when was {} released?".format(movie) for movie in movies_by_year]

compare_in_classes(movies_by_year, movies_by_year_queries, 'movies_by_year.csv')
