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
		self.syns = []
		for word in self.cm_wordlist:
			for synset_in_cmwordlist in wordnet.synsets(word):
				self.syns.append(synset_in_cmwordlist)

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
		lin_results = []
		count = 0
		red_words = []
		bad_words = []
		for i in range(25):
			if self.words[i][0] == '*':
				continue
			elif self.maps[i] == "Assassin" or self.maps[i] == "Blue" or self.maps[i] == "Civilian":
				bad_words.append(self.words[i].lower())
			else:
				red_words.append(self.words[i].lower())
		print("RED:\t", red_words)

		for red_word in red_words:
			for synset_in_cmwordlist in self.syns:
				lin_clue = 0
				for red_synset in wordnet.synsets(red_word):
					try:
						# only if the two compared words have the same part of speech
						lin_score = synset_in_cmwordlist.lin_similarity(red_synset, self.brown_ic)
					except:
						continue
					if lin_score:
						if not self.arr_not_in_word(synset_in_cmwordlist.lemma_names()[0], red_words+bad_words):
							continue
						lin_results.append((lin_score, synset_in_cmwordlist))
						if lin_score > lin_clue:
							lin_clue = lin_score

		lin_results = list(reversed(sorted(lin_results, key=itemgetter(0))))
		return [lin_results[0][1].lemma_names()[0], 1]

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
