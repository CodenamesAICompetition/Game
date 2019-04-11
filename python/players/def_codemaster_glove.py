from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import wordnet_ic
from numpy.linalg import norm
from players.codemaster import codemaster
from operator import itemgetter
from numpy import *
import gensim.models.keyedvectors as word2vec
import gensim.downloader as api
import itertools
import numpy as np
import random
import scipy


class ai_codemaster(codemaster):

	def __init__(self, brown_ic=None, glove_vecs=None, word_vectors=None):
		self.brown_ic = brown_ic
		self.glove_vecs = glove_vecs
		self.word_vectors = word_vectors
		self.wordnet_lemmatizer = WordNetLemmatizer()
		self.lancaster_stemmer = LancasterStemmer()
		self.cm_wordlist = []
		with open('players/cm_wordlist.txt') as infile:
			for line in infile:
				self.cm_wordlist.append(line.rstrip())

		self.bad_word_dists = None
		self.red_word_dists = None

	def get_board(self, words):
		self.words = words
		return words

	def get_map(self, maps):
		self.maps = maps
		return maps

	def get_bot_text(self, bot_array):
		self.bot_array = bot_array
		return bot_array

	def give_clue(self):
		cos_dist = scipy.spatial.distance.cosine
		red_words = []
		bad_words = []
		
		# Creates Red-Labeled Word arrays, and everything else arrays
		for i in range(25):
			if self.words[i][0] == '*':
				continue
			elif self.maps[i] == "Assassin" or self.maps[i] == "Blue" or self.maps[i] == "Civilian":
				bad_words.append(self.words[i].lower())
			else:
				red_words.append(self.words[i].lower())
		print("RED:\t", red_words)

		all_vectors = (self.glove_vecs,)
		bests = {}
		if not self.bad_word_dists:
			self.bad_word_dists = {}
			for word in self.cm_wordlist:
				self.bad_word_dists[word] = {}
				for val in bad_words:
					b_dist = cos_dist(self.concatenate(val, all_vectors), self.concatenate(word, all_vectors))
					self.bad_word_dists[word][val] = b_dist

			self.red_word_dists = {}
			for word in red_words:
				self.red_word_dists[word] = {}
				for val in self.cm_wordlist:
					b_dist = cos_dist(self.concatenate(val, all_vectors), self.concatenate(word, all_vectors))
					self.red_word_dists[word][val] = b_dist
		else:
			to_remove = set(self.bad_word_dists) - set(bad_words)
			for word in to_remove:
				del self.bad_word_dists[word]
			to_remove = set(self.red_word_dists) - set(red_words)
			for word in to_remove:
				del self.red_word_dists[word]

		for clue_num in range(1,3+1):
			best_per_dist = np.inf
			best_per = ''
			best_red_word = ''
			for red_word in list(itertools.combinations(red_words, clue_num)):
				best_word = ''
				best_dist = np.inf
				for word in self.cm_wordlist:
					if not self.arr_not_in_word(word, red_words + bad_words):
						continue
					bad_dist = np.inf
					worst_bad = ''
					for bad_word in bad_word_dists[word]:
						if bad_word_dists[word][bad_word] < bad_dist:
							bad_dist = bad_word_dists[word][bad_word]
							worst_bad = bad_word
					worst_red = 0 
					for red in red_word:
						dist = red_word_dists[red][word]
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
			bests[clue_num] = (best_red_word, best_per, best_per_dist)
		
		print("BESTS: ", bests)
		li = []
		pi = []
		for clue_num, clue in bests.items():
			best_red_word, combined_clue, combined_score = clue
			worst = -np.inf
			best = np.inf
			worst_word = ''
			for word in best_red_word:
				dist = cos_dist(self.concatenate(word,all_vectors),self.concatenate(combined_clue,all_vectors))
				if dist > worst:
					worst_word = word
					worst = dist
				if dist < best:
					best = dist

			li.append((worst/best, best_red_word, worst_word, combined_clue,
				combined_score,combined_score**len(best_red_word)))

		print("LI: ", li)
		print("The clue is: ", li[0][3])
		# return in array styled: ["clue", number]
		return [li[0][3], 1]

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
		factor = 1.0/float(len(words))
		new_word = self.concatenate(words[0],wordvecs)*factor
		for word in words[1:]:
			new_word += self.concatenate(word,wordvecs)*factor
		return new_word

	def concatenate(self, word, wordvecs):
		concatenated = wordvecs[0][word]
		for vec in wordvecs[1:]:
			concatenated = np.hstack((concatenated,vec[word] ))
		return concatenated

