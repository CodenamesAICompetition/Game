from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import wordnet_ic
from itertools import product

def word_synset(word_a, word_b):

        if not word_a in words.words() and not word_b in words.words():
            print("Not a word")

        brown_ic = wordnet_ic.ic('ic-brown.dat')

        potato_list = []
        synset_array_a = wordnet.synsets(word_a)
        synset_array_b = wordnet.synsets(word_b)

        # for i in synset_array_a:
        # 	for j in synset_array_b:

        # 		temp_a = synset_array_a.
        # 		.lch_similarity(word_b)

        wup = max((wordnet.wup_similarity(s1, s2) or 0, s1, s2) for s1, s2 in product(synset_array_a, synset_array_b))
        print(wup)

        # lch must have same part of speech --> noun vs noun
        # lch gives a score of 3.538 for maximum similarity (literally identical)
        # lch also gives a score of 2.484 for immediate childs/parents, such as apple.n.01, and pear.n.01
        sow = max((wordnet.path_similarity(s1, s2) or 0, s1, s2) for s1, s2 in product(synset_array_a, synset_array_b))
        print(sow)

        #lch = wordnet.lch_similarity(synset_array_a[0], synset_array_b[0])
        #print(lch)

        plow = synset_array_a[0].res_similarity(synset_array_b[0], brown_ic)
        print(plow)
        


word_synset("ocean", "water")




#lch similarity, path similarity, resnik similarity
