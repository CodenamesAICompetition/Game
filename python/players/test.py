from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import wordnet_ic
from operator import itemgetter
from allennlp.commands.elmo import ElmoEmbedder
import gensim.models.keyedvectors as word2vec
import gensim.downloader as api
import itertools
import numpy as np
import random
import scipy


def test_glove():
    board = ["COFFEE", "POTATO", "CHICKEN", "CARROT", "LIGHT", 
    "DARK", "GRIND", "KING", "PIN", "DEVIL", 
    "ICE", "DOG", "ALADIN", "WOLF", "SWITCH", 
    "TOGGLE", "GALAXY", "WIND", "SEASON", "FALL", 
    "RAIN", "TOMATO", "FIRE", "FLY", "WINTER"]

    clue = "FOOD"
    words = {}
    result = []
    i = 1

    # download from here, --> https://nlp.stanford.edu/data/glove.6B.zip
    # and move to this directory (~/Desktop/Game/python/players/glove)
    with open('glove/glove.6B.50d.txt') as infile:
        for line in infile:
            i += 1
            line = line.rstrip().split(' ')
            words[line[0]] = np.array([float(n) for n in line[1:]])

    for i in range(25):
        linalg = np.dot(words[board[i].lower()] / np.linalg.norm(words[board[i].lower()]),
            words[clue.lower()] / np.linalg.norm(words[clue.lower()]))
        result.append([board[i], clue, linalg])

    result = list(reversed(sorted(result, key=take_third)))
    print(result)
    # return result[:5]


def take_third(elem):
    return elem[2]


def test_google_w2v():
    # download from here ---->  https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
    # and move to this directory (~/Desktop/game/python/players)
    word_vectors = word2vec.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
    good = ['berry','calf','turkey','heart','switch','fork','bug','ice']
    bad = []

    for combo in list(itertools.combinations(good,2)):
        best = word_vectors.most_similar_cosmul(list(combo),bad)
        best = [t for t in best if '_' not in t[0]]
        best = [t for t in best if not t[0][0].isupper()]
        best = [t for t in best if combo[0] not in t[0].lower() and combo[1] not in t[0].lower()]

        print(combo,'\n','\n\t'.join([str(t) for t in  best if t[1] > 0.5]))

    result = word_vectors.most_similar(positive=['woman', 'king'], negative=['man'])
    print("{}: {:.4f}".format(*result[0]))

    similarity = word_vectors.similarity('woman', 'man')
    print(similarity)


# params --> self, clue, board
def test_elmo():
    board = ["China", "Potato", "Tomato", "Eggplant", "Nasa", "Kingdom"]
    clue = "Wall"

    hot = wordnet.synsets('hot')
    tokenized = [tokens.split(' ') for tokens in hot[8].examples()]
    print(tokenized)

    vectors = ElmoEmbedder().embed_sentence(["I", "ate", "an", "apple", "for", "breakfast"])
    vectors2 = ElmoEmbedder().embed_sentence(["I", "ate", "a", "carrot", "for", "breakfast"])
    vectors3 = ElmoEmbedder().embed_sentence(["I", "ate", "a", "airplane", "for", "breakfast"])
    carrot = ElmoEmbedder().embed_sentence(['carrot'])
    apple = ElmoEmbedder().embed_sentence(['apple'])

    hot_temp = ElmoEmbedder().embed_sentence(["It", "was", "a", "hot", "oven"])
    hot_spicy = ElmoEmbedder().embed_sentence(["I", "ate", "a", "hot", "pepper"])
    spicy = ElmoEmbedder().embed_sentence(['jalapeno', 'peppers', 'are', 'very', 'hot'])
    spicy2 = ElmoEmbedder().embed_sentence(['hot','salsa'])
    
    print('hot to spicy', scipy.spatial.distance.cosine(spicy2[2][0], spicy[2][4]))
    print('hot to hot', scipy.spatial.distance.cosine(hot_spicy[2][3], hot_temp[2][3]))

    board_vector = ElmoEmbedder().embed_sentence(board)
    vec_clue = ElmoEmbedder().embed_sentence(clue)

    for i in range(len(board)):
        print(scipy.spatial.distance.cosine(board_vector[2][i], vec_clue[2][0]))


def salmon():
    w2v = [(0.3589853048324585, 'APPLE'), (0.8013214617967606, 'FLY'), 
    (0.8053699284791946, 'GRASS'), (0.8500983864068985, 'FLUTE')]
    glove = [(0.40823636894816195, 'APPLE'), (0.48846032017027585, 'GRASS'), 
    (0.5819027688959142, 'MOUSE'), (0.6007173192984769, 'DAY')]
    result = w2v[:4] + glove[:4]
    print(result)


def potato():
    for synset in wordnet.synsets('dog'):
        print(synset)
        for lemma in synset.lemmas():
            print(lemma.name())


def loop():
    result = [[('worms', 0.71803), ('Conficker_aka_Downadup', 0.675), ('idiot_savant', 0.53)]]
    li = result.pop(0)
    print(li)

    for i in li:
        print(i[0])
        index = li.index(i)
        print(index)

        if i[0] is "idiot_savant":
            li.pop(index)

    print(li)


# def do_imp(name):
#     name = "package." + name
#     mod = import(name, fromlist=[''])
#     mod.do_imp()

#     # python3 game.py   human  someone_elses_codemaster
#     # import('package.someone_elses_codemaster')
#     # codemaster_bot = import('package.someone_elses_codemaster')()

#     wordlist = set(load(cm_wordlist.txt))
#     clues = w2v.most_similar(positive, negative)
#     for clue in clues:
#     if clue in wordlist:
#           good_clues.append(clue)

#     get_guess()


# def keep_guessing():
#     if bot.keep_guessing():
#         answer = bot.give_answer()
#     return True


loop()


