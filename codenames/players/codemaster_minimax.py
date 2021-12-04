from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import numpy as np
import scipy.spatial.distance
import itertools
import heapq
from typing import Tuple, List

from players.codemaster import *

class MiniMaxCodemaster(Codemaster):
    def __init__(self, **kwargs):
        """Set up word list and handle pretrained vectors"""
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

        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.lancaster_stemmer = LancasterStemmer()
        self.word_distances = None
        self.words_on_board = None
        self.key_grid = None
        self.good_color = "Red"
        self.bad_color = "Blue"
        self.max_clue_num = 1

        # Potential codemaster clues
        self.cm_word_set = set([])
        with open('players/cm_wordlist.txt') as infile:
            for line in infile:
                self.cm_word_set.add(line.rstrip().lower())

    def set_game_state(self, words_on_board: List[str], key_grid: List[str]) -> None:
        """A set function for wordOnBoard and keyGrid (called 'map' in framework) """
        self.words_on_board = words_on_board.copy()
        self.key_grid = key_grid

        # intialize word distances on first call
        if self.word_distances is None:
            self._calc_distance_between_words_on_board_and_clue()

    def _calc_distance_between_words_on_board_and_clue(self) -> None:
        """Create word-distance dictionaries for both red words and bad words"""
        self.word_distances = {}
        for word in self.words_on_board:
            print("Calculating distance for " + word)
            self.word_distances[word] = {}
            word_stacked = self._hstack_word_vectors(word.lower())
            for potentialClue in self.cm_word_set:
                try:
                    dist = scipy.spatial.distance.cosine(word_stacked, self._hstack_word_vectors(potentialClue))
                except TypeError:
                    dist = np.inf
                self.word_distances[word][potentialClue] = dist

    def get_clue(self) -> Tuple[str, int]:
        """Function that returns a clue word and number of estimated related words on the board"""
        clue, num = self._min_max(max, 1, self.words_on_board, self.key_grid)
        print("The " + self.good_color + " clue is " + clue)
        print("Old board + Expected new board")
        print(self.words_on_board)
        new_board = self._simulate_guesses(self.good_color, clue, num, self.words_on_board, self.key_grid)
        print(new_board)
        return (clue, num)

    def _min_max(self, function, depth, words_on_board, key_grid) -> Tuple[str, int]:
        # TODO prune word set for illegal clues
        clueOutcomes = {}
        for potentialClue in self.cm_word_set:
            for clueNum in range(1, self.max_clue_num + 1):
                new_words_on_board = self._simulate_guesses(self.good_color, potentialClue, clueNum, words_on_board, key_grid)
                # TODO minimize
                value = self._heuristicFunction(self.good_color, new_words_on_board, key_grid)
                clueOutcomes[(potentialClue, clueNum)] = value

        return function(clueOutcomes, key=clueOutcomes.get)

    def _simulate_guesses(self, guesser_color, clue, num, words_on_board, key_grid):

        # use heapq for priority queue
        best_words = []
        new_words_on_board = words_on_board.copy()

        # find and sort best words
        for word_index in range(len(words_on_board)):
            word = new_words_on_board[word_index]
            if word[0] == '*':
                continue
            word_distance = self.word_distances[word][clue]
            heapq.heappush(best_words, (word_distance, word_index))

        # try best words
        for i in range(num):
            _, word_index = heapq.heappop(best_words)
            word_color = key_grid[word_index]
            new_words_on_board[word_index] = "*" + word_color + "*"
            if key_grid[word_index] != guesser_color:
                break

        return new_words_on_board

    def _heuristicFunction(self, last_player_color, words_on_board, key_grid):
        good_remaining = 0
        bad_remaining = 0
        neutral_remaining = 0
        assasin_remaining = 0

        for i in range(len(self.key_grid)):
            # words on board that have already been identified will have been replaced with *<operatorName>*
            # so the first character is '*'
            if words_on_board[i][0] == '*':
                continue
            elif key_grid[i] == self.good_color:
                good_remaining += 1
            elif key_grid[i] == self.bad_color:
                bad_remaining += 1
            elif key_grid[i] == "Civilian":
                neutral_remaining += 1
            elif key_grid[i] == "Assassin":
                assasin_remaining += 1
            else:
                # TODO should never get here, throw error
                pass

        if good_remaining == 0:
            return 10

        if bad_remaining == 0:
            return -10

        if assasin_remaining == 0 and last_player_color == self.good_color:
            return -10
        elif assasin_remaining == 0 and last_player_color == self.bad_color:
            return 10

        return bad_remaining - good_remaining


    def _hstack_word_vectors(self, word):
        """For word, stack all word embedding nd.array for each kind of word vector"""
        try:
            stacked_words = self.all_vectors[0][word]
            for vec in self.all_vectors[1:]:
                stacked_words = np.hstack((stacked_words, vec[word]))
            return stacked_words
        except KeyError:
            return None