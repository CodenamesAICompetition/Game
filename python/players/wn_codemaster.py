from nltk.stem import WordNetLemmatizer
from players.codemaster import codemaster
import random

class wn_codemaster(codemaster):

	def get_board(self, words):
		self.words = words


	def get_bot_text(self, bot_array):
		self.bot_array = bot_array


	def give_clue(self):

		# assuming none of the words in botwordlist is also in CNwordlist, gotta add that
		f = open("cm_wordlist.txt", "r")

		if f.mode == 'r':
			temp_arr = f.read().splitlines()

		bot_string_input = random.choice(temp_arr)
		bot_num_input = random.randint(1, 5)
		clue = [str(bot_string_input), str(bot_num_input)]
		return clue


	def check_singular(self, word):

	    bool_plur, lemma = is_plural(self.word)
	    print(self.word, lemma, bool_plur)

	    # if word is plural return true, elsewise false
	    return bool_plur


	def is_plural(self, word):

	    wnl = WordNetLemmatizer()
	    lemma = wnl.lemmatize(self.word, 'n')
	    plural = True if self.word is not lemma else False
	    return plural, lemma

