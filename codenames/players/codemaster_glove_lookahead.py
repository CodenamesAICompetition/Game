import scipy.spatial.distance
from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import copy
import itertools

from players.codemaster import Codemaster


class AICodemaster(Codemaster):

    def __init__(self, brown_ic=None, glove_vecs=None, word_vectors=None):
        super().__init__()
        self.brown_ic = brown_ic
        self.glove_vecs = glove_vecs
        self.word_vectors = word_vectors
        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.lancaster_stemmer = LancasterStemmer()
        self.cm_wordlist = []
        with open('players/cm_wordlist.txt') as infile:
            for line in infile:
                self.cm_wordlist.append(line.rstrip())
        self.root = None

    def set_game_state(self, words, maps):
        self.words = words
        self.maps = maps
        self.red_words = []
        self.bad_words = []
        for i in range(25):
            if self.words[i][0] == '*':
                continue
            elif self.maps[i] == "Assassin" or self.maps[i] == "Blue" or self.maps[i] == "Civilian":
                self.bad_words.append(self.words[i].lower())
                if self.maps[i] == "Assassin":
                    self.black_guessed = False
            else:
                self.red_words.append(self.words[i].lower())


        cos_dist = scipy.spatial.distance.cosine
        all_vectors = (self.glove_vecs,)
        self.bad_word_dists = {}
        for word in self.bad_words:
            self.bad_word_dists[word] = {}
            for val in self.cm_wordlist:
                b_dist = cos_dist(self.concatenate(val, all_vectors), self.concatenate(word, all_vectors))
                self.bad_word_dists[word][val] = b_dist

        self.red_word_dists = {}
        for word in self.red_words:
            self.red_word_dists[word] = {}
            for val in self.cm_wordlist:
                b_dist = cos_dist(self.concatenate(val, all_vectors), self.concatenate(word, all_vectors))
                self.red_word_dists[word][val] = b_dist

    def get_clue(self):
        if self.root is None or self.root.words != self.words:
            if self.root:
                print("board mismatch: initializing new root")
            self.root = Node(self, self.words, self.maps, None, depth = 0)
        self.root.get_val(depth=3)
        best_clue = self.root.best_clue
        print("BESTS: ", self.root.children.keys())
        print('chosen_clue is:', best_clue[0])

        self.root = self.root.best_child()
        
        return best_clue

    def arr_not_in_word(self, word, arr):
        if word in arr:
            return False
        lemm = self.wordnet_lemmatizer.lemmatize(word)
        lancas = self.lancaster_stemmer.stem(word)
        for i in arr:
            if i == lemm or i == lancas:
                return False
            if i.find(word) != -1:
                return False
            if word.find(i) != -1:
                return False
        return True

    def combine(self, words, wordvecs):
        factor = 1.0 / float(len(words))
        new_word = self.concatenate(words[0], wordvecs) * factor
        for word in words[1:]:
            new_word += self.concatenate(word, wordvecs) * factor
        return new_word

    def concatenate(self, word, wordvecs):
        concatenated = wordvecs[0][word]
        for vec in wordvecs[1:]:
            concatenated = np.hstack((concatenated, vec[word]))
        return concatenated


class Node:
    def __init__(self, codemaster, words, maps, parent, depth = 0):
        self.codemaster = codemaster
        self.words = words
        self.maps = maps
        self.parent = parent
        self.depth = depth
        self.best_clue = None
        self.children = {}
        self.val = None
        self.terminal = False

    def get_best_clues(self):
        bests = {}
        possible = {}
        cm = self.codemaster
        print(f"calculating best clues")
        #print(f"red word dists: {self.red_word_dists}")
        for clue_num in range(1, 3 + 1):
            best_per_dist = np.inf
            best_per = ''
            best_red_word = ''
            for red_word in list(itertools.combinations(self.red_words, clue_num)):
                best_word = ''
                best_dist = np.inf
                for word in cm.cm_wordlist:
                    if not cm.arr_not_in_word(word, self.red_words + self.bad_words):
                        continue

                    bad_dist = np.inf
                    worst_bad = ''
                    for bad_word in self.bad_words:
                        if cm.bad_word_dists[bad_word][word] < bad_dist:
                            bad_dist = cm.bad_word_dists[bad_word][word]
                            worst_bad = bad_word
                    worst_red = 0
                    for red in red_word:
                        dist = cm.red_word_dists[red][word]
                        if dist > worst_red:
                            worst_red = dist

                    if worst_red < best_dist and worst_red < bad_dist:
                        best_dist = worst_red
                        best_word = word
                        # print(worst_red,red_word,word)

                        if best_dist < best_per_dist:
                            best_per_dist = best_dist
                            best_per = best_word
                            best_red_word = red_word
                if best_dist < np.inf:            
                    possible[(best_word, clue_num)] = (red_word, best_per_dist)
            bests[clue_num] = (best_red_word, best_per, best_per_dist)
        print(f"length of possibilities: {len(possible)}")
        return possible

    def add_children(self):
        cos_dist = scipy.spatial.distance.cosine
        cm = self.codemaster
        all_vectors = (cm.glove_vecs,)
        print(f"at depth {self.depth}")
        bests = self.get_best_clues()
        for clue, clue_info in bests.items():
            combined_clue, clue_num = clue
            best_red_word, combined_score = clue_info
            worst = -np.inf
            for word in best_red_word:
                dist = cos_dist(cm.concatenate(word, all_vectors), cm.concatenate(combined_clue, all_vectors))
                if dist > worst:
                    worst = dist
            if worst < 0.7 and worst != -np.inf or clue_num == 1:
                print(f"adding clue: {clue}")
                self.add_child(clue, best_red_word)
        
    def check_board(self):
        cm = self.codemaster
        self.red_words = []
        self.bad_words = []
        self.black_guessed = True
        cos_dist = scipy.spatial.distance.cosine

        # Creates Red-Labeled Word arrays, and everything else arrays
        for i in range(25):
            if self.words[i][0] == '*':
                continue
            elif self.maps[i] == "Assassin" or self.maps[i] == "Blue" or self.maps[i] == "Civilian":
                self.bad_words.append(self.words[i].lower())
                if self.maps[i] == "Assassin":
                    self.black_guessed = False
            else:
                self.red_words.append(self.words[i].lower())


        red_count = len(self.red_words)
        if self.black_guessed:
            self.val = -1
            self.terminal = True
        elif red_count == 0:
            self.val = 26 - self.depth
            self.terminal = True
        else:
            self.val = 1 - red_count/8.0
     
    def add_child(self, clue, expected_words_chosen):
        new_words = copy.copy(self.words)
        new_maps = copy.copy(self.maps)
        for word in expected_words_chosen:
            idx = self.words.index(word.upper())
            new_words[idx] = f"*{self.maps[idx]}*"
            new_maps[idx] = f"*{self.maps[idx]}*"
        child_node = Node(self.codemaster, new_words, new_maps, self, self.depth + 1)
        self.children[clue] = child_node
        
    def get_val(self, depth=np.inf):
        self.check_board()
        if self.terminal:
            return self.val
        else:
            if self.depth < depth and len(self.children) == 0:
                self.add_children()
            if len(self.children) > 0:
                best_val = -np.inf
                for (clue, child) in self.children.items():
                    child_val = child.get_val(depth)
                    print(f"clue: {clue} val: {child_val}")
                    if child_val >= best_val:
                        best_val = child_val
                        self.best_clue = clue
                self.val = best_val
            return self.val

    def best_child(self):
        best_clue = self.best_clue
        for child_key in self.children.keys():
            if child_key == best_clue:
                best_child = self.children[child_key]
        best_child.reset_depth()
        return best_child
        
    def reset_depth(self, depth = 0):
        self.depth = depth
        for child in self.children.values():
            child.reset_depth(depth+1)


        
