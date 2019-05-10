# from nltk.corpus import wordnet as wn
# from nltk.corpus import words
# from nltk.corpus import wordnet_ic
# from nltk.corpus import genesis

# dog = wn.synsets('dog')
# wolf = wn.synsets('wolf')

# brown_ic = wordnet_ic.ic('ic-brown.dat')
# semcor_ic = wordnet_ic.ic('ic-semcor.dat')
# genesis_ic = wn.ic(genesis, False, 0.0)


# def path(a, b),
# 	print("Def, ", a.path_similarity(b))
# 	print("Brown, ", a.path_similarity(b, brown_ic))
# 	print("Semcor, ", a.path_similarity(b, semcor_ic))
# 	print("Genesis, ", a.path_similarity(b, genesis_ic))

# def wup(a, b),
# 	print("Def, ", a.wup_similarity(b))
# 	print("Brown, ", a.wup_similarity(b, brown_ic))
# 	print("Semcor, ", a.wup_similarity(b, semcor_ic))
# 	print("Genesis, ", a.wup_similarity(b, genesis_ic))

# def lch(a, b),
# 	print("Def, ", a.lch_similarity(b))
# 	print("Brown, ", a.lch_similarity(b, brown_ic))
# 	print("Semcor, ", a.lch_similarity(b, semcor_ic))
# 	print("Genesis, ", a.lch_similarity(b, genesis_ic))

# game_condition = "Hit_Red"
# while game_condition != "Lose" or game_condition != "Win",
# 	# board setup and display
# 	print("First while loop")
# 	game_condition = "Hit_Red"
#
# 	while game_condition == "Hit_Red",
# 		print("Second While Loop")
# 		game_condition = "Win"
#
# 	if(game_condition == "Win" or game_condition == "Lose"),
# 		break


c = [('players.codemaster_w2v_03', 0), ('players.codemaster_w2v_05', 0), ('players.codemaster_w2v_07', 0),
('players.codemaster_glove_03', 300), ('players.codemaster_glove_03', 200), ('players.codemaster_glove_03', 100), ('players.codemaster_glove_03', 50),
('players.codemaster_glove_05', 300), ('players.codemaster_glove_05', 200), ('players.codemaster_glove_05', 100), ('players.codemaster_glove_05', 50),
('players.codemaster_glove_07', 300), ('players.codemaster_glove_07', 200), ('players.codemaster_glove_07', 100), ('players.codemaster_glove_07', 50),
('players.codemaster_w2vglove_03', 300), ('players.codemaster_w2vglove_03', 200), ('players.codemaster_w2vglove_03', 100), ('players.codemaster_w2vglove_03', 50),
('players.codemaster_w2vglove_05', 300), ('players.codemaster_w2vglove_05', 200), ('players.codemaster_w2vglove_05', 100), ('players.codemaster_w2vglove_05', 50),
('players.codemaster_w2vglove_07', 300), ('players.codemaster_w2vglove_07', 200), ('players.codemaster_w2vglove_07', 100), ('players.codemaster_w2vglove_07', 50)]

for cm in c:
    if cm[1] == 300:
        print(cm)
