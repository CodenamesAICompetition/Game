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
		cm_wordlist = []
		red_words = []
		bad_words = []
		with open('players/revised.txt') as infile:
			for line in infile:
				cm_wordlist.append(line.rstrip())
		
		# Creates Red Word arrays, and everything else arrays
		for i in range(25):
			if self.words[i][0] == '*':
				continue
			elif self.maps[i] == "Assassin" or self.maps[i] == "Blue" or self.maps[i] == "Civilian":
				bad_words.append(self.words[i].lower())
			else:
				red_words.append(self.words[i].lower())
		print("RED:\t", red_words)

		all_vectors = (self.word_vectors, self.glove_vecs,)
		bests = {}

		for clue_num in range(1,2+1):
			best_per_dist = np.inf
			best_per = ''
			best_red_word = ''
			for red_word in list(itertools.combinations(red_words, clue_num)):
				#REPLACE THIS FOR NLTK STUFF
				combined_word = self.combine(red_word,all_vectors)
				best_word = ''
				best_dist = np.inf
				for word in cm_wordlist:
					if not self.arr_not_in_word(word, red_words):
						continue
					#REPLACE COSINE DISTANCE FOR NLTK STUFF
					distance = scipy.spatial.distance.cosine(combined_word,self.concatenate(word,all_vectors))
					if distance < best_dist:
						best_dist = distance
						best_word = word
						if best_dist < best_per_dist:
							best_per_dist = best_dist
							best_per = best_word
							best_red_word = red_word

			bests[clue_num] = (best_red_word,best_per,best_per_dist)
		li = []
		for clue_num, clue in bests.items():
			best_red_word,combined_clue,combined_score = clue
			worst = -np.inf
			best = np.inf
			worst_word = ''
			for word in best_red_word:
				dist = scipy.spatial.distance.cosine(self.concatenate(word,all_vectors),
					self.concatenate(combined_clue,all_vectors))
				if dist > worst:
					worst_word = word
					worst = dist
				if dist < best:
					best = dist
			li.append((clue_num, ":\t", worst/best, best_red_word, worst_word, combined_clue, combined_score))

		print(bests)
		print(li)
		print("The clue is: ", li[0][5])
		# return in array styled: ["clue", number]
		return [li[0][5], 1]

	def arr_not_in_word(self, word, arr):
		if word in arr:
			return False
		wordnet_lemmatizer = WordNetLemmatizer()
		lancaster_stemmer = LancasterStemmer()
		lemm = wordnet_lemmatizer.lemmatize(word)
		lancas = lancaster_stemmer.stem(word)
		
		for i in arr:
			if i == lemm or i == lancas:
				return False
			if i.find(word) != -1:
				return False
			if word.find(i) != -1:
				return False
		return True

	def slerp(self, p0, p1, t):
		omega = arccos(dot(p0/norm(p0), p1/norm(p1)))
		so = sin(omega)
		return sin((1.0-t)*omega) / so * p0 + sin(t*omega)/so * p1

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

