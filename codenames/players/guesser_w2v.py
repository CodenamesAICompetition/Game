from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import wordnet_ic
from operator import itemgetter
from players.guesser import guesser
from collections import Counter
import gensim.models.keyedvectors as word2vec
import gensim.downloader as api
import itertools
import numpy as np
import random
import scipy


class ai_guesser(guesser):

	def __init__(self, brown_ic=None, glove_vecs=None, word_vectors=None):
		self.brown_ic = brown_ic
		self.glove_vecs = glove_vecs
		self.word_vectors = word_vectors
		self.num = 0
		
	def get_board(self, words):
		self.words = words
		return words

	def get_clue(self, clue, num):
		self.clue = clue
		self.num = num
		print("The clue is:", clue, num, sep=" ")
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
		# preset weights based on testing for optimal voting algorithm
		# weights[0] = w2v initial weight, weights[1] = glove initial weight
		# w2v holds a higher initial value due to its accuracy.
		weights = [13, 12]
		sorted_words = self.compute_distance(self.clue, self.words)
		print(f'guesses: {sorted_words}')
		self.num -= 1
		return sorted_words[0][1]

