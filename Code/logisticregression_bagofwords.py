import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn import preprocessing
import re
import argparse
import matplotlib.pyplot as plt
import pydotplus
import collections
from gensim import corpora
from gensim import matutils


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

def remove_postag(sent_list_1, sent_list_2, target_word_1, target_word_2):
    """Remove the pos tag"""
    update_sent_list = []
    for i in sent_list_1:
        sent = []
        for x in i:
            if x[0] != target_word_1:
                sent.append(x[0])
        update_sent_list.append(sent)
    for i in sent_list_2:
        sent = []
        for x in i:
            if x[0] != target_word_2:
                sent.append(x[0])
        update_sent_list.append(sent)
    return update_sent_list

def gensimthings(sent_list):
    """Creates a bag of words model"""
    dictionary = corpora.Dictionary(sent_list)
    sparse_vector = [dictionary.doc2bow(tokens) for tokens in sent_list]
    dense_vector= matutils.corpus2dense(sparse_vector,num_terms=len(dictionary.token2id))
    vocab = list(dictionary.values())
    return dense_vector.T, vocab

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
            sent_list_1, target1 = sent_list(sentences, target_word_1, 0)
            sent_list_2, target2 = sent_list(sentences, target_word_2, 1)
            total_sent_list = remove_postag(sent_list_1, sent_list_2, target_word_1, target_word_2)
            data, vocab = gensimthings(total_sent_list)
            target = np.concatenate((target1,target2), axis=0)

        model = LogisticRegression()
        model.fit(data,target)
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
        importance = model.coef_[0]
        importance = importance[340:380]
        vocab = vocab[340:380]
        plt.bar([x for x in range(len(importance))], importance)
        plt.xticks(range(len(importance)), vocab, rotation='vertical', fontsize=7)
        plt.ylabel('Stuðull')
        plt.title('Mikilvægi þátta með orðaskjóðu, lógístískt aðhvarf')
        plt.show() # A bar chart containing the importance of each feature (should be restricted in order to be readable)
        
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F-score: " ,fscore)
    

parser = argparse.ArgumentParser()
parser.add_argument('filename') # Sentence examples
parser.add_argument('wordfile') # List of words
args = parser.parse_args()

automate(args.wordfile)

