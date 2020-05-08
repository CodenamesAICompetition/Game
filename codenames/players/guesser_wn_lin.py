import random
from operator import itemgetter

from nltk.corpus import wordnet

from players.guesser import Guesser


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
        lin_results = []
        count = 0
        for i in board:
            for clue_list in wordnet.synsets(clue):
                lin_clue = 0
                for board_list in wordnet.synsets(i):
                    try:
                        # only if the two compared words have the same part of speech
                        lin = clue_list.lin_similarity(board_list, self.brown_ic)
                    except KeyError:
                        continue
                    if lin:
                        lin_results.append(("lin: ", lin, count, clue_list, board_list, i))
                        if lin > lin_clue:
                            lin_clue = lin

        # if results list is empty
        if not lin_results:
            return []

        lin_results = list(reversed(sorted(lin_results, key=itemgetter(1))))
        return lin_results[:3]
