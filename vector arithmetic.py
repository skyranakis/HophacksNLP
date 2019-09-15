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
