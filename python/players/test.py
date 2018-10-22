import numpy as np
import gensim.models.keyedvectors as word2vec
import itertools
from allennlp.commands.elmo import ElmoEmbedder
import scipy

def test_glove():

    words = {}

    # download from here, --> https://nlp.stanford.edu/data/glove.6B.zip
    # and move to this directory (~/Desktop/Game/python/players/glove)
    with open('glove/glove.6B.50d.txt') as infile:
        for line in infile:
            line = line.rstrip().split(' ')
            words[line[0]] = np.array([float(n) for n in line[1:]])

    word1 = 'cat'
    word2 = 'potato'
    god = np.dot(words[word1]/np.linalg.norm(words[word1]),words[word2]/np.linalg.norm(words[word2]))

    print(word1, word2, god)

    word2 = 'tiger'
    god = np.dot(words[word1]/np.linalg.norm(words[word1]),words[word2]/np.linalg.norm(words[word2]))

    print(word1, word2, god)

    word2 = 'dog'
    god = np.dot(words[word1]/np.linalg.norm(words[word1]),words[word2]/np.linalg.norm(words[word2]))

    print(word1, word2, god)

    word1 = 'chronological'
    word2 = 'history'
    god = np.dot(words[word1]/np.linalg.norm(words[word1]),words[word2]/np.linalg.norm(words[word2]))

    print(word1, word2, god)

    word1 = 'basketball'
    word2 = 'orange'
    god = np.dot(words[word1]/np.linalg.norm(words[word1]),words[word2]/np.linalg.norm(words[word2]))

    print(word1, word2, god)


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


def test_elmo():

    elmo = ElmoEmbedder()
    tokens = ["I", "ate", "an", "apple", "for", "breakfast"]

    vectors = elmo.embed_sentence(tokens)
    vectors2 = elmo.embed_sentence(["I", "ate", "a", "carrot", "for", "breakfast"])


    # cosine distance between "ate" and "carrot" in the last layer
    x = scipy.spatial.distance.cosine(vectors[2][3], vectors2[2][3])

    print(x)



test_elmo()

