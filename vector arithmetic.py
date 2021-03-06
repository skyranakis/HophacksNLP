from annoy import AnnoyIndex
import sys
import requests
import json
import pandas as pd
import numpy as np

syntactic_tests = [['how tall is tom cruise?', 'tom cruise height', 'brad pitt height'],
                   ['tom cruise height', 'brad pitt height', 'brad pitt age'],
                   ['how many computers are there in the world?', 'how much does a computer weigh?',
                    'how much does an ant weigh?'],
                   ['what color is the sky?', 'what color is the sky', 'how fast is a cheetah']]

syntactic_expected_results = ['how tall is brad pitt?',
                              'tom cruise age',
                              'how many ants are there in the world?',
                              'how fast is a cheetah?']

semantic_tests = [['what is the capital of france?', 'where is paris?', 'where is ottawa?'],
                  ['when was the french revolution?', 'what caused the french revolution?', 'why did world war i start?']]

semantic_expected_results = ['what is the capital of canada?',
                             'when was world war i?']

typo_correction_tests = [['how big is a baseball field', 'how big is a baseball feild', 'star of feild of dreams'],
                         ['what is whole milk?', 'what is hwole milk?', 'cat with srting'],
                         ['how long do cats live?', 'how lng do cats live?', 'how helthy is tea?']]

expected_typo_correction_results = ['star of field of dreams',
                                    'cat with string',
                                    'how healthy is tea']


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


def compare_in_classes(queries, queries_expected_results, save):
    similarity = np.zeros((len(queries), 2))
    headers = {
        'Ocp-Apim-Subscription-Key': sys.argv[1],
    }
    for i, query in enumerate(queries):
        response = requests.post('https://api.msturing.org/gen/encode',
                                headers=headers,
                                data=create_query_line(queries))
        data = json.loads(response.text)
        similarity[i][0] = data[0]['vector'] - data[1]['vector'] + data[2]['vector']

    response = requests.post('https://api.msturing.org/gen/encode',
                            headers=headers,
                            data=create_query_line(queries))
    data = json.loads(response.text)

    for i, row in enumerate(data):
        similarity[i][1] = row[0]['vector']

    df = pd.DataFrame(similarity)
    df.columns = labels

    df.to_csv(save)


def find_and_save_nearest_neighbors(vector, k, indices, save_name):
    u = AnnoyIndex(100, 'angular')
    u.load('test.ann')
    near_indices = u.get_nns_by_vector(vector, k)
    near_queries = [indices.iloc[index]['query'] for index in near_indices]
    near_vectors = [[float(num) for num in indices.iloc[index]['vector'][1:-1].split(', ')] for index in near_indices]
    near_similarities = [cosine_similarity(vec, vector) for vec in near_vectors]
    df = pd.DataFrame([near_queries, near_similarities])
    df.to_csv(save_name)


# indices = pd.read_csv('test.csv')


def do_arithmetic_list(test, indices, name):
    queries = [example for example in test]
    headers = {
        'Ocp-Apim-Subscription-Key': sys.argv[1],
    }
    for i, example in enumerate(queries):
        response = requests.post('https://api.msturing.org/gen/encode',
                                 headers=headers,
                                 data=create_query_line(example))
        data = json.loads(response.text)
        new_vector = np.asarray(data[0]['vector']) - np.asarray(data[1]['vector']) + np.asarray(data[2]['vector'])
        find_and_save_nearest_neighbors(new_vector, 10, indices, name + '_'+ str(i) + '.csv')


do_arithmetic_list(typo_correction_tests, indices, 'typo')


def find_similarity_of_expected(test, expected, name):
    queries = [example for example in test]
    headers = {
        'Ocp-Apim-Subscription-Key': sys.argv[1],
    }
    rows = list()
    for i, example in enumerate(queries):
        response = requests.post('https://api.msturing.org/gen/encode',
                                 headers=headers,
                                 data=create_query_line([example, expected[i]]))
        data = json.loads(response.text)
        new_vector = np.asarray(data[0]['vector']) - np.asarray(data[1]['vector']) + np.asarray(data[2]['vector'])
        expected = np.asarray(data[3]['vector'])
        similarity = cosine_similarity(new_vector, expected)
        rows.append([name + '_' + str(i), expected[i], similarity])
    df = pd.DataFrame(rows)
    df.to_csv(name + '.csv')


find_similarity_of_expected(syntactic_tests, syntactic_expected_results, 'syntactic')

# compare_in_classes(syntactic_tests, syntactic_expected_results, 'syntactic_tests.csv')


# u = AnnoyIndex(f, 'angular')
# u.load('test.ann')
