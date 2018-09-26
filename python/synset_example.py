
from nltk.corpus import wordnet as wn

def sss():
	print(wn.synsets('sofa'))

	print(wn.synsets('ocean'))
	print(wn.synset('sofa.n.01').definition())
	print(wn.synset('pasta.n.01').hyponyms())
	print(wn.synset('pasta.n.01').hypernyms())
	print(wn.synset('dish.n.02').definition())
	print(wn.synset('snore.v.01').entailments())
	print(wn.synset('kitchen.n.01').part_holonyms() )
	

sss()