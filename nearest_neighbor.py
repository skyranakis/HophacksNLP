from annoy import AnnoyIndex
import pandas as pd

f = 100
t = AnnoyIndex(f, 'angular')  # Length of item vector that will be indexed

query_df = pd.read_csv("test.csv")
num_rows = query_df.shape[0]
print(query_df.shape)

for index, row in query_df.iterrows():
    if index % 10000 == 0:
        print('Currently at {} of {}'.format(index, num_rows))
    t.add_item(index, [float(s) for s in row["vector"][1:-1].split(',')])

t.build(10) # 10 trees
t.save('test.ann')


u = AnnoyIndex(f, 'angular')
u.load('test.ann') # super fast, will just mmap the file
print(u.get_nns_by_item(0, 1000)) # will find the 1000 nearest neighbors
