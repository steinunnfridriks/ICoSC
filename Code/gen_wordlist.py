import argparse 
import csv
import time
start_time = time.clock()

MII_wordlist = open("ordmyndalisti.txt", "r", encoding='utf-8')

def grab_MII_words(MII_wordlist):
    """Returns a list of all words from the Database of Modern Icelandic Inflection"""
    all_words = []
    for word in MII_wordlist:
        word = word.rstrip()
        word = word.lower()
        all_words.append(word)
    return all_words    


def word_in_allfreq(all_words):
    """Check if the words from the DoMII actually exist in the Gigaword corpus"""
    actual_words = []
    freqwords = []
    with open('allfreq.tsv', encoding='utf8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            freqwords.append(row[0])
    for word in all_words:
        if word in freqwords:
            actual_words.append(word)
    return actual_words


def find_candidate1(actual_words):
    """Returns a list of all words containing CS candidate 1"""
    cand1words = []
    for word in actual_words:
        if args.candidate1 in word:
            cand1words.append(word) 
    return cand1words


def check_candidate2(cand1words):
    """Replaces candidate 1 with candidate 2 (both instances if more than one appearance).
    Returns a list of words without considering if the changed word really exists"""
    word_list = []
    for word in cand1words:
        newword = word.replace(args.candidate1, args.candidate2, 1)
        newword_backwards = word[::-1].replace(args.candidate1, args.candidate2,1)
        newword_backwards = newword_backwards[::-1]
        word_list.append(newword)
        word_list.append(newword_backwards)
    return word_list


def check_if_real_word(word_list,cand1words):
    """Checks if the words from the previous function exist in the MII.
    Really slow"""
    real_words = []
    for i in all_words:
        if i in word_list:
            real_words.append(i)
    return real_words

def check_sent(real_words):
    """Check if there are sentence examples containing these words in the IGC"""
    words = []
    with open("all_sent.csv", "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            for i in real_words:
                if i in row:
                    if i not in words:
                        words.append(i)
    return words

def check_things(words, cand1words):
    """Returns a list of viable confusion sets"""
    cslist = [] # Do the words in real_words have counterparts with the other candidate?
    for i in words:
        cslist.append(i)
        newword = i.replace(args.candidate2, args.candidate1,1)
        if newword in cand1words:
            cslist.append(newword)
    cs_list = [] # Make sure only one copy of each word makes it to the final list
    for i in cslist:
        if i not in cs_list:
            cs_list.append(i)
    cs_final = [] # Finalized confusion sets with only two words per pair, making sure no triples make it through
    i = 0
    while i <= (len(cs_list) - 2):
        cand1 = cs_list[i]
        if cs_list[i+1] == cand1.replace(args.candidate2, args.candidate1, 1):
            cs_final.append(cs_list[i])
            cs_final.append(cs_list[i+1])
        i += 1
    return cs_final

def write_output(cs_final):
    """Specify outputfile as a command prompt argument"""
    with open(args.outputfile, 'w', encoding='utf8') as f:
        for i in cs_final:
            f.write(str(i) + '\n')

parser = argparse.ArgumentParser()
outputfile = parser.add_argument('outputfile', help="Specify a txt output file")
candidate1 = parser.add_argument('candidate1', help="Which letters does candidate 1 contain?")
candidate2 = parser.add_argument('candidate2', help="Which letters does candidate 2 contain?")
args = parser.parse_args()

all_words = grab_MII_words(MII_wordlist)
actual_words = word_in_allfreq(all_words)
cand1words = find_candidate1(actual_words)
word_list = check_candidate2(cand1words)
real_words = check_if_real_word(word_list, cand1words)
words = check_sent(real_words)
cs_final = check_things(words, cand1words)
write_output(cs_final)

print("--- %s seconds ---" % (time.clock() - start_time))
