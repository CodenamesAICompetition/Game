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


	def __init__(self):
		self.brown_ic = wordnet_ic.ic('ic-brown.dat')
		self.glove_vecs = {}
		self.word_vectors = word2vec.KeyedVectors.load_word2vec_format(
            'players/GoogleNews-vectors-negative300.bin', binary=True, unicode_errors='ignore')
		# with open('glove/glove.6B.300d.txt') as infile:
		# 	for line in infile:
		# 		line = line.rstrip().split(' ')
		# 		self.glove_vecs[line[0]] = np.array([float(n) for n in line[1:]])


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

		print("red: ", red_words)
		print("black: ", black)

		# for syn_list in red_word_synsets:
		# 	for i in syn_list:
		# 		for i_lemma in i.lemmas():
		# 			try:
		# 				result.append((i.hyponyms(), i_lemma.name(), "hypo"))
		# 				result.append((i.member_holonyms(), i_lemma.name(), "mem_holo"))
		# 				result.append((i.root_hypernyms(), i_lemma.name(), "root_hol"))
		# 			except:
		# 				continue

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

		for i in range(len(list_of_words)):
			if(self.redund(list_of_words[i], red_words)):
				list_of_words.remove()

		print(list_of_words)
		clue = ["food", "1"]
		return clue


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


	def redund(self, word_one, word_two):
		if(word_one.lower() in word_two.lower() or word_two.lower() in word_one.lower()):
			return True


	def is_plural(self, word):
		wnl = WordNetLemmatizer()
		lemma = wnl.lemmatize(self.word, 'n')
		plural = True if self.word is not lemma else False
		return plural, lemma

		
