from PIL import Image
import matplotlib.pyplot as plt
import csv
import numpy as np


with open('movies_by_year.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    array = list()
    for i, row in enumerate(reader):
        if i == 0:
            continue
        array.append([float(item) for item in row[1:]])
image = Image.fromarray(np.asarray(array))
image.save('movies_by_year.tiff')
