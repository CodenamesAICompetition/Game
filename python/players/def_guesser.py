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

	def get_board(self, words):
		self.words = words
		return words

	def get_clue(self, clue, num):
		self.clue = clue
		print("The clue is:", clue, num, sep=" ")
		li = [clue, num]
		return li

	def compute_googlove(self, clue, board):
		w2v = []
		glove = []
		linalg_result = []

		for word in board:
			try:
				if word[0] == '*':
					continue
				w2v.append((scipy.spatial.distance.cosine(self.word_vectors[clue],
					self.word_vectors[word.lower()]), word))
				glove.append((scipy.spatial.distance.cosine(self.glove_vecs[clue],
					self.glove_vecs[word.lower()]), word))
			except KeyError:
				continue

		print("w2v ", sorted(w2v)[:1])
		print("glove ", sorted(glove)[:1])

		w2v = list(sorted(w2v))
		glove = list(sorted(glove))
		result = w2v[:3] + glove[:3]
		return result
		
	def keep_guessing(self, clue, board):
		return True

	def give_answer(self):
		# preset weights based on testing for optimal voting algorithm
		# weights[0] = w2v initial weight, weights[1] = glove initial weight
		# w2v holds a higher initial value due to its accuracy.
		weights = [14, 12]
		google_glove = self.compute_googlove(self.clue, self.words)

		# w2v threshold + added weights
		if google_glove[0][0] < 0.8:
			if google_glove[0][0] < 0.7:
				if google_glove[0][0] < 0.51:
					weights[0] += 20
				weights[0] += 10
			weights[0] += 3
		# glove threshold + added weights
		if google_glove[3][0] < 0.66:
			if google_glove[3][0] < 0.51:
				if google_glove[3][0] < 0.36:
					weights[1] += 20
				weights[1] += 10
			weights[1] += 4

		max_weight = max(weights)
		y = ([i for i, j in enumerate(weights) if j == max_weight])
		x = int(y[0]) + 1
		# if w2v won the voting alg (x == 0) choose the word w2v, else choose glove's word.
		string_answer_input = google_glove[0][1] if x == 1 else google_glove[3][1]
		print("Threshold chose word: ", string_answer_input, " from: ", x)
		return string_answer_input

