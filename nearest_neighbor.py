from annoy import AnnoyIndex
import pandas as pd

f = 100
t = AnnoyIndex(f, 'angular')  # Length of item vector that will be indexed

query_df = pd.read_csv("test.csv")

for index, row in df.iterrows():
    t.add_item(index, row["vector"])

t.build(10) # 10 trees
t.save('test.ann')


u = AnnoyIndex(f, 'angular')
u.load('test.ann') # super fast, will just mmap the file
print(u.get_nns_by_item(0, 1000)) # will find the 1000 nearest neighbors
