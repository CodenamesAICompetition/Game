import subprocess

# for everything else but glove vs glove
def run():

	# w2v_thresholds vs glove300
	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "game.py", "players.codemaster_w2v_03", "players.guesser_glove", "--w2v", "players/GoogleNews-vectors-negative300.bin", "--glove", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "game.py", "players.codemaster_w2v_05", "players.guesser_glove", "--w2v", "players/GoogleNews-vectors-negative300.bin", "--glove", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "game.py", "players.codemaster_w2v_07", "players.guesser_glove", "--w2v", "players/GoogleNews-vectors-negative300.bin", "--glove", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50


	# glove300_thresholds vs glove300 (GLOVE V GLOVE)
	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_glove_03", "players.guesser_glove", "--glove_cm", "players/glove/glove.6B.300d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_glove_05", "players.guesser_glove", "--glove_cm", "players/glove/glove.6B.300d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_glove_07", "players.guesser_glove", "--glove_cm", "players/glove/glove.6B.300d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50


	# glove200_thresholds vs glove300 (GLOVE V GLOVE)
	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_glove_03", "players.guesser_glove", "--glove_cm", "players/glove/glove.6B.200d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_glove_05", "players.guesser_glove", "--glove_cm", "players/glove/glove.6B.200d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_glove_07", "players.guesser_glove", "--glove_cm", "players/glove/glove.6B.200d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50
	

	# glove100_thresholds vs glove300 (GLOVE V GLOVE)
	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_glove_03", "players.guesser_glove", "--glove_cm", "players/glove/glove.6B.100d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_glove_05", "players.guesser_glove", "--glove_cm", "players/glove/glove.6B.100d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_glove_07", "players.guesser_glove", "--glove_cm", "players/glove/glove.6B.100d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50


	# glove50_thresholds vs glove300 (GLOVE V GLOVE)
	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_glove_03", "players.guesser_glove", "--glove_cm", "players/glove/glove.6B.50d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_glove_05", "players.guesser_glove", "--glove_cm", "players/glove/glove.6B.50d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_glove_07", "players.guesser_glove", "--glove_cm", "players/glove/glove.6B.50d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50


	# w2vglove300_thresholds vs glove300 (GLOVE V GLOVE)
	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_w2vglove_03", "players.guesser_glove", "--w2v", "players/GoogleNews-vectors-negative300.bin", "--glove_cm", "players/glove/glove.6B.300d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_w2vglove_05", "players.guesser_glove", "--w2v", "players/GoogleNews-vectors-negative300.bin", "--glove_cm", "players/glove/glove.6B.300d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_w2vglove_07", "players.guesser_glove", "--w2v", "players/GoogleNews-vectors-negative300.bin", "--glove_cm", "players/glove/glove.6B.300d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50


	# w2vglove200_thresholds vs glove300 (GLOVE V GLOVE)
	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_w2vglove_03", "players.guesser_glove", "--w2v", "players/GoogleNews-vectors-negative300.bin", "--glove_cm", "players/glove/glove.6B.200d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_w2vglove_05", "players.guesser_glove", "--w2v", "players/GoogleNews-vectors-negative300.bin", "--glove_cm", "players/glove/glove.6B.200d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_w2vglove_07", "players.guesser_glove", "--w2v", "players/GoogleNews-vectors-negative300.bin", "--glove_cm", "players/glove/glove.6B.200d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50


	# w2vglove100_thresholds vs glove300 (GLOVE V GLOVE)
	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_w2vglove_03", "players.guesser_glove", "--w2v", "players/GoogleNews-vectors-negative300.bin", "--glove_cm", "players/glove/glove.6B.100d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_w2vglove_05", "players.guesser_glove", "--w2v", "players/GoogleNews-vectors-negative300.bin", "--glove_cm", "players/glove/glove.6B.100d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_w2vglove_07", "players.guesser_glove", "--w2v", "players/GoogleNews-vectors-negative300.bin", "--glove_cm", "players/glove/glove.6B.100d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50


	# w2vglove50_thresholds vs glove300 (GLOVE V GLOVE)
	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_w2vglove_03", "players.guesser_glove", "--w2v", "players/GoogleNews-vectors-negative300.bin", "--glove_cm", "players/glove/glove.6B.50d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_w2vglove_05", "players.guesser_glove", "--w2v", "players/GoogleNews-vectors-negative300.bin", "--glove_cm", "players/glove/glove.6B.50d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50

	counter = 100
	for i in range(30):
		str_counter = str(int(counter))
		subprocess.run(["python", "glove_glove.py", "players.codemaster_w2vglove_07", "players.guesser_glove", "--w2v", "players/GoogleNews-vectors-negative300.bin", "--glove_cm", "players/glove/glove.6B.50d.txt", "--glove_guesser", "players/glove/glove.6B.200d.txt", "--seed", str_counter])
		counter += 50


run()

