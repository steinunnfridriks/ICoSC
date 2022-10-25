import csv
import string
import argparse

def collect_words(file):
    """Takes a textfile containing a list of words from a certain category,
    needs to be specified as a command line argument""" 
    wordlist = []
    for i in file:
        i = i.rstrip()
        wordlist.append(i)
    return wordlist

def collect_freqs(wordlist):
    """Returns a list with each word form, lemma, tag and frequency 
    from the corpus total count"""
    freqlist = []
    for i in wordlist:
        found = False
        with open('allfreq.tsv', encoding='utf8') as tsvfile: #allfreq contains all word frequencies from the IGC
            reader = csv.reader(tsvfile, delimiter='\t')
            for row in reader:
                if row[0] == i: # grab the freqs of the appropriate words
                    freqlist.append(row)
                    found = True
        if not found: # if the word does not exist in allfreq
            freqlist.append([i, "0", "n/a", "0"])
    return freqlist

def freqdict(freqlist):
    """Returns a dictionary containing key value pairs with each word form
    and their frequency"""
    result = {}
    for row in freqlist:
        key = row[0]
        count = int(row[3])
        if key in result:
            result[key] += int(count)
        else:
            result[key] = int(count)
    return result

def createconfusionsets(result, freqlist):
    """Returns a zipped list containing the word forms and total freqs, possible pos tags 
    and their freqs for each confusion set, as well as a zipped list with all possible
    pos tags for each confusion set"""
    total_count = [] # word forms of both candidates, total freq, possible pos and individual freqs
    POS_set = [] # all pos tags of both candidates without additional information
    for key, count in result.items(): 
        word_count = [] 
        POS_word = [] 
        word_count.append(key)
        word_count.append(count)
        for i in freqlist:
            if i[0] == key:
                word_count.append(i[2])
                POS_word.append(i[2])
                word_count.append(int(i[3]))
        total_count.append(word_count)
        POS_set.append(POS_word)
    zipped_POS = list(zip(POS_set[::2], POS_set[1::2]))
    zipped_cs = list(zip(total_count[::2], total_count[1::2]))
    return zipped_POS, zipped_cs


def identical_or_disjoint(POS, CS):
    """Checks if the POS tags of each candidate in a confusion set are identical, disjoint or neither.
    Returns a finalized list containing the confusion sets along with their binary categorical information"""
    gramdis = [] # no pos tags shared
    gramid = [] # all pos tags identical
    for i in POS:
        POS1 = set(i[0])
        POS2 = set(i[1])
        if len(POS1.intersection(POS2)) > 0:
            gramdis.append("False")
        else:
            gramdis.append("True")

        if POS1 == POS2:
            gramid.append("True")
        else:
            gramid.append("False")
    zipped_final = list(zip(CS,gramdis,gramid))
    return zipped_final


def writeoutput(zipped_final, zipped_cs, outputfile):
    """Creates a more CSV friendly list. Writes a csv output file, 
    needs to be specified as a command prompt argument"""
    final_list = [] # candidate1&freq, pos&freq, candidate2&freq, pos&freq, GD, GI
    i = 0
    while i < len(zipped_cs):
        placeholder_list = []
        placeholder_list.append(zipped_final[i][0][0][0])
        placeholder_list.append(zipped_final[i][0][0][1])
        placeholder_list.append(zipped_final[i][0][0][2:])
        placeholder_list.append(zipped_final[i][0][1][0])
        placeholder_list.append(zipped_final[i][0][1][1])
        placeholder_list.append(zipped_final[i][0][1][2:])
        placeholder_list.append(zipped_final[i][1][0:])
        placeholder_list.append(zipped_final[i][2][0:])
        i += 1
        final_list.append(placeholder_list)

    with open(args.outputfile, "w", newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(["Word form", "Total count", "POS tags and their frequency","Word form", "Total count", "POS tags and their frequency", "Grammatically disjoint","Grammatically identical"])
        for i in final_list:
            thewriter.writerow(i)

parser = argparse.ArgumentParser()
parser.add_argument('wordlist', help="Specify a text file with a list of word candidates")
outputfile = parser.add_argument('outputfile', help="Specify a csv output file")
args = parser.parse_args()
with open(args.wordlist, encoding='utf8') as data_file:
    total_words = collect_words(data_file)
    freqlist = collect_freqs(total_words)
    result = freqdict(freqlist)
    POS, CS = createconfusionsets(result, freqlist)
    zipped_final = identical_or_disjoint(POS, CS)
    writeoutput(zipped_final, CS, outputfile)