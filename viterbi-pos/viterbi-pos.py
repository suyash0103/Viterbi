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

# Dictionary to store frequency of each Tag
tag_frequency = {}

""" Calculating Transition Probability """
# val = transition_prob['VERB']
# print (val)
# print (sum(val.values()))
# divisor = sum(val.values())
# print (val.items())
# for in_key in val:
#     # Evaluate c(VERB NOUN) / c(VERB)
#     val[in_key] /= divisor
# val = sorted(val, key=lambda x : x[0])
# print (val)

# print (transition_prob['VERB'])
# P(NOUN | VERB) = c(VERB NOUN) / c(VERB) -> Transition Probability
for out_key in transition_prob:
    out_value = transition_prob[out_key]

    # Calculate c(VERB)
    divisor = sum(out_value.values())
    tag_frequency[out_key] = tag_frequency.get(out_key, 0)
    tag_frequency[out_key] = divisor

    for in_key in out_value:
        # Evaluate c(VERB NOUN) / c(VERB)
        out_value[in_key] /= divisor

    # Outer dictionary with key as sorted list
    out_value = out_value.items()
    out_value = sorted(out_value, key = lambda x : x[0])
    transition_prob[out_key] = out_value

# print (transition_prob['VERB'])
# print(tag_frequency)

""" Calculating Emission Probability """
# P(WORD | VERB) = c(VERB WORD) / c(VERB) -> Emission Probability
for out_key in emission_prob:
    out_value = emission_prob[out_key]

    for in_key in out_value:
        # print(in_key)
        # print(out_value[in_key])
        # print(tag_frequency[in_key])
        # Evaluate c(VERB WORD) / c(VERB)
        out_value[in_key] /= tag_frequency[in_key]
        # print(out_value[in_key])

    # Outer dictionary with key as sorted list
    out_value = out_value.items()
    out_value = sorted(out_value, key=lambda x: x[0])
    emission_prob[out_key] = out_value

# print (emission_prob)

""" TESTING """

testing_file = open("wsj_test.txt", "r")
testing_str = testing_file.read()
testing_data = testing_str.split()

test_words = ['']
test_tags = ['']
final_tags = ['']

testing_data_size = len(testing_data)

test_words *= testing_data_size
test_tags *= testing_data_size
final_tags *= testing_data_size

error = 0

for i in range(testing_data_size):
    temp = testing_data[i].split("/")
    test_words[i] = temp[0]
    test_tags[i] = temp[1]

    if i == 0:
        transition_prob_list =  transition_prob['.']
    else:
        try:
            transition_prob_list = transition_prob[final_tags[i - 1]]
        except:
            transition_prob_list = []

    emission_prob_list = emission_prob.get(test_words[i], '')

    # If testing data word is not found, tag it as NOUN
    if emission_prob_list == '':
        final_tags[i] = 'NOUN'

    else:
        probability = 0
        max_probability = 0
        count_transition_prob = 0
        count_emission_prob = 0

        while count_emission_prob < len(emission_prob_list) and count_transition_prob < len(transition_prob_list):
            transition_tag = transition_prob_list[count_transition_prob][0]
            emission_tag = emission_prob_list[count_emission_prob][0]

            if transition_tag < emission_tag:
                count_transition_prob += 1
            elif emission_tag < transition_tag:
                count_emission_prob += 1
            else:
                probability = transition_prob_list[count_transition_prob][1] * emission_prob_list[count_emission_prob][1]
                if max_probability < probability:
                    max_probability = probability
                    final_tags[i] = transition_tag
                count_transition_prob += 1
                count_emission_prob += 1

    if final_tags[i] == '':
        final_tags[i] = max(emission_prob_list, key = itemgetter(1))[0]

    if final_tags[i] != test_tags[i]:
        error += 1

print ("Fraction of errors (Viterbi) : ",(error/len(test_tags)))

print ("Tags suggested by Viterbi Algorithm : ", final_tags)

print ("Correct tags : ", test_tags)