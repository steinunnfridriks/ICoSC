import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn import preprocessing
import re
import argparse
import matplotlib.pyplot as plt
import pydotplus
import collections
from sklearn.linear_model import LogisticRegression

def preprocess(file):
    """Takes a txt file containing all sentence examples from the category as an input. 
    Outputs a list of all sentences from the file """
    data = file.read()
    data = data.split(";;")
    sent = []
    for i in data:
        i = i.split("punctuation")
        for x in i:
            x = x.split()
            sent.append(x)
    return sent


def tuple_sent(sent):
    """Takes each sentence and outputs each word and PoS tag as a tuple"""
    tupled_sentences = []
    for i in sent:
        tupled_sentences.append(list(zip(i[::2], i[1::2])))
    return tupled_sentences


def sent_list(sent, target_word):
    """Checks if the chosen word pair exists in each sentence. 
    Outputs a list of sentences containing the words"""
    sent_list = []
    for i in sent:
        for x in i:
            word = x[0]
            if word == target_word:
                sent_list.append(i)
    return sent_list


def right_left_context(sent, target_word):
    """Outputs the words immediately to the right and left of the target word as well as
    the word two words to the left of the target word"""
    for index, tup in enumerate(sent):
        word = tup[0]
        if word == target_word:
            left_context_word = sent[index-1]
            if index+1 < len(sent):
                right_context_word = sent[index+1]
            else:
                right_context_word = ("(N/A)", "none")
            if 0 <= index-2:
                left_two_context_word = sent[index-2]
            else:
                left_two_context_word = ("(N/A)", "none")
    
    return left_context_word, right_context_word, left_two_context_word


def feature_extraction(sent, target_word):
    """Outputs a feature vector for the target word"""
    target_vector = np.zeros(16)
    LC, RC, LC2 = right_left_context(sent, target_word) 
    nominal_left = re.search(r'^[n|l|f|g|t]', LC[1]) # Words with grammatical case, such as nouns and pronouns
    nominal_right = re.search(r'^[n|l|f|g|t]', RC[1])
    finite_left = re.search(r'^[sb|sf|sv]', LC[1]) # A verb that inflects for person agreement
    finite_right = re.search(r'^[sb|sf|sv]', RC[1])
    nominative_left = re.search(r'^[nn|ln|fn|gn|tn]', LC[1]) 
    nominative_right = re.search(r'^[nn|ln|fn|gn|tn]', RC[1])
    oblique_left = re.search(r'^[no|lo|fo|go|to|nþ|lþ|fþ|gþ|tþ|ne|le|fe|ge|te]', LC[1]) # Has some grammatical case other than nominative
    oblique_right = re.search(r'^[no|lo|fo|go|to|nþ|lþ|fþ|gþ|tþ|ne|le|fe|ge|te]', RC[1])
    particle_left = re.search(r'^[a|c]', LC[1])
    particle_right = re.search(r'^[a|c]', RC[1])
    feminine_two_left = re.search(r'^[fpv|nv]', LC2[1])
    masculine_two_left = re.search(r'^[fpk|nk]', LC2[1])
    infinitive_particle_left = re.search(r'^[cn]', LC[1]) 
    infinitive_particle_right = re.search(r'^[cn]', RC[1])
    infinitive_verb_left = re.search(r'^[sn]', LC[1])
    infinitive_verb_right = re.search(r'^[sn]', RC[1])
    if nominal_left:
        target_vector[0] = 1
    else:
        target_vector[0] = 0
    if nominal_right:
        target_vector[1] = 1
    else:
        target_vector[1] = 0
    if finite_left:
        target_vector[2] = 1
    else:
        target_vector[2] = 0
    if finite_right:
        target_vector[3] = 1
    else:
        target_vector[3] = 0
    if nominative_left:
        target_vector[4] = 1
    else:
        target_vector[4] = 0
    if nominative_right:
        target_vector[5] = 1
    else:
        target_vector[5] = 0
    if oblique_left:
        target_vector[6] = 1
    else:
        target_vector[6] = 0
    if oblique_right:
        target_vector[7] = 1
    else:
        target_vector[7] = 0
    if particle_left:
        target_vector[8] = 1
    else:
        target_vector[8] = 0
    if particle_right:
        target_vector[9] = 1
    else:
        target_vector[9] = 0
    if feminine_two_left:
        target_vector[10] = 1
    else:
        target_vector[10] = 0
    if masculine_two_left:
        target_vector[11] = 1
    else:
        target_vector[11] = 0
    if infinitive_particle_left:
        target_vector[12] = 1
    else:
        target_vector[12] = 0
    if infinitive_particle_right:
        target_vector[13] = 1
    else:
        target_vector[13] = 0
    if infinitive_verb_left:
        target_vector[14] = 1
    else:
        target_vector[14] = 0
    if infinitive_verb_right:
        target_vector[15] = 1
    else:
        target_vector[15] = 0
    
    return target_vector


def automate(wordfile):
    words = []
    accuracy = []
    precision = []
    recall = []
    fscore = []

    with open(args.wordfile, encoding='utf8') as wordfile:
        for word in wordfile:
            words.append(word.rstrip())
    count = 0
    while len(words) > count:
        target_word_1 = words[count]
        count += 1
        target_word_2 = words[count]
        count += 1

        with open(args.filename, encoding='utf8') as data_file: # The datafile contains all sentence examples of the category in consideration
            sent = preprocess(data_file)
            sentences = tuple_sent(sent)
            sent_list_1 = sent_list(sentences, target_word_1)
            sent_list_2 = sent_list(sentences, target_word_2)
            data_matrix_1 = np.zeros([1,16])
            data_matrix_2 = np.zeros([1,16])
            for i in sent_list_1:
                target_vector = feature_extraction(i, target_word_1)
                data_matrix_1 = np.vstack((data_matrix_1, target_vector)) # Create a data matrix for all sentence examples of the target words
            for i in sent_list_2:
                target_vector = feature_extraction(i, target_word_2)
                data_matrix_2 = np.vstack((data_matrix_2, target_vector)) 
            N1,D1 = data_matrix_1.shape
            N2,D2 = data_matrix_2.shape
            target1 = np.zeros(N1)
            target2 = np.ones(N2)
            target = np.concatenate((target1,target2), axis=0)
            data = np.concatenate((data_matrix_1, data_matrix_2), axis=0) # A unified data matrix containing all examples for both candidates
            data = preprocessing.scale(data)
            feature_names = ["LW nom", "RW nom", "LW finite", "RW finite", "LW nomin", "RW nomin", "LW obli", "RW obli", "LW partic", "RW partic", "L2 femin", "L2 masc"]

        model = LogisticRegression()

        cross_val_accuracy_scores = cross_val_score(model, data, target, cv=10)
        cross_val_precision_scores = cross_val_score(model, data, target, cv=10, scoring="precision")
        cross_val_recall_scores = cross_val_score(model, data, target, cv=10, scoring="recall")
        cross_val_f1_scores = cross_val_score(model, data, target, cv=10, scoring="f1")
        print("Results for", target_word_1, "and", target_word_2)
        #print("Cross validation accuracy scores:", cross_val_accuracy_scores) # All cross val scores individually
        sumav = sum(cross_val_accuracy_scores) / 10 # Average over all cross val scores
        print("Average accuracy:", sumav)
        #print("Cross validation precision scores:", cross_val_precision_scores)
        sumav2 = sum(cross_val_precision_scores) / 10
        print("Average precision:", sumav2)
        #print("Cross validation recall scores:", cross_val_recall_scores)
        sumav3 = sum(cross_val_recall_scores) / 10
        print("Average recall:", sumav3)
        #print("Cross validation F1 scores:", cross_val_f1_scores)
        sumav4 = sum(cross_val_f1_scores) / 10
        print("Average F1:", sumav4)
    
        accuracy.append(sumav)
        precision.append(sumav2)
        recall.append(sumav3)
        fscore.append(sumav4)
        
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F-score: " ,fscore)
    

parser = argparse.ArgumentParser()
parser.add_argument('filename') # Sentence examples
parser.add_argument('wordfile') # Word list
args = parser.parse_args()

automate(args.wordfile)