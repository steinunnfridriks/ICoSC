import glob
from collections import Counter
import xml.etree.ElementTree
import csv
import sys
import operator
import time
import re
import collections

def findFiles(path): return glob.glob(path)
output_file = 'allfreq.tsv'

# XML namespace
ns = {'tei': 'http://www.tei-c.org/ns/1.0' }
sentences = []

def text_words(teifile):
    # Returns word freqs and sentence examples from all words in the corpus
    root = xml.etree.ElementTree.parse(teifile).getroot()
    for asentence in root.findall('.//tei:s',ns):
        sentence = []
        for i in asentence[0:]:
            word_form = i.text
            pos_tag = i.get('type')
            sentence.append(word_form)
            sentence.append(pos_tag)
        sentences.append(sentence)

    for aword in root.findall('.//tei:w',ns): 
        word = aword.text
        word = word.lower()
        word = re.sub(r'[^\w\s]','',word)
        lemma = aword.get('lemma')
        lemma = lemma.lower()
        lemma = re.sub(r'[^\w\s]','',lemma)
        tag = aword.get('type')
        tag = re.sub(r'[^\w\s]','',tag)

        yield '{}\t{}\t{}'.format(word,lemma,tag)

# counter object that updates word form frequencies file by file        
c = Counter()

for filename in findFiles('risamalheild/*/*.xml'):
    c.update((text_words(filename)))

# write sentence examples to file
with open("all_sent.csv", "w", newline='', encoding="utf-8") as f:
    thewriter = csv.writer(f)
    for i in sentences:
        thewriter.writerow(i)           

# sort frequency list in reverse order by counts (most frequent first)
sorted_words = reversed(sorted(c.items(), key=operator.itemgetter(1)))

# make tab formatted entries for output file
allwords = ['{}\t{}'.format(x[0],x[1]) for x in sorted_words]

# write freqs to file
with open(output_file, 'w', encoding="utf-8") as f:
    f.write('\n'.join(allwords))
