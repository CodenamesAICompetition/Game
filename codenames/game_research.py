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


class Alt_game:
	guesser = 0
	codemaster = 0

	def __init__(self):
		print("Hi, nothing to see here!")

	def game_pool(self):
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

	def set_players(self, cm, guesser, w2v, glove_cm, glove_guesser, wordnet, cm_wordlist, seed):
		self.cm_pckge = cm
		self.guesser_pckge = guesser
		if glove_cm == None:
			glove_cm = ("None", {})
		if glove_guesser == None:
			glove_guesser = ("None", {})

		self.glove_cm = glove_cm[0]
		self.glove_guesser = glove_guesser[0]

		codemaster_module = importlib.import_module(cm)
		self.codemaster = codemaster_module.ai_codemaster(wordnet, glove_cm[1], w2v, cm_wordlist)
		print('loaded codemaster')

		guesser_module = importlib.import_module(guesser)
		self.guesser = guesser_module.ai_guesser(wordnet, glove_guesser[1], w2v)
		print('loaded guesser')

		self.seed = seed
		random.seed(seed)

	def write_results(self, num_of_turns):
		red_result = 0
		blue_result = 0
		civ_result = 0
		assa_result = 0

		str_cm_pckge = str(self.cm_pckge)
		str_guesser_pckge = str(self.guesser_pckge)
		str_seed = str(self.seed)
		str_glove_cm = str(self.glove_cm)
		str_glove_guesser = str(self.glove_guesser)

		for i in range(len(self.words)):
			if self.words[i] == "*Red*":
				red_result += 1
			elif self.words[i] == "*Blue*":
				blue_result += 1
			elif self.words[i] == "*Civilian*":
				civ_result += 1
			elif self.words[i] == "*Assassin*":
				assa_result += 1

		with open('bot_results.txt', 'a') as f:
			f.write(
				f'TOTAL:{num_of_turns} B:{blue_result} C:{civ_result} A:{assa_result} '
				f'R:{red_result} CM:{str_cm_pckge} GUESSER:{str_guesser_pckge} '
				f'SEED:{str_seed} Glove_CM:{str_glove_cm} Glove_Guesser:{str_glove_guesser}\n'
			)

	def run(self):
		print("NEW GAME\n\n")
		self.game_pool()
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

				elif game_condition == "Win":
					self.display_board_codemaster()
					print("You Won")
					self.write_results(game_counter)
					print("Game Counter:", game_counter)

			if game_condition == "Lose" or game_condition == "Win":
				break


if __name__ == "__main__":
	brown_ic = wordnet_ic.ic('ic-brown.dat')
	semcor_ic = wordnet_ic.ic('ic-semcor.dat')
	glove_vecs_50 = {}
	glove_vecs_100 = {}
	glove_vecs_200 = {}
	glove_vecs_300 = {}
	word_vectors = word2vec.KeyedVectors.load_word2vec_format(
		"players/GoogleNews-vectors-negative300.bin", binary=True, unicode_errors='ignore')

	cm_wordlist = []
	with open('players/cm_wordlist.txt') as infile:
		for line in infile:
			cm_wordlist.append(line.rstrip())

	with open("players/glove/glove.6B.50d.txt", encoding="utf-8") as infile:
		for line in infile:
			line = line.rstrip().split(' ')
			glove_vecs_50[line[0]] = np.array([float(n) for n in line[1:]])
	print('loaded glove50 vectors')

	with open("players/glove/glove.6B.100d.txt", encoding="utf-8") as infile:
		for line in infile:
			line = line.rstrip().split(' ')
			glove_vecs_100[line[0]] = np.array([float(n) for n in line[1:]])
	print('loaded glove100 vectors')

	with open("players/glove/glove.6B.200d.txt", encoding="utf-8") as infile:
		for line in infile:
			line = line.rstrip().split(' ')
			glove_vecs_200[line[0]] = np.array([float(n) for n in line[1:]])
	print('loaded glove200 vectors')

	with open("players/glove/glove.6B.300d.txt", encoding="utf-8") as infile:
		for line in infile:
			line = line.rstrip().split(' ')
			glove_vecs_300[line[0]] = np.array([float(n) for n in line[1:]])
	print('loaded glove300 vectors')

	glove_v50 = ("glove_v50", glove_vecs_50)
	glove_v100 = ("glove_v100", glove_vecs_100)
	glove_v200 = ("glove_v200", glove_vecs_200)
	glove_v300 = ("glove_v300", glove_vecs_300)

	c = [('players.codemaster_w2v_03', 0), ('players.codemaster_w2v_05', 0), ('players.codemaster_w2v_07', 0),
	('players.codemaster_glove_03', 300), ('players.codemaster_glove_03', 200), ('players.codemaster_glove_03', 100), ('players.codemaster_glove_03', 50),
	('players.codemaster_glove_05', 300), ('players.codemaster_glove_05', 200), ('players.codemaster_glove_05', 100), ('players.codemaster_glove_05', 50),
	('players.codemaster_glove_07', 300), ('players.codemaster_glove_07', 200), ('players.codemaster_glove_07', 100), ('players.codemaster_glove_07', 50),
	('players.codemaster_w2vglove_03', 300), ('players.codemaster_w2vglove_03', 200), ('players.codemaster_w2vglove_03', 100), ('players.codemaster_w2vglove_03', 50),
	('players.codemaster_w2vglove_05', 300), ('players.codemaster_w2vglove_05', 200), ('players.codemaster_w2vglove_05', 100), ('players.codemaster_w2vglove_05', 50),
	('players.codemaster_w2vglove_07', 300), ('players.codemaster_w2vglove_07', 200), ('players.codemaster_w2vglove_07', 100), ('players.codemaster_w2vglove_07', 50)]

	guesser = 'players.guesser_wn_lch'
	g_cm = None

	for codemaster in c:
		if codemaster[1] == 300:
			g_cm = glove_v300
		elif codemaster[1] == 200:
			g_cm = glove_v200
		elif codemaster[1] == 100:
			g_cm = glove_v100
		elif codemaster[1] == 50:
			g_cm = glove_v50


		for seed in range(30):
			game = Alt_game()
			# def set_players(cm,          guesser,     w2v,   glove_cm, glove_guesser, wordnet, cm_wordlist, seed):
			game.set_players(codemaster[0], guesser, word_vectors, g_cm, None, brown_ic, cm_wordlist, seed)
			game.run()
