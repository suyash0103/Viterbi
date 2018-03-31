from __future__ import division #To avoid integer division
from operator import itemgetter

""" TRAINING """

training_file = open("wsj_training.txt", "r")
training_str = training_file.read()
training_data = training_str.split()
print (training_data)

train_words = ['']
train_tags = ['']

training_data_size = len(training_data)
train_words *= training_data_size
train_tags *= training_data_size

for i in range(0, training_data_size):
    word_tag = training_data[i].split('/')
    train_words[i] = word_tag[0]
    train_tags[i] = word_tag[1]
    # print (i, train_words[i], train_tags[i])


# TRANSITION PRABABILITY
transition_prob = {}

# EMISSION PROBABILITY
emission_prob = {}