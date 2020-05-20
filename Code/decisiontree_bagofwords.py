import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import re
import argparse
import matplotlib.pyplot as plt
import pydotplus
import collections
#import gensim
#from gensim import corpora
#from gensim import matutils


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


def sent_list(sent, target_word, n):
    """Checks if the chosen word pair exists in each sentence. 
    Outputs a list of sentences containing the words"""
    sent_list = []
    target_vector = []
    for i in sent:
        for x in i:
            word = x[0]
            if word == target_word:
                sent_list.append(i)
                target_vector.append(n)
    return sent_list, target_vector

def remove_postag(sent_list_1, sent_list_2):
    """Remove the pos tag"""
    vocab = []
    update_sent_list = []
    for i in sent_list_1:
        sent = []
        for x in i:
            vocab.append(x[0])
            sent.append(x[0])
        update_sent_list.append(sent)
    for i in sent_list_2:
        sent = []
        for x in i:
            vocab.append(x[0])
            sent.append(x[0])
        update_sent_list.append(sent)
    return vocab, update_sent_list

#def gensimthings(sent_list):
#    dictionary = corpora.Dictionary(sent_list)
    #dictionary.filter_n_most_frequent(1000)
#    sparse_vector = [dictionary.doc2bow(tokens) for tokens in sent_list]
#    dense_vector= matutils.corpus2dense(sparse_vector,num_terms=len(dictionary.token2id))
#    return dense_vector.T
 
def generate_bow(vocab, sent_list, target_word_1, target_word_2):
    unique_vocab = {}
    for i in vocab:
        if i != target_word_1:
            if i != target_word_2:
                if i in unique_vocab:
                    unique_vocab[i] += 1
                else:
                    unique_vocab[i] = 1

    vocab_list = []
    for key, value in unique_vocab.items():
        vocab_list.append(key)

    data_matrix = np.zeros(len(vocab_list))
    for sentence in sent_list:
        bow_vector = np.zeros(len(vocab_list))
        for word in sentence:
            for i, w in enumerate(vocab_list):
                if word == w:
                    bow_vector[i] += 1
        data_matrix = np.vstack((data_matrix, bow_vector))
    data_matrix = np.delete(data_matrix, 0,0)
    return data_matrix, vocab_list

def automate(wordfile): # Makes it possible to calculate all word pairs of a certain category rather than running it over and over again by hand
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
            sent_list_1, target1 = sent_list(sentences, target_word_1, 0)
            sent_list_2, target2 = sent_list(sentences, target_word_2, 1)
            vocab, total_sent_list = remove_postag(sent_list_1, sent_list_2)
            data, vocab_list = generate_bow(vocab, total_sent_list, target_word_1, target_word_2)
            #data_matrix_2 = gensimthings(sent_list_2)
            target = np.concatenate((target1,target2), axis=0)

        clf = tree.DecisionTreeClassifier()

        cross_val_accuracy_scores = cross_val_score(clf, data, target, cv=10)
        cross_val_precision_scores = cross_val_score(clf, data, target, cv=10, scoring="precision")
        cross_val_recall_scores = cross_val_score(clf, data, target, cv=10, scoring="recall")
        cross_val_f1_scores = cross_val_score(clf, data, target, cv=10, scoring="f1")
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
parser.add_argument('filename') # This is a file containing sentence examples
parser.add_argument('wordfile') # This is a file that contains a list of words meant to be analyzed
args = parser.parse_args()

automate(args.wordfile)
