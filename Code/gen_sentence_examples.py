import csv
import argparse

def clean_word_list(wordlist):
    """Returns a clean list of words from the txt inputfile, specified as
    an argparse argument"""
    word_list = []
    for i in wordlist:
        i = i.rstrip()
        word_list.append(i)
    return word_list


def total_sentence_list(word_list):
    """Returns a list of all the sentences from the IGC"""
    sentence_list = []
    with open("all_sent.csv", "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        for i in csv_reader:
            sentence_list.append(i)
    return sentence_list


def word_in_sentence(sentence_list, word_list):
    """Returns all sentence examples containing each word from the wordlist"""
    all_sentences = []
    for word in word_list:
        each_word_example = []
        each_word_example.append(word) # The words appear by themselves before the sentence examples
        for sent in sentence_list:
            if word in sent:
                each_word_example.append(sent)
        all_sentences.append(each_word_example)
    return all_sentences


def write_output(all_sentences):
    """Ouputs a txt file with the sentence examples"""
    with open(args.outputfile, "w", newline='', encoding="utf-8") as f:
        for i in all_sentences:
            f.write(";;") # Two semicolons and the word in question used as barriers between sentence examples 
            f.write(i[0])
            f.write('\n')
            for x in i[1:]:
                f.write('\n')
                for p,k in zip(x[0::2], x[1::2]): # Zip a word and it's pos tags as a unit
                    if p.startswith(';;'): # Make sure no sentence actually starts with ;;
                        print("OH NOES")
                    else:
                        f.write(p)
                        f.write('\t') # The word and POS tag seperated by a tab
                        f.write(k)
                        f.write('\n')
            f.write('\n')

parser = argparse.ArgumentParser()
parser.add_argument('wordlist', help="Specify a text file with a list of word candidates")
outputfile = parser.add_argument('outputfile', help="Specify a txt output file")
args = parser.parse_args()
with open(args.wordlist, encoding='utf8') as wordlist:
    word_list = clean_word_list(wordlist)
    sentence_list = total_sentence_list(word_list)
    all_sentences = word_in_sentence(sentence_list, word_list)
    write_output(all_sentences)
