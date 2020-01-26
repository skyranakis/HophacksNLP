import subprocess
import json
import numpy as np
import os
import time
import random
import string
import requests


letters = string.ascii_lowercase
queries = [''.join(random.choice(letters)
           for i in range(random.randint(1, 50))) for _ in range(100)]


def create_query_line(queries):
    line = '{"queries": ["'
    for i, query in enumerate(queries[:-1]):
        line += query
        line += '", "'
    line += queries[-1]
    line += '"]}'
    return line


headers = {
    'Ocp-Apim-Subscription-Key': '',
}
response = requests.post('https://api.msturing.org/gen/encode',
                         headers=headers,
                         data=create_query_line(queries))

data = json.loads(response.text)

vector_0 = np.asarray(data[0]['vector'], dtype=np.float32)
vector_1 = np.asarray(data[1]['vector'], dtype=np.float32)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.sqrt(np.sum(np.square(a))) * np.sqrt(np.sum(np.square(b))))


print("Query 0: " + data[0]['query'])
print("Query 1: " + data[1]['query'])
print(cosine_similarity(vector_0, vector_1))
