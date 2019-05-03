import subprocess


counter = 100

for i in range(20):
	str_counter = str(int(counter))
	subprocess.run(["python", "game.py", "players.codemaster_wn_lin", "players.guesser_wn_lin", "--wordnet", "ic-brown.dat", "--seed", str_counter])
	counter += 50
