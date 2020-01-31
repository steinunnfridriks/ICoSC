# ICoSC

**The Icelandic Confusion Set Corpus (ICoSC) is available under a CC-BY licence for anyone wanting to run their own experiment or replicate ours. It was compiled during the course of three months in 2019 by Steinunn Rut Friðriksdóttir and Anton Karl Ingason of the language technology department in the University of Iceland.**


## **Content:**
The ICoSC consists of the following categories of confusion sets, selected for their linguistic properties as homophones, separated orthographically by a single letter. The categories are:

•**196  pairs  containing  y/i (leyti _’extent’_ / leiti _’search’_)**:  
In modern Icelandic,  there is no phonetic  distinction between  these sounds (both of which are pronounced as [ɪ]) and thus their distinction is purely historical. The use of y refers to a vowel mutation from another, related word, some of which are derived from Danish. Confusing words that differ only by these letters is therefore very common when writing Icelandic.

•**150 pairs containing ý/í (sýn _’vision’_ / sín _’theirs (possessive reflexive)’_)**: 
The same goes for these sounds, which are both pronounced as [i]. The original rounding of y and ý started merging with the unrounded counterparts of these sounds in the 14th century and the sounds in question have remained merged since the 17th century (Gunnlaugsson, 1994).

•**1203 pairs containing nn/n (forvitinn _’curious(masc.)’_ / forvitin _’curious (fem.)’_)**:  
The alveolar nasal [n] is not elongated in pronunciation and therefore there is no real distinction between these sounds in pronunciation (although the preceding vowel to a double n is often elongated). The distinction between them is often grammatical and refers to whether the word has a feminine or masculine grammatical gender. However, the rules on when to write each vary and have many exceptions, many of which are taught as something to remember by heart. It is therefore common for both native and nonnative speakers to make spelling and/or grammar mistakes in these type of words.

•**8 pairs commonly confused by Icelandic speakers**:  
These confusion sets could prove useful in grammar correction as their difference is in their morphological information rather than their orthography. These include for example _mig/mér_ (_me_ (accusative) / _me_ (dative)) which commonly get confused when followed by experiencer-subject verbs (Jónsson  and  Eythórsson, 2005; Ingason, 2010; Thráinsson, 2013; Nowenstein, 2017). 

•**24 pairs containing hv/kv (hvað _’what’_ / kvað _’chanted’_)**:
Hv and kv are homophones for the majority of Icelandic speakers.

•**42 pairs containing rð/ðr (veðri _’weather (dative)’_ / verði _’will become’_)**:
Included due to their potential confusability, though they are not homophones. 

•**110 pairs containing rr/r (klárri _’smart (indef. fem. dative)’_ / klári _’smart (def. masc. nominative)’_)**:
Included due to their potential confusability, as the pronunciation difference is only in the preceding vowel. 

Included in the ICoSC are spreadsheets containing all collected confusion sets of each category and their frequencies. The spreadsheets are organized so that for each set, the total frequency of each candidate is calculated  along  with the frequency of each possible PoS tag for that candidate. The seventh and eight column of the tables contain binary values referring to whether the confusion set is grammatically disjoint (all PoS tags differ for the two candidates) or grammatically identical (all PoS tags are identical for the two candidates). The final column shows the frequency of the less frequent candidate of the set which can be used to determine which sets are viable in an experiment. Also included are text files containing the list of words from each category and text files containing all sentence examples from the IGC including the words for each category. As the n/nn examples are by far the most frequent confusion sets, the corpus also includes a word list and sentence examples for the 55 most frequent sets. All files have UTF-8 encoding.



## **Code:**

•**gen_totalfreqs_totalsents.py** generates a TSV file (allfreq.tsv) containing the word form, lemma, POS tag and frequency of each word in the Icelandic Gigaword Corpus, as well as a CSV file (all_sent.csv) containing all sentences from the IGC as lists. It is dependent on the IGC. 

•**gen_wordlist.py** generates a txt file containing a list of viable confusion sets for each category. It is dependent on the wordlist provided by the Database of Modern Icelandic Inflection (ordmyndalisti.txt), the frequency list from the Icelandic Gigaword Corpus (allfreq.tsv) and the CSV file with all sentence examples (all_sent.csv). 

**Required argparse arguments:** 
Outputfile = A txt file.
Candidate1 = Specific letters to search for within the words of the DMII wordlist, f.ex. y. 
Candidate2 = Specific letters to replace in the words retrieved by candidate1, f.e.x. i. 

•**gen_spreads.py** takes the txt file generated by gen_wordlist as an input and outputs a CSV file, containing frequency tables for the confusion sets of that category. The tables are organized so that for each set, the total frequency of each candidate is calculated along with the frequency of each possible PoS tag for that candidate. The seventh and eight columns of the tables contain binary values referring to whether the confusion set is grammatically disjoint or grammatically identical. The final column shows the frequency of the less frequent candidate of the set which can be used to determine which sets are viable in an experiment. 

**Required argparse arguments:**
Wordlist = A txt file containing a list of confusion set candidates.
Outputfile = A CSV file. 

•**gen_sentence_examples.py** is dependent on the sentences from the IGC (all_sent.csv) generated by gen_totalfreqs_totalsents. It takes the wordlist generated by gen_wordlist as an input, and outputs a txt file containing all the sentence examples for each word, separated by a double semi colon and the word itself.

**Required argparse arguments:**
Wordlist = A txt file containing a list of confusion set candidates.
Outputfile = A txt file.

•**decisiontree_classifier** is dependent on the txt file containing all sentence examples for the chosen category (for example y_sent.txt). Takes a word pair (for example _leyti/leiti_) and looks for the sentence examples containing each candidate. Creates a feature vector for each example and generates a data matrix from all examples, which is then split into test and train data. Runs the data through the Decision tree algorithm provided by Scikit learn and outputs cross validation results for the chosen confusion set, as well as a Graphviz visualization of the tree and a bar chart containing the feature importance.

**Required argparse arguments:**
Filename = A txt file containing all sentence examples from the chosen category. 
Target word 1 = The first candidate of the confusion set in question.
Target word 2 = The second candidate of the confusion set in question. 



## **References:**
• Gunnlaugsson, G. M. (1994). _Um afkringingu á y, ý, ey í íslensku._ Málvísindastofnun Háskóla Íslands.

•Jónsson, J. G. and Eythórsson, T. (2005).  Variation in subject case marking in Insular Scandinavian. _Nordic Journal of Linguistics_, 28.2:223–245.

•Ingason,  A. K. (2010). Productivity  of  non-default  case. _Working papers in Scandinavian syntax_, 85:65–117.

•Nowenstein, I. (2017). Determining the nature of intra-speaker subject case variation. In Thráinsson, Höskuldur, C. H. H. P. P. and Hansen, Z. S., editors, _Syntactic Variation in Insular Scandinavian_, pages 91–112. 

• Thráinsson, H. (2013). Ideal speakers and other speakers. The case of dative and other cases. In Fenández,  B.and  Etxepare,  R.,  editors, _Variation  in  Datives  –  A Micro-Comparative Perspective_, pages 161–188. Oxford University Press.
