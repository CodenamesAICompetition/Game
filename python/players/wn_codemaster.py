from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import wordnet_ic
from players.codemaster import codemaster
from allennlp.commands.elmo import ElmoEmbedder
from operator import itemgetter
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
		# self.word_vectors = word2vec.KeyedVectors.load_word2vec_format(
        #     'players/GoogleNews-vectors-negative300.bin', binary=True, unicode_errors='ignore')
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
		result_two = []
		red_word_synsets = []
		pat_results = []
		lch_results = []
		res_results = []

		for i in range(25):
			if(self.maps[i] != "Red" or self.words[i][0] == '*'):
				continue
			red_word_synsets.append(wordnet.synsets(self.words[i].lower()))

		for syn_list in red_word_synsets:
			for i in syn_list:
				for lemma in i.lemmas():
					try:
						result.append((i.hyponyms(), lemma.name(), "hypo"))
						result.append((i.member_holonyms(), lemma.name(), "mem_holo"))
						result.append((i.root_hypernyms(), lemma.name(), "root_hol"))
						for j in syn_list:
							result_two.append(i.lowest_common_hypernyms(j))
					except:
						continue

				for j in syn_list:
					try:
						pat = i.path_similarity(j)
						lch = i.lch_similarity(j)
						res = i.res_similarity(j, self.brown_ic)
						if(pat == 1 or pat is None):
							continue
						pat_results.append((pat, i, j))
						lch_results.append((lch, i, j))
						res_results.append((res, i, j))
					except:
						continue

		root_hypernym_list = []
		newlist = []
		for i in result_two:
			for j in i:
				for lemma in j.lemmas():
					if(self.check_useless(lemma.name()) or lemma.name().upper() in self.words):
						continue
					root_hypernym_list.append(lemma.name())

		for i in root_hypernym_list:
			if i not in newlist:
				newlist.append(i)

		print(newlist, "\n")
		pat_results = list(reversed(sorted(pat_results, key=itemgetter(0))))
		lch_results = list(reversed(sorted(lch_results, key=itemgetter(0))))
		res_results = list(reversed(sorted(res_results, key=itemgetter(0))))
		print(pat_results[:5])
		print(lch_results[:5])
		print(res_results[:5])

		clue = ["food", "1"]
		return clue


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


	def is_plural(self, word):
		wnl = WordNetLemmatizer()
		lemma = wnl.lemmatize(self.word, 'n')
		plural = True if self.word is not lemma else False
		return plural, lemma

		
