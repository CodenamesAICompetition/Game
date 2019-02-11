from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import wordnet_ic
from players.codemaster import codemaster
from allennlp.commands.elmo import ElmoEmbedder
from operator import itemgetter
from numpy import *
from numpy.linalg import norm
import gensim.models.keyedvectors as word2vec
import gensim.downloader as api
import itertools
import numpy as np
import random
import scipy


class wn_codemaster(codemaster):


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
		result = []
		red_word_synsets = []
		red_words = []
		cm_wordlist = []
		best = np.inf

		# with open('cm_wordlist.txt') as infile:
		# 	for line in infile:
		# 		cm_wordlist.append(line.rstrip())

		for i in range(25):
			if(self.maps[i] == "Assassin"):
				black = self.words[i].lower()
			elif(self.maps[i] != "Red" or self.words[i][0] == '*'):
				continue
			else:
				red_word_synsets.append(wordnet.synsets(self.words[i].lower()))
				red_words.append(self.words[i].lower())

		print("red:  ", red_words)
		print("black:", black)

		# guess = ['fire', 'bell']
		# for word in reversed(cm_wordlist):
		# 	try:
		# 		dist = scipy.spatial.distance.cosine(self.word_vectors[word],
		# 			slerp(self.word_vectors[guess[0]], self.word_vectors[guess[1]], 0.5))

		# 		if dist < best and word not in guess:
		# 			best = dist
		# 			print(best,word)
		# 	except:
		# 		continue

		list_of_words = []
		for i in range(len(red_words)):
			try:
				for j in range(i, len(red_words)):
					result = self.word_vectors.most_similar(positive=[red_words[i], red_words[j]], negative=[black])
					print("{}: {:.3f}".format(*result[0]))
				list_of_words.append(self.word_vectors.similar_by_word(red_words[i]))
			except:
				continue

		# code goes busts over here
		li = result.pop(0)
		print(li)

		for i in li:
			print(i[0])
			index = li.index(i)
			if(self.redund(i[0], red_words)):
				li.pop(index)

		print(li)
		return ["food", "2"]


	def slerp(self, p0, p1, t):
		omega = arccos(dot(p0/norm(p0), p1/norm(p1)))
		so = sin(omega)
		return sin((1.0-t)*omega / so * p0 + sin(t*omega)/so * p1)


	def check_singular(self, word):
		bool_plur, lemma = is_plural(self.word)
		print(self.word, lemma, bool_plur)
		return bool_plur


	def check_useless(self, string):
		if (string == "entity" or string == "abstract_entity" or string == "physical_entity" or 
			string == "abstraction" or string == "matter" or string == "physical_object" or string == "object" 
			or string == "artefact" or string == "artifact"):
			return True
		return False


	def redund(self, word_one, list_of_reds):
		for i in list_of_reds:
			if(word_one.lower() in i.lower() or i.lower() in word_one.lower()):
				return True
		return False


	def is_plural(self, word):
		wnl = WordNetLemmatizer()
		lemma = wnl.lemmatize(self.word, 'n')
		plural = True if self.word is not lemma else False
		return plural, lemma

		
