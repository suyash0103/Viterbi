from __future__ import division #To avoid integer division
from operator import itemgetter

""" TRAINING """

training_file = open("wsj_training.txt", "r")
training_str = training_file.read()
training_data = training_str.split()
print (training_data)

