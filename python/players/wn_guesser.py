from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import wordnet_ic
from nltk.corpus import genesis
from itertools import product
from nltk.stem import WordNetLemmatizer
from operator import itemgetter


def word_synset(clue, board):

    brown_ic = wordnet_ic.ic('ic-brown.dat')
    wup_results = []
    pat_results = []
    lch_results = []
    res_results = []
    jcn_results = []
    lin_results = []
    count = 0

    for i in (board):
        for clue_list in wordnet.synsets(clue):

            per_clue = wup_clue = pat_clue = res_clue = jcn_clue = lin_clue = 0

            for board_list in wordnet.synsets(i):

                try:
                    # only if the two compared words have the same part of speech
                    wup = clue_list.wup_similarity(board_list)
                    pat = clue_list.path_similarity(board_list)
                    lch = clue_list.lch_similarity(board_list)
                    res = clue_list.res_similarity(board_list, brown_ic)
                    jcn = clue_list.jcn_similarity(board_list, brown_ic)
                    lin = clue_list.lch_similarity(board_list, brown_ic)

                except:
                    continue

                # if lch is non-zero so are the other 3 algorithms (same part of speech was compared)
                if lch:

                    lch_results.append(("lch: ", lch, count, clue_list, board_list, i))
                    res_results.append(("res: ", res, count, clue_list, board_list, i))
                    jcn_results.append(("jcn: ", jcn, count, clue_list, board_list, i))
                    lin_results.append(("lin: ", lin, count, clue_list, board_list, i))
                    count += 1

                    if lch > per_clue:
                        per_clue = lch

                    if res > res_clue:
                        res_clue = res

                    if jcn > jcn_clue:
                        jcn_clue = jcn

                    if lin > lin_clue:
                        lin_clue = lin

                # wup and path_sim always compares regardless of Part of Speech to an extent
                if wup:

                    wup_results.append(("wup: ", wup, count, clue_list, board_list, i))
                    pat_results.append(("pat: ", pat, count, clue_list, board_list, i))
                    count += 1

                    if wup > wup_clue:
                        wup_clue = wup

                    if pat > pat_clue:
                        pat_clue = pat      

            print("lch: ", i, per_clue)
            print("wup: ", i, wup_clue)
            print("res: ", i, res_clue)
            print("jcn: ", i, jcn_clue)
            print("lin: ", i, lin_clue)
            print("pat: ", i, pat_clue)
            print('-'*30)

    # if results list is empty
    if not lch_results:
        return []

    wup_results = list(reversed(sorted(wup_results, key=take_second)))
    pat_results = list(reversed(sorted(pat_results, key=take_second)))
    lch_results = list(reversed(sorted(lch_results, key=take_second)))
    res_results = list(reversed(sorted(res_results, key=take_second)))
    jcn_results = list(reversed(sorted(jcn_results, key=take_second)))
    lin_results = list(reversed(sorted(lin_results, key=take_second)))

    results = [wup_results, pat_results, res_results, lch_results, lin_results, jcn_results]
    return results


def take_second(elem):
    return elem[1]


def test():

    words = ['abc','def','xyz']
    scores =[7, 10, 25]

    score_words = [(s,w) for s,w  in zip(scores,words)]

    print(score_words)
    print(list(reversed(sorted(score_words))))


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


def run():
    
    my_board = ["Potato", "Crab", "Tomato", "Chicken", "Salad", "Titan", "Human", "Puppy", "King", "Peasant", "Phone"]
    sorted_results = (word_synset("Food", my_board))

    # grab the first index of the 2d list in each row
    first_index_row = [i[0] for i in sorted_results]
    for j in first_index_row:
        print(j)


