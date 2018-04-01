from __future__ import division #To avoid integer division
from operator import itemgetter

""" TRAINING """

training_file = open("wsj_training.txt", "r")
training_str = training_file.read()
training_data = training_str.split()
# print (training_data)

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
""" Dictionary stores keys and values in the form : { tagA : {tagB : number of times tagB follows tagA} } """
transition_prob = {}

# EMISSION PROBABILITY
""" Dictionary stores keys and values in the form : { wordA : {tagA : number of times wordA is tagged with tagA} } """
emission_prob = {}

for i in range(training_data_size - 1):
    # For Dictionary of Transition Probability
    outer_key = train_tags[i]
    inner_key = train_tags[i + 1]
    # If outer_key exists as a key, return its value, or else return an empty dictionary
    transition_prob[outer_key] = transition_prob.get(outer_key, {})
    # If inner_key exists for this particular outer_key, return value of inner dictionary, or else return 0
    transition_prob[outer_key][inner_key] = transition_prob[outer_key].get(inner_key, 0)
    # Increment count
    transition_prob[outer_key][inner_key] += 1

    # For Dictionary of Emission Probability
    outer_key = train_words[i]
    inner_key = train_tags[i]
    # If outer_key exists as a key, return its value, or else return an empty dictionary
    emission_prob[outer_key] = emission_prob.get(outer_key, {})
    # If inner_key exists for this particular outer_key, return value of inner dictionary, or else return 0
    emission_prob[outer_key][inner_key] = emission_prob[outer_key].get(inner_key, 0)
    # Increment count
    emission_prob[outer_key][inner_key] += 1

# print (transition_prob['VERB'])

""" First word of sentence comes after a '.' But first tag of document has no prior '.' Following code considers that """
transition_prob['.'] = transition_prob.get('.', {})
transition_prob['.'][train_tags[0]] = transition_prob['.'].get(train_tags[0], 0)
transition_prob['.'][train_tags[0]] += 1

""" Considering last word and tag of document, since it is not included in the above for loop """
index = training_data_size - 1
outer_key = train_words[index]
inner_key = train_tags[index]
# If outer_key exists as a key, return its value, or else return an empty dictionary
emission_prob[outer_key] = emission_prob.get(outer_key, {})
# If inner_key exists for this particular outer_key, return value of inner dictionary, or else return 0
emission_prob[outer_key][inner_key] = emission_prob[outer_key].get(inner_key, 0)
# Increment count
emission_prob[outer_key][inner_key] += 1

