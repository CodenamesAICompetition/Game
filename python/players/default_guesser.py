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
import timeit


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


	def wordnet_synset(self, clue, board):
		pat_results = []
		jcn_results = []
		lin_results = []
		count = 0

		for i in (board):
			for clue_list in wordnet.synsets(clue):
				pat_clue = jcn_clue = lin_clue = 0
				for board_list in wordnet.synsets(i):
					try:
						# only if the two compared words have the same part of speech
						pat = clue_list.path_similarity(board_list)
						jcn = clue_list.jcn_similarity(
							board_list, self.brown_ic)
						lin = clue_list.lin_similarity(
							board_list, self.brown_ic)
					except:
						continue

					if jcn:
						jcn_results.append(
							("jcn: ", jcn, count, clue_list, board_list, i))
						lin_results.append(
							("lin: ", lin, count, clue_list, board_list, i))
						if jcn > jcn_clue:
							jcn_clue = jcn

					if pat:
						pat_results.append(
							("pat: ", pat, count, clue_list, board_list, i))
						if pat > pat_clue:
							pat_clue = pat

		# if results list is empty
		if not jcn_results:
			return []

		pat_results = list(reversed(sorted(pat_results, key=itemgetter(1))))
		lin_results = list(reversed(sorted(lin_results, key=itemgetter(1))))
		jcn_results = list(reversed(sorted(jcn_results, key=itemgetter(1))))

		results = [pat_results[:3], jcn_results[:3], lin_results[:3]]
		return results


	def compute_GooGlove(self, clue, board):
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


	def give_answer(self):
		# set weights based on testing for optimal voting algorithm
		# order is w2v, glove, path_sim, jcn_sim, lin_sim. w2v has more initial weights due to its accuracy.
		weights = [15, 12, 8, 8, 8]
		sorted_results = self.wordnet_synset(self.clue, self.words)
		google_glove = self.compute_GooGlove(self.clue, self.words)

		if google_glove and sorted_results:
			# w2v threshhold + added weights
			if(google_glove[0][0] < 0.8):
				if(google_glove[0][0] < 0.7):
					if(google_glove[0][0] < 0.51):
						weights[0] += 20
					weights[0] += 10
				weights[0] += 3
			# glove threshhold + added weights
			if(google_glove[3][0] < 0.66):
				if(google_glove[3][0] < 0.51):
					if(google_glove[3][0] < 0.36):
						weights[1] += 20
					weights[1] += 10
				weights[1] += 4
			# path_sim threshhold + added weights
			if(sorted_results[0][0][1] > 0.24):
				if(sorted_results[0][0][1] > 0.34):
					if(sorted_results[0][0][1] > 0.49):
						weights[2] += 11
					weights[2] += 7
				weights[2] += 5
			# jcn_sim threshhold + added weights
			if(sorted_results[1][0][1] > 0.10):
				if(sorted_results[1][0][1] > 0.128):
					if(sorted_results[1][0][1] > 0.19):
						weights[3] += 11
					weights[3] += 7
				weights[3] += 5
			# lin_sim threshhold + added weights
			if(sorted_results[2][0][1] > 0.52):
				if(sorted_results[2][0][1] > 0.64):
					if(sorted_results[2][0][1] > 0.79):
						weights[4] += 11
					weights[4] += 7
				weights[4] += 5

			for i in [i[0] for i in sorted_results]:
				print(i)
			# google_glove[0][1] is w2v scipy cosine value

			maxWeight = max(weights)
			y = ([i for i, j in enumerate(weights) if j == maxWeight])
			x = int(y[0])
			print(x,y)
			if x == 0:
				string_answer_input = (google_glove[0][1])
			elif x == 1:
				string_answer_input = (google_glove[3][1])
			elif x == 2:
				string_answer_input = (sorted_results[0][0][5])
			elif x == 3:
				string_answer_input = (sorted_results[1][0][5])
			elif x == 4:
				string_answer_input = (sorted_results[2][0][5])
		else:
			return("no comparisons")
		
		print("Threshold chose word: ", string_answer_input)
		return string_answer_input

