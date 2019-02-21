from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import wordnet_ic
from numpy.linalg import norm
from operator import itemgetter
from numpy import *
import gensim.models.keyedvectors as word2vec
import gensim.downloader as api
import itertools
import numpy as np
import random
import scipy


def cm():
    word_vectors = word2vec.KeyedVectors.load_word2vec_format(
        'GoogleNews-vectors-negative300.bin', binary=True, unicode_errors='ignore')
    cm_wordlist = []
    with open('cm_wordlist.txt') as infile:
        for line in infile:
            cm_wordlist.append(line.rstrip())

    num_best = np.inf

    # red_words = ['death', 'wake', 'date', 'cap', 'oil', 'comic', 'fish', 'log']
    red_words = ['staff', 'shadow', 'string', 'block', 'plate', 'beijing', 'pie', 'berry']
    # red_words = ['kiwi', 'lemon', 'scuba', 'line', 'spider', 'copper', 'olive', 'maple']
    # red_words = ['point', 'leprechaun', 'knife', 'nurse', 'face', 'pyramid', 'van', 'watch']

    li = []
    for word in reversed(cm_wordlist):
        for i in range(len(red_words)):
            for j in range(i, len(red_words)):
                try:
                    dist = scipy.spatial.distance.cosine(word_vectors[word],
                        slerp(word_vectors[red_words[i]], word_vectors[red_words[j]], 0.5))

                    if dist < num_best and word not in red_words and arr_not_in_word(word, red_words):
                        num_best = dist
                        word_best = word
                        print("Best: ", word_best)
                        li.append((num_best, word_best))
                except:
                    continue

    li = list(sorted(li))
    print(li)
    return [li[0][1], 1]


def arr_not_in_word(word, arr):
    for i in arr:
        if(i in word):
            return False
    return True


def slerp(p0, p1, t):
    omega = arccos(dot(p0/norm(p0), p1/norm(p1)))
    so = sin(omega)
    return sin((1.0-t)*omega) / so * p0 + sin(t*omega)/so * p1


def do_imp(name):
    name = "package." + name
    mod = import(name, fromlist=[''])
    mod.do_imp()

    python3 game.py human  someone_elses_codemaster
    import('package.someone_elses_codemaster')
    codemaster_bot = import('package.someone_elses_codemaster')()


s = cm()
print(s)



