import random
from operator import itemgetter

from nltk.corpus import wordnet

from codenames.players.guesser import Guesser


class AIGuesser(Guesser):

    def __init__(self, brown_ic=None, glove_vecs=None, word_vectors=None):
        super().__init__()
        self.brown_ic = brown_ic
        self.glove_vecs = glove_vecs
        self.word_vectors = word_vectors
        self.num = 0

    def set_board(self, words):
        self.words = words

    def set_clue(self, clue, num):
        self.clue = clue
        self.num = num
        print("The clue is:", clue, num)
        li = [clue, num]
        return li

    def keep_guessing(self):
        return self.num > 0

    def get_answer(self):
        sorted_results = self._wordnet_synset(self.clue, self.words)
        if not sorted_results:
            choice = "*"
            while choice[0] is '*':
                choice = random.choice(self.words)
            return choice
        print(f'guesses: {sorted_results}')
        self.num -= 1
        return sorted_results[0][5]

    def _wordnet_synset(self, clue, board):
        res_results = []
        count = 0
        for i in board:
            for clue_list in wordnet.synsets(clue):
                res_clue = 0
                for board_list in wordnet.synsets(i):
                    try:
                        # only if the two compared words have the same part of speech
                        res = clue_list.res_similarity(board_list, self.brown_ic)
                    except :
                        continue
                    if res:
                        res_results.append(("res: ", res, count, clue_list, board_list, i))
                        if res > res_clue:
                            res_clue = res

        # if results list is empty
        if not res_results:
            return []

        res_results = list(reversed(sorted(res_results, key=itemgetter(1))))
        return res_results[:3]
