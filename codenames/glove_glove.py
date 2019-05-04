from players.codemaster import *
from players.guesser import *
from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import wordnet_ic
import numpy as np
import scipy
import itertools
import importlib
import random
import array
import os
import sys
import colorama
import gensim.models.keyedvectors as word2vec
import gensim.downloader as api
import argparse


class Game:
	guesser = 0
	codemaster = 0
	
	def __init__(self):
		parser = argparse.ArgumentParser(
        description="Run the Codenames AI competition game.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
		parser.add_argument("codemaster", help="Path to codemaster package or 'human'")
		parser.add_argument("guesser", help="Path to guesser package or 'human'")
		parser.add_argument("--seed", help="Random seed value for board state -- integer or 'time'",default='time')
		parser.add_argument("--w2v", help="Path to w2v file or 'none'",default='none')
		parser.add_argument("--glove_cm", help="Path to glove file or 'none'",default='none')
		parser.add_argument("--glove_guesser", help="Path to glove file or 'none'",default='none')
		parser.add_argument("--wordnet", help="Name of wordnet file or 'none', most like ic-brown.dat",default='none')
		
		args = parser.parse_args()

		# if the game is going to have an ai, load up word vectors
		if sys.argv[1] != "human" or sys.argv[2] != "human":
			brown_ic = None
			if args.wordnet != 'none':
				brown_ic = wordnet_ic.ic(args.wordnet)
			glove_vecs_cm = {}
			if args.glove_cm != 'none':
				with open(args.glove_cm, encoding="utf-8") as infile:
					for line in infile:
						line = line.rstrip().split(' ')
						glove_vecs_cm[line[0]] = np.array([float(n) for n in line[1:]])
				print('loaded glove cm vectors')

			glove_vecs_guesser = {}
			if args.glove_guesser != 'none':
				with open(args.glove_guesser, encoding="utf-8") as infile:
					for line in infile:
						line = line.rstrip().split(' ')
						glove_vecs_guesser[line[0]] = np.array([float(n) for n in line[1:]])
				print('loaded glove guesser vectors')


			word_vectors = {}
			if args.w2v != 'none':
				word_vectors = word2vec.KeyedVectors.load_word2vec_format(
					args.w2v, binary=True, unicode_errors='ignore')
				print('loaded word vectors')

		if args.codemaster == "human":
			self.codemaster = human_codemaster()
			print('human codemaster')
		else:
			codemaster_module = importlib.import_module(args.codemaster)
			self.codemaster = codemaster_module.ai_codemaster(brown_ic, glove_vecs_cm, word_vectors)
			print('loaded codemaster')

		if args.guesser == "human":
			self.guesser = human_guesser()
			print('human guesser')
		else:
			guesser_module = importlib.import_module(args.guesser)
			self.guesser = guesser_module.ai_guesser(brown_ic, glove_vecs_guesser, word_vectors)
			print('loaded guesser')

		self.seed = 'time'
		if args.seed != 'time':
			self.seed = args.seed
			random.seed(int(args.seed))

		f = open("game_wordpool.txt", "r")
		
		if f.mode == 'r':
			temp_array = f.read().splitlines()
			self.words = set([])
			# if duplicates were detected and the set length is not 25 then restart
			while len(self.words) != 25:
				self.words = set([])
				for x in range(0, 25):
					random.shuffle(temp_array)
					self.words.add(temp_array.pop())
			self.words = list(sorted(self.words))
			random.shuffle(self.words)

		self.maps = ["Red"]*8 + ["Blue"]*7 + ["Civilian"]*9 + ["Assassin"]
		random.shuffle(self.maps)

	# prints out board with color-paired words, only for codemaster, color && stylistic
	def display_board_codemaster(self):
		print(str.center("___________________________BOARD___________________________\n", 60))
		counter = 0
		for i in range(len(self.words)):
			if counter >= 1 and i % 5 == 0:
				print("\n")
			if self.maps[i] is 'Red':
				print(str.center(colorama.Fore.RED + self.words[i], 15), " ", end='')
				counter += 1
			elif self.maps[i] is 'Blue':
				print(str.center(colorama.Fore.RESET + self.words[i], 15), " ", end='')
				counter += 1
			elif self.maps[i] is 'Civilian':
				print(str.center(colorama.Fore.RESET + self.words[i], 15), " ", end='')
				counter += 1
			else:
				print(str.center(colorama.Fore.MAGENTA + self.words[i], 15), " ", end='')
				counter += 1
		print(str.center(colorama.Fore.RESET + 
			"\n___________________________________________________________", 60))
		print("\n")

	# prints the list of words in a board like fashion (5x5)
	def display_board(self):
		print(colorama.Style.RESET_ALL)
		print(str.center("___________________________BOARD___________________________", 60))
		counter = 0
		for i in range(len(self.words)):
			if i % 5 == 0:
				print("\n")
			print(str.center(self.words[i], 10), " ", end='')

		print(str.center("\n___________________________________________________________", 60))
		print("\n")

	# aesthetic purposes, doesn't impact function of code.
	def display_map(self):
		print("\n")
		print(str.center(colorama.Fore.RESET + 
			"____________________________MAP____________________________\n", 55))
		counter = 0
		for i in range(len(self.maps)):
			if counter >= 1 and i % 5 == 0:
				print("\n")
			if self.maps[i] is 'Red':
				print(str.center(colorama.Fore.RED + self.maps[i], 15), " ", end='')
				counter += 1
			elif self.maps[i] is 'Blue':
				print(str.center(colorama.Fore.RESET + self.maps[i], 15), " ", end='')
				counter += 1
			elif self.maps[i] is 'Civilian':
				print(str.center(colorama.Fore.RESET + self.maps[i], 15), " ", end='')
				counter += 1
			else:
				print(str.center(colorama.Fore.MAGENTA + self.maps[i], 15), " ", end='')
				counter += 1
		print(str.center(colorama.Fore.RESET + 
			"\n___________________________________________________________", 55))
		print("\n")

	def list_words(self):
		return self.words

	def list_map(self):
		return self.maps

	# takes in an int index called guess to compare with the Map
	def accept_guess(self,guess_index):
		# CodeMaster will always win with Red and lose if Blue =/= 7 or Assassin == 1
		if self.maps[guess_index] == "Red":
			self.words[guess_index] = "*Red*"
			if self.words.count("*Red*") >= 8:
				return "Win"
			return "Hit_Red"
		elif self.maps[guess_index] == "Blue":
			self.words[guess_index] = "*Blue*"
			if self.words.count("*Blue*") >= 7:
				return "Lose"
			else:
				return "Still Going"
		elif self.maps[guess_index] == "Assassin":
			self.words[guess_index] = "*Assassin*"
			return "Lose"
		else:
			self.words[guess_index] = "*Civilian*"
			return "Still Going"

	def cls(self):
		print('\n'*4)

	def write_results(self, num_of_turns):
		red_result = 0
		blue_result = 0
		civ_result = 0
		assa_result = 0

		if not sys.argv[2] == "human":
			for i in range(len(self.words)):
				if self.words[i] == "*Red*":
					red_result += 1
				elif self.words[i] == "*Blue*":
					blue_result += 1
				elif self.words[i] == "*Civilian*":
					civ_result += 1
				elif self.words[i] == "*Assassin*":
					assa_result += 1
			total = red_result + blue_result + civ_result + assa_result

			f = open("bot_results.txt", "a")
			# if successfully opened start appending
			if f.mode == 'a':
				f.write(
					f'TOTAL:{num_of_turns} B:{blue_result} C:{civ_result} A:{assa_result}'
					f' R:{red_result} CM:{sys.argv[1]} GUESSER:{sys.argv[2]} SEED:{self.seed}\n'
					)
			f.close()

	def run(self):
		game_condition = "Hit_Red"
		game_counter = 0
		while game_condition != "Lose" or game_condition != "Win":
			# board setup and display
			self.cls()
			words_in_play = self.list_words()
			current_map = self.list_map()
			self.codemaster.receive_game_state(words_in_play, current_map)
			# self.display_map()
			self.display_board_codemaster()
			# codemaster gives clue & number here
			clue, num = self.codemaster.give_clue()
			game_counter += 1
			keep_guessing = True
			guess_num = 0
			num = int(num)

			self.cls()
			self.guesser.get_clue(clue, num)
			
			game_condition = "Hit_Red"
			while guess_num <= num and keep_guessing and game_condition == "Hit_Red":
				self.guesser.get_board(words_in_play)
				guess_answer = self.guesser.give_answer()

				# if no comparisons were made/found than retry input from codemaster
				if guess_answer == "no comparisons":
					break
				guess_answer_index = words_in_play.index(guess_answer.upper().strip())
				game_condition = self.accept_guess(guess_answer_index)

				if game_condition == "Hit_Red":
					self.cls()
					self.display_board_codemaster()
					guess_num += 1
					print("Keep Guessing?")
					keep_guessing = self.guesser.keep_guessing(clue, words_in_play)
					print("The clue is :", clue, num, sep=" ")

				# if guesser selected a civilian or a blue-paired word
				elif game_condition == "Still Going":
					break

				elif game_condition == "Lose":
					self.display_board_codemaster()
					print("You Lost")
					game_counter = 25
					self.write_results(game_counter)
					print("Game Counter:", game_counter)
					exit()

				elif game_condition == "Win":
					self.display_board_codemaster()
					print("You Won")
					self.write_results(game_counter)
					print("Game Counter:", game_counter)
					exit()


if __name__ == "__main__":
	game = Game()
	game.run()