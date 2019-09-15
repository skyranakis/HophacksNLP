syntactic_tests = [['How tall is Tom Cruise?', 'Tom Cruise height', 'Brad Pitt height'],
                   ['Tom Cruise height', 'Brad Pitt height', 'Brad Pitt age']]

syntactic_expected_results = [['How tall is Brad Pitt?'],
                              ['Tom Cruise age']]