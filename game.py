import random
import array
import os
import sys
import colorama
from players.codemaster import *
from players.guesser import *
try:
	from players.ai_guesser import *
	from players.ai_codemaster import *
except:
	pass
from players.wn_guesser import *
from players.wn_codemaster import *
# The WordNet corpus reader gives access to the Open Multilingual WordNet, using ISO-639 language codes.


class Game:
	guesser = 0
	words = 0
	codemaster = 0
	maps = 0


	def __init__(self):
		if(sys.argv[1]!="human" or sys.argv[2]!="human"):
			brown_ic = wordnet_ic.ic('ic-brown.dat')
			glove_vecs = {}
			word_vectors = word2vec.KeyedVectors.load_word2vec_format(
			'players/GoogleNews-vectors-negative300.bin', binary=True, unicode_errors='ignore', limit=500000)
			with open('players/glove/glove.6B.300d.txt') as infile:
				for line in infile:
					line = line.rstrip().split(' ')
					glove_vecs[line[0]] = np.array([float(n) for n in line[1:]])
		if len(sys.argv) == 1:
			self.guesser =  human_guesser()
			self.codemaster = human_codemaster()
		else:
			if sys.argv[1] == "human":
				self.codemaster = human_codemaster()
			elif sys.argv[1] == "ai":
				self.codemaster = ai_codemaster()
			else:
				self.codemaster = wn_codemaster(brown_ic, glove_vecs, word_vectors)

			if sys.argv[2] == "human":
				self.guesser = human_guesser()
			elif sys.argv[2] == "ai":
				self.guesser = ai_guesser()
			else:
				self.guesser = wn_guesser(brown_ic, glove_vecs, word_vectors)
		f = open("game_wordlist.txt", "r")
		if f.mode == 'r':
			temp_array = f.read().splitlines()
			self.words = set([])
			for x in range(0, 25):
				self.words.add(random.choice(temp_array))
			# if duplicates were detected and the set length is not 25 then restart
			if len(self.words) != 25:
				self.__init__()
			self.words = list(self.words)
 
		self.maps = ["Red"]*8 + ["Blue"]*7 + ["Civilian"]*9 + ["Assassin"]
		random.shuffle(self.maps)


	def display_board_codemaster(self):
		print(str.center(colorama.Fore.YELLOW + "___________________________BOARD___________________________\n", 60))
		counter = 0
		for i in range(len(self.words)):
			if counter >= 1 and i % 5 == 0:
				print("\n")
			if self.maps[i] is 'Red':
				print(str.center(colorama.Fore.RED + self.words[i], 15), " ", end='')
				counter += 1
			elif self.maps[i] is 'Blue':
				print(str.center(colorama.Fore.BLUE + self.words[i], 15), " ", end='')
				counter += 1
			elif self.maps[i] is 'Civilian':
				print(str.center(colorama.Fore.WHITE + self.words[i], 15), " ", end='')
				counter += 1
			else:
				print(str.center(colorama.Fore.MAGENTA + self.words[i], 15), " ", end='')
				counter += 1
		print(str.center(colorama.Fore.YELLOW + "\n___________________________________________________________", 60))
		print("\n")

 
	def display_board_guesser(self):
		print(colorama.Style.RESET_ALL)
		print(str.center("___________________________BOARD___________________________", 60))
		counter = 0
		for i in range(len(self.words)):
			# newline for every 5 prints
			if i % 5 == 0:
				print("\n")
			# centers the output
			print(str.center(self.words[i], 10), " ", end='')
 
		print(str.center("\n___________________________________________________________", 60))
		print("\n")


	def display_map(self):
		print("\n")
		print(str.center(colorama.Fore.YELLOW + "____________________________MAP____________________________\n", 55))
		counter = 0
		for i in range(len(self.maps)):
			if counter >= 1 and i % 5 == 0:
				print("\n")
			if self.maps[i] is 'Red':
				print(str.center(colorama.Fore.RED + self.maps[i], 15), " ", end='')
				counter += 1
			elif self.maps[i] is 'Blue':
				print(str.center(colorama.Fore.BLUE + self.maps[i], 15), " ", end='')
				counter += 1
			elif self.maps[i] is 'Civilian':
				print(str.center(colorama.Fore.WHITE + self.maps[i], 15), " ", end='')
				counter += 1
			else:
				print(str.center(colorama.Fore.MAGENTA + self.maps[i], 15), " ", end='')
				counter += 1
		print(str.center(colorama.Fore.YELLOW + "\n___________________________________________________________", 55))
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
 
 
	def write_results(self):
		red_result = 0
		blue_result = 0
		civ_result = 0
		assa_result = 0
		# if the guesser wasn't human
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

			# append to file
			f = open("bot_results.txt", "a")
			# if successfully opened start appending
			if f.mode == 'a':
				f.write("R: %d B: %d C: %d A: %d\r\n" % (red_result, blue_result, civ_result, assa_result))
			f.close()
 
	   
	def run(self):
		string_condition = "Hit_Red"
		print("========================GAME START========================\n")

		while(string_condition != "Lose" or string_condition != "Win"):
			self.cls()
			words_in_play = self.list_words()
			map_in_play = self.list_map()
			self.codemaster.get_map(map_in_play)
			self.codemaster.get_board(words_in_play)
			self.display_board_codemaster()
			self.display_map()
			clue, num = self.codemaster.give_clue()
			num = int(num)

			for i in reversed(range(num)):
				self.guesser.clues.append((clue,num-i)) 
			self.cls()
			self.display_board_guesser()
			self.guesser.get_clue(clue, num)
			
			string_condition = "Hit_Red"
		   
			while(string_condition == "Hit_Red"):
				#num -= 1
				self.guesser.get_board(words_in_play)
				guess_answer = self.guesser.give_answer()
				# if no comparisons were made/found than retry input from codemaster
				if(guess_answer == ("no comparisons")):
					break
				guess_answer_index = words_in_play.index(guess_answer.upper().strip())
				string_condition = self.accept_guess(guess_answer_index)

				if string_condition == "Hit_Red":
					self.guesser.clues.pop()
					self.cls()
					self.display_board_guesser()
					if(self.guesser.clues):
						clue=self.guesser.clues[len(self.guesser.clues)-1]
						print("The clue is:", clue[0], clue[1], sep =" ")
					else:
						string_condition="Still Going"
				   
				elif string_condition == "Still Going":
					break
 
				elif string_condition == "Lose":
					self.display_board_codemaster()
					print("You Lost")
					self.write_results()
					exit()
 
				elif string_condition == "Win":
					self.display_board_codemaster()
					print("You Won")
					self.write_results()
					exit()


if __name__ == "__main__":
	game = Game()
	game.run()
