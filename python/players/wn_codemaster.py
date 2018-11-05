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
		
		return bool_plur


	def is_plural(self, word):

		wnl = WordNetLemmatizer()
		lemma = wnl.lemmatize(self.word, 'n')
		plural = True if self.word is not lemma else False
		return plural, lemma


	def work(self, words):
		return 1
		# with open('glove/glove.6B.50d.txt') as infile:
	 #        for line in infile:
	 #            line = line.rstrip().split(' ')
	 #            words[line[0]] = np.array([float(n) for n in line[1:]])

	 #    for i in range(25):
	 #        for j in range(25):
	 #            if board[i] == board[j]:
	 #                continue

	 #            linalg = np.dot(words[board[i].lower()] / np.linalg.norm(words[board[i].lower()]),
	 #                words[board[j].lower()] / np.linalg.norm(words[board[j].lower()]))
	 #            result.append([board[i], board[j], linalg])

	 #    result = list(reversed(sorted(result, key=take_third)))
	 #    return result[:5]

