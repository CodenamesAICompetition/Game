from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import numpy as np
import scipy.spatial.distance
import itertools
from typing import Tuple, List

from players.codemaster import *

class VectorCodemaster(Codemaster):
    """Generalized Vector Codemaster
    Concat any keyed vector that can be accessed like: word_vector_dict["<word>"] = nd.array
    """
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

        self.distance_threshold = kwargs.get("distance_threshold", 0.7)
        self.max_red_words_per_clue = kwargs.get("max_red_words_per_clue", 3)
        self.same_clue_patience = kwargs.get("sameCluePatience", 25)

        # print("patience:", self.sameCluePatience, "distancethresh",
        #       self.distanceThreshold, "maxRedWordsPerClue", self.maxRedWordsPerClue)

        self.same_clue_counter = 0
        self.last_clue = None
        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.lancaster_stemmer = LancasterStemmer()
        self.bad_word_distances = None
        self.red_word_distances = None
        self.words_on_board = None
        self.key_grid = None

        self.cm_word_set = set([])
        with open('players/cm_wordlist.txt') as infile:
            for line in infile:
                self.cm_word_set.add(line.rstrip().lower())

    def set_game_state(self, words_on_board: List[str], key_grid: List[str]) -> None:
        """A set function for wordOnBoard and keyGrid (called 'map' in framework) """
        self.words_on_board = words_on_board
        self.key_grid = key_grid

        red_words, bad_words = self._identify_words_on_board()
        self._calc_distance_between_words_on_board_and_clue(red_words, bad_words)
        self._remove_conflicting_clues(red_words, bad_words)

    def _calc_distance_between_words_on_board_and_clue(self, red_words: List[str], bad_words: List[str]) -> None:
        """Create word-distance dictionaries for both red words and bad words"""
        self.red_word_distances = {}
        for redWord in red_words:
            self.red_word_distances[redWord] = {}
            red_word_stacked = self._hstack_word_vectors(redWord)
            for potentialClue in self.cm_word_set | set(bad_words) | set(red_words):
                try:
                    dist = scipy.spatial.distance.cosine(red_word_stacked, self._hstack_word_vectors(potentialClue))
                except KeyError:
                    dist = np.inf
                self.red_word_distances[redWord][potentialClue] = dist

        self.bad_word_distances = {}
        for badWord in bad_words:
            self.bad_word_distances[badWord] = {}
            bad_word_stacked = self._hstack_word_vectors(badWord)
            for potentialClue in self.cm_word_set | set(bad_words) | set(red_words):
                try:
                    dist = scipy.spatial.distance.cosine(bad_word_stacked, self._hstack_word_vectors(potentialClue))
                except KeyError:
                    dist = np.inf
                self.bad_word_distances[badWord][potentialClue] = dist

    def _remove_conflicting_clues(self, red_words: List[str], bad_words: List[str]) -> None:
        """Remove and save clues that overlap with words on the board"""
        self.removed_clues = {}
        for word in bad_words + red_words:
            removed_clues_per_word = []
            lemm = self.wordnet_lemmatizer.lemmatize(word)
            lancas = self.lancaster_stemmer.stem(word)
            for clue in self.cm_word_set.copy():
                if word == clue or lemm == clue or lancas == clue \
                        or clue.find(word) != -1 or word.find(clue) != -1 \
                        or clue.find(lemm) != -1 or lemm.find(clue) != -1 \
                        or clue.find(lancas) != -1 or lancas.find(clue) != -1:

                    self.cm_word_set.discard(clue)
                    self.cm_word_set.discard(word)
                    self.cm_word_set.discard(lemm)
                    self.cm_word_set.discard(lancas)

                    removed_clues_per_word.append(clue)
                    removed_clues_per_word.append(word)
            self.removed_clues[word] = removed_clues_per_word

    def _identify_words_on_board(self) -> Tuple[List[str], List[str]]:
        red_words = []
        bad_words = []

        for i in range(len(self.key_grid)):
            # words on board that have already been identified will have been replaced with *<operatorName>*
            # so the first character is '*'
            if self.words_on_board[i][0] == '*':
                continue
            elif self.key_grid[i] == "Assassin" or self.key_grid[i] == "Blue" or self.key_grid[i] == "Civilian":
                bad_words.append(self.words_on_board[i].lower())
            else:
                red_words.append(self.words_on_board[i].lower())

        return red_words, bad_words

    def get_clue(self) -> Tuple[str, int]:
        """Function that returns a clue word and number of estimated related words on the board"""

        red_words, bad_words = self._identify_words_on_board()
        # print("REDWORDS:", redWords)

        to_remove = set(self.bad_word_distances) - set(bad_words)
        for word in to_remove:
            # del self.badWordDists[word]
            removed_clues_per_word = self.removed_clues.get(word, [])
            for clue in removed_clues_per_word:
                self.cm_word_set.add(clue)

        to_remove = set(self.red_word_distances) - set(red_words)
        for word in to_remove:
            # del self.redWordDists[word]
            removed_clues_per_word = self.removed_clues.get(word, [])
            for clue in removed_clues_per_word:
                self.cm_word_set.add(clue)

        bests = {}
        # iterate though combinations of red words for best clue
        # ignore clue with close distance to a bad word
        for n_red_words_in_clue in range(1, self.max_red_words_per_clue + 1):
            best_dist_per_clue_num = np.inf
            best_word_per_clue_num = ""
            best_red_word_per_clue_num = ""

            for red_word_combination in list(itertools.combinations(red_words, n_red_words_in_clue)):
                best_dist = np.inf
                best_word = ""

                for potential_clue in self.cm_word_set:

                    if potential_clue == self.last_clue and self.same_clue_counter >= self.same_clue_patience:
                        continue

                    min_bad_dist = np.inf
                    min_bad_word = ""
                    for bad_word in bad_words:
                        if self.bad_word_distances[bad_word][potential_clue] < min_bad_dist:
                            min_bad_dist = self.bad_word_distances[bad_word][potential_clue]
                            min_bad_word = bad_word

                    max_red_dist = 0
                    for red_word in red_word_combination:
                        dist = self.red_word_distances[red_word][potential_clue]
                        if dist > max_red_dist:
                            max_red_dist = dist

                    if max_red_dist < best_dist and max_red_dist < min_bad_dist:
                        best_dist = max_red_dist
                        best_word = potential_clue

                        if best_dist < best_dist_per_clue_num:
                            best_dist_per_clue_num = best_dist
                            best_word_per_clue_num = best_word
                            best_red_word_per_clue_num = red_word_combination

            bests[n_red_words_in_clue] = (best_red_word_per_clue_num, best_word_per_clue_num, best_dist_per_clue_num)

        # print("bests:", bests)

        chosen_clue = bests[1][1]
        chosen_num = 1

        for clue_num, (redWordCombo, potential_clue, score) in bests.items():
            if score == np.inf:
                continue

            worst = -np.inf
            best = np.inf

            for word in redWordCombo:
                dist = self.red_word_distances[word][potential_clue]
                if dist > worst:
                    worst = dist
                if dist < best:
                    best = dist

            # pick up the highest combination size
            # where the worst distance between clue and redWord is below distanceThreshold
            if worst < self.distance_threshold and worst != -np.inf:
                chosen_clue = potential_clue
                chosen_num = clue_num

        # track how many times in a row the same clue is chosen
        if chosen_clue == self.last_clue:
            self.same_clue_counter += 1
        else:
            self.same_clue_counter = 1
        self.last_clue = chosen_clue
        return chosen_clue, chosen_num

    def _hstack_word_vectors(self, word):
        """For word, stack all word embedding nd.array for each kind of word vector"""
        try:
            stacked_words = self.all_vectors[0][word]
            for vec in self.all_vectors[1:]:
                stacked_words = np.hstack((stacked_words, vec[word]))
            return stacked_words
        except KeyError:
            return None

