import subprocess

# for everything else but glove vs glove
def run():

	counter = 100

	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "game.py", "players.codemaster_wn_lin", "players.guesser_wn_lin", "--wordnet", "ic-brown.dat", "--seed", str_counter])
		counter += 50


def glove_vs_glove():
	counter = 100

	for i in range(20):
		str_counter = str(int(counter))
		subprocess.run(["python", "game_no_w2v.py", "players.codemaster_glove_07", "players.guesser_glove", str_counter])
		counter += 50


run()