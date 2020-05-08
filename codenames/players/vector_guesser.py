import numpy as np
import scipy.spatial.distance
from typing import Tuple, List

from players.guesser import *

class VectorGuesser(Guesser):
    """Generalized Vector Guesser
    Concat any keyed vector that can be accessed like: word_vector_dict["<word>"] = nd.array
    """
    def __init__(self, **kwargs):
        """Handle pretrained vectors and declare instance vars"""
        super().__init__()

        glove_vecs = kwargs.get("glove_vecs", None)
        word_vectors = kwargs.get("word_vectors", None)

        self.all_vectors = []
        if glove_vecs is not None:
            self.all_vectors.append(glove_vecs)
        if word_vectors is not None:
            self.all_vectors.append(word_vectors)
        if "vectors" in kwargs:
            for vecs in kwargs["vectors"]:
                self.all_vectors.append(vecs)

        self.init_num_guesses = None
        self.num_guesses_left = None
        self.clue_word = None
        self.words_on_board = None

        self.predicted_guesses = None

    def set_board(self, words_on_board: List[str]) -> None:
        """Set function for the current game board"""
        self.words_on_board = words_on_board

    def set_clue(self, clue: str, init_num_guesses: int) -> None:
        """Set function for current clue and number of guesses this class should attempt"""
        self.clue_word = clue
        self.init_num_guesses = init_num_guesses
        self.num_guesses_left = init_num_guesses
        # print("Guesser:", "clue =",self.clueWord, ", numGuesses =",self.numGuesses)
        self.predicted_guesses = None

    def keep_guessing(self) -> bool:
        """Return True if guess attempts remaining otherwise False"""
        return self.num_guesses_left > 0

    def get_answer(self) -> str:
        """Return the top guessed word based on the clue and current game board"""
        # calculate the top guesses only once
        if self.predicted_guesses is None:
            guesses = self._calc_dist_between_clues_and_board()
            # for cos-dist, min/reverse=False ; for cos-similarity, max/reverse=True
            guesses = sorted(guesses, key=lambda x: x[1], reverse=False)
            self.predicted_guesses = guesses

        # print("Guesser:", self.guesses)

        # return the top guess based on how many guesses have already been made
        top_word = self.predicted_guesses[int(self.init_num_guesses - self.num_guesses_left)][0]
        #print("Guesser:", "trying", top_word)

        self.num_guesses_left -= 1
        return top_word

    def _calc_dist_between_clues_and_board(self) -> List[Tuple[str, float]]:
        """Calc cosine similarity between clue word and words on the board"""
        word_distance_tuples = []
        cos_dist = scipy.spatial.distance.cosine
        for word in self.words_on_board:
            try:
                if word[0] == '*':
                    continue
                else:
                    distance = cos_dist(self._hstack_word_vectors(self.clue_word),
                                        self._hstack_word_vectors(word.lower()))  # 1 - cos_dist = cos similarity
                    word_distance_tuples.append((word, distance))
            except KeyError:
                continue

        return word_distance_tuples

    def _hstack_word_vectors(self, word):
        """For word, stack all word embedding nd.array for each kind of word vector"""
        try:
            stacked_words = self.all_vectors[0][word]
            for vec in self.all_vectors[1:]:
                stacked_words = np.hstack((stacked_words, vec[word]))
            return stacked_words
        except KeyError:
            return None
