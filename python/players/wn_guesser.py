from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import wordnet_ic
from operator import itemgetter
from players.guesser import guesser
from collections import Counter
from allennlp.commands.elmo import ElmoEmbedder
import gensim.models.keyedvectors as word2vec
import itertools
import numpy as np
import random
import scipy

class wn_guesser(guesser):

    def __init__(self):

        self.brown_ic = wordnet_ic.ic('ic-brown.dat')
        print("IC corpus successfully imported")
        self.word_vectors = word2vec.KeyedVectors.load_word2vec_format(
            'players/GoogleNews-vectors-negative300.bin', binary=True)
        print("Glove successfully imported")

        self.glove_vecs = {}
        with open('players/glove/glove.6B.50d.txt') as infile:
            for line in infile:
                line = line.rstrip().split(' ')
                self.glove_vecs[line[0]] = np.array([float(n) for n in line[1:]])
        # self.elmo = ElmoEmbedder()
        

    def get_board(self, words):

        self.words = words
        return words


    def get_clue(self, clue, num):

        self.clue = clue
        print("The clue is:", clue, num, sep=" ")

        li = [clue, num]
        return li


    def wordnet_synset(self, clue, board):

        wup_results = []
        res_results = []
        count = 0

        for i in (board):
            for clue_list in wordnet.synsets(clue):
                wup_clue = res_clue = 0
                for board_list in wordnet.synsets(i):
                    try:
                        # only if the two compared words have the same part of speech
                        wup = clue_list.wup_similarity(board_list)
                        res = clue_list.res_similarity(board_list, self.brown_ic)
                    except:
                        continue
                    # if lch is non-zero so are the other 3 algorithms (same part of speech was compared)
                    if res:
                        res_results.append(("res: ", res, count, clue_list, board_list, i))
                        count += 1

                        if res > res_clue:
                            res_clue = res

                    # wup always compares regardless of Part of Speech to an extent
                    if wup:
                        wup_results.append(("wup: ", wup, count, clue_list, board_list, i))
                        count += 1

                        if wup > wup_clue:
                            wup_clue = wup 

                print("wup: ", i, wup_clue)
                print("res: ", i, res_clue)
                print('-'*30)

        # if results list is empty
        if not res_results:
            return []

        wup_results = list(reversed(sorted(wup_results, key=self.take_second)))
        res_results = list(reversed(sorted(res_results, key=self.take_second)))

        results = [wup_results, res_results]
        return results


    def take_second(self, elem):
        return elem[1]

    def take_third(self, elem):
        return elem[2]


    # def go_elmo(self, clue, board):

    #     hot = wordnet.synsets('hot')
    #     tokenized = [tokens.split(' ') for tokens in hot[8].examples()]
    #     print(tokenized)

    #     vec_clue = self.elmo.embed_sentence([clue])

    #     return results


    def compute_GooGlove(self, clue, board):
    

        w2v = []
        glove = []
        linalg_result = []

        for word in board:
            try:
                if word[0] == '*':
                    continue

                # for i in range(25):

                #     linalg = np.dot(words[board[i].lower()] / np.linalg.norm(words[board[i].lower()]),
                #         words[clue.lower()] / np.linalg.norm(words[clue.lower()]))
                #     linalg_result.append([board[i], clue, linalg])

                w2v.append((scipy.spatial.distance.cosine(self.word_vectors[clue], 
                    self.word_vectors[word.lower()]),word))
                glove.append((scipy.spatial.distance.cosine(self.glove_vecs[clue],
                    self.glove_vecs[word.lower()]),word))

            except KeyError:
                continue

        print("w2v ", sorted(w2v)[:3])
        print("glove ", sorted(glove)[:3])

        w2v = list(sorted(w2v))
        glove = list(sorted(glove))
        # linalg_result = list(reversed(sorted(linalg_result, key=self.take_third)))

        result = w2v[:3] + glove[:3] # + linalg_result[:4]
        return result


    def give_answer(self):

        sorted_results = self.wordnet_synset(self.clue, self.words)
        print('-' * 20)
        google_glove = self.compute_GooGlove(self.clue, self.words)
        print(google_glove)

        if(sorted_results):

            first_index_row = [i[0] for i in sorted_results]
            for i in first_index_row:
                print(i)

            answer_input = (google_glove[0][1])
            #most_common_word.append(google_glove[6][0][0])

            # most_list = []
            # for i, count in Counter(most_common_word).most_common():
            #     if count != Counter(most_common_word).most_common(2)[0][1]:
            #         break
            #     most_list.append(i)

            # answer_input = random.choice(most_list)

        # result list was empty
        else:
            answer_input = "no comparisons"

        print(answer_input)
        return answer_input


