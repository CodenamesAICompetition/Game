from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import wordnet_ic
import numpy as np


def wordnet_synset(clue, board):
	pat_results = []
	jcn_results = []
	lin_results = []
	count = 0
	for i in board:
		for clue_list in wordnet.synsets(clue):
			pat_clue = jcn_clue = lin_clue = 0
			for board_list in wordnet.synsets(i):
				try:
					# only if the two compared words have the same part of speech
					pat = clue_list.path_similarity(board_list)
					jcn = clue_list.jcn_similarity(board_list, self.brown_ic)
					lin = clue_list.lin_similarity(board_list, self.brown_ic)
				except:
					continue
				if jcn:
					jcn_results.append(("jcn: ", jcn, count, clue_list, board_list, i))
					lin_results.append(("lin: ", lin, count, clue_list, board_list, i))
					if jcn > jcn_clue:
						jcn_clue = jcn
				if pat:
					pat_results.append(("pat: ", pat, count, clue_list, board_list, i))
					if pat > pat_clue:
						pat_clue = pat
	# if results list is empty
	if not pat_results or not jcn_results:
		return []

	pat_results = list(reversed(sorted(pat_results, key=itemgetter(1))))
	lin_results = list(reversed(sorted(lin_results, key=itemgetter(1))))
	jcn_results = list(reversed(sorted(jcn_results, key=itemgetter(1))))
	results = [pat_results[:3], jcn_results[:3], lin_results[:3]]
	return results