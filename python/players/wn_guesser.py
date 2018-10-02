from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import wordnet_ic
from nltk.corpus import genesis
from itertools import product
from nltk.stem import WordNetLemmatizer


def word_synset(word_a, word_b):

    if not word_a in words.words() and not word_b in words.words():
        print("Not a word")

    brown_ic = wordnet_ic.ic('ic-brown.dat')
    semcor_ic = wordnet_ic.ic('ic-semcor.dat')

    potato_list = []
    synset_array_a = wordnet.synsets(word_a)
    synset_array_b = wordnet.synsets(word_b)

    # for i in synset_array_a:
    #   for j in synset_array_b:

    #       temp_a = synset_array_a.
    #       .lch_similarity(word_b)

    # wup returns a score of 0 - 1, where 1 is a higher probabilty in favor
    wup = max((wordnet.wup_similarity(s1, s2) or 0, s1, s2) for s1, s2 in product(synset_array_a, synset_array_b))
    print("wup:\t", wup)

    
    path = max((wordnet.path_similarity(s1, s2) or 0, s1, s2) for s1, s2 in product(synset_array_a, synset_array_b))
    print("path:\t", path)

    # lch must have same part of speech --> noun vs noun
    # lch gives a score of 3.6~ for maximum similarity (literally identical)
    # lch also gives a score of 2.484 for immediate childs/parents, such as apple.n.01, and pear.n.01
    # this command takes a while
    lch = wordnet.lch_similarity(synset_array_a[0], synset_array_b[0])
    print("lch:\t", lch)

    # res will give pretty high numbers, the higher the number ~12 the greater the similarity
    res_brown = synset_array_a[0].res_similarity(synset_array_b[0], brown_ic)
    print("res:\t", res_brown)
    
    jcn = synset_array_a[0].jcn_similarity(synset_array_b[0], brown_ic)
    print("jcn:\t", jcn)

    lin = synset_array_a[0].lin_similarity(synset_array_b[0], brown_ic)
    print("lin:\t", lin)



def is_word(word_a, word_b):

    if not word_a in words.words() or not word_b in words.words():
        return "Not a word"

    
def check_singular(wordy):

    bool_plur, lemma = is_plural(wordy)
    print(wordy, lemma, bool_plur)

    # if word is plural return true, elsewise false
    return bool_plur


def is_plural(wordy):

    wnl = WordNetLemmatizer()
    lemma = wnl.lemmatize(wordy, 'n')
    plural = True if wordy is not lemma else False
    return plural, lemma


word_synset("say", "titan")


