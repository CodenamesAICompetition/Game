
from textblob import Word

def sss():
	word = Word("plant")
	print(word.synsets[:5])
	print(word.definitions[:5])
	plant = word.synsets[1]

	print(plant)
	print(plant.lemma_names)
	print(plant.hypernyms())
	print(plant.hyponyms()[:3])

sss()