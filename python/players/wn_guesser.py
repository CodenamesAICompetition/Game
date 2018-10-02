from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import wordnet_ic
from nltk.corpus import genesis
from itertools import product
from nltk.stem import WordNetLemmatizer


def word_synset(word_a, word_b, lch_threshold=2.15, verbose=True):

    brown_ic = wordnet_ic.ic('ic-brown.dat')
    semcor_ic = wordnet_ic.ic('ic-semcor.dat')
    results = []

    for list_a in wordnet.synsets(word_a):
        for list_b in wordnet.synsets(word_b):

            try:
                lch = list_a.lch_similarity(list_b)

            except:
                continue

            # The value to compare the LCH to was found empirically.
            # (The value is very application dependent. Experiment!)

            if lch >= lch_threshold:
                results.append((list_a, list_b))

    if not results:
        return False

    if verbose:

        for list_a, list_b in results:
            print("path:\t", list_a.path_similarity(list_b))
            print("lch:\t", list_a.lch_similarity(list_b))
            print("wup:\t", list_a.wup_similarity(list_b))

    return True


    # res_brown = synset_array_a[0].res_similarity(synset_array_b[0], brown_ic)
    # print("res:\t", res_brown)
    
    # jcn = synset_array_a[0].jcn_similarity(synset_array_b[0], brown_ic)
    # print("jcn:\t", jcn)

    # lin = synset_array_a[0].lin_similarity(synset_array_b[0], brown_ic)
    # print("lin:\t", lin)



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


word_synset("titan", "say")


