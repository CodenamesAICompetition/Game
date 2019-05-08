from nltk.corpus import wordnet as wn
from nltk.corpus import words
from nltk.corpus import wordnet_ic
from nltk.corpus import genesis

dog = wn.synsets('dog')
wolf = wn.synsets('wolf')

brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')
genesis_ic = wn.ic(genesis, False, 0.0)


def path(a, b):
	print("Def: ", a.path_similarity(b))
	print("Brown: ", a.path_similarity(b, brown_ic))
	print("Semcor: ", a.path_similarity(b, semcor_ic))
	print("Genesis: ", a.path_similarity(b, genesis_ic))

def wup(a, b):
	print("Def: ", a.wup_similarity(b))
	print("Brown: ", a.wup_similarity(b, brown_ic))
	print("Semcor: ", a.wup_similarity(b, semcor_ic))
	print("Genesis: ", a.wup_similarity(b, genesis_ic))

def lch(a, b):
	print("Def: ", a.lch_similarity(b))
	print("Brown: ", a.lch_similarity(b, brown_ic))
	print("Semcor: ", a.lch_similarity(b, semcor_ic))
	print("Genesis: ", a.lch_similarity(b, genesis_ic))

for i in dog:
	for j in wolf:
		path(i, j)
		wup(i, j)
		lch(i, j)