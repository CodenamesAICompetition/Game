import scipy.spatial.distance

from players.guesser import Guesser


class AIGuesser(Guesser):

    def __init__(self, brown_ic=None, glove_vecs=None, word_vectors=None):
        self.brown_ic = brown_ic
        self.glove_vecs = glove_vecs
        self.word_vectors = word_vectors
        self.num = 0

    def get_board(self, words):
        self.words = words

    def get_clue(self, clue, num):
        self.clue = clue
        self.num = num
        print("The clue is:", clue, num)
        li = [clue, num]
        return li

    def compute_distance(self, clue, board):
        w2v = []
        glove = []
        linalg_result = []

        for word in board:
            try:
                if word[0] == '*':
                    continue
                w2v.append((scipy.spatial.distance.cosine(self.word_vectors[clue],
                                                          self.word_vectors[word.lower()]), word))
            except KeyError:
                continue

        w2v = list(sorted(w2v))
        return w2v

    def keep_guessing(self, clue, board):
        return self.num > 0

    def give_answer(self):
        sorted_words = self.compute_distance(self.clue, self.words)
        print(f'guesses: {sorted_words}')
        self.num -= 1
        return sorted_words[0][1]
