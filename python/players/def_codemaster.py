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
		red_words = []
		cm_wordlist = []
		num_best = np.inf

		with open('players/cm_wordlist.txt') as infile:
			for line in infile:
				cm_wordlist.append(line.rstrip())

		# gather the synsets of both red and black-labeled words.
		for i in range(25):
			if(self.maps[i] == "Assassin"):
				black = self.words[i].lower()
			elif(self.maps[i] != "Red" or self.words[i][0] == '*'):
				continue
			else:
				red_words.append(self.words[i].lower())

		print("red:  ", red_words)
		print("black:", black)

		li = []
		for word in reversed(cm_wordlist):
			for i in red_words:
				for j in red_words:
					if i != j:
						dist = scipy.spatial.distance.cosine(self.word_vectors[word], 
							self.slerp(self.word_vectors[i], self.word_vectors[j], 0.5))

						if dist < num_best and word not in red_words and self.arr_not_in_word(word, red_words):
							num_best = dist
							word_best = word
							li.append((num_best, word_best))
					if i == j:
						dist = scipy.spatial.distance.cosine(self.word_vectors[word], self.word_vectors[i])
						if dist < num_best and word not in red_words and self.arr_not_in_word(word, red_words):
							num_best = dist
							word_best = word
							li.append((num_best, word_best))


			# for i in range(len(red_words)):
			# 	for j in range(i, len(red_words)):
			# 		try:
			# 			dist = scipy.spatial.distance.cosine(self.word_vectors[word], 
			# 				self.slerp(self.word_vectors[red_words[i]], self.word_vectors[red_words[j]], 0.5))

			# 			if dist < num_best and word not in red_words and self.arr_not_in_word(word, red_words):
			# 				num_best = dist
			# 				word_best = word
			# 				li.append((num_best, word_best))
			# 		except:
			# 			continue

		li = list(sorted(li))
		print(li)
		# select the 1st element in li, which is the "String clue"
		list_comp = [i[1] for i in li]
		print("The clue is: ", list_comp[0])
		# return in array styled: ["clue", number]
		return [list_comp[0], 1]
		

	def arr_not_in_word(self, word, arr):
		wordnet_lemmatizer = WordNetLemmatizer()
		lancaster_stemmer = LancasterStemmer()
		lemm = wordnet_lemmatizer.lemmatize(word)
		lancas = lancaster_stemmer.stem(word)

		for i in arr:
			if(i == lemm or i == lancas):
				return False
		return True


	def slerp(self, p0, p1, t):
	    omega = arccos(dot(p0/norm(p0), p1/norm(p1)))
	    so = sin(omega)
	    return sin((1.0-t)*omega) / so * p0 + sin(t*omega)/so * p1

