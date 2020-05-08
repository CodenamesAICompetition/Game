import time
import json
import io
import sys

from codenames.game import Game
from codenames.players.codemaster_glove_03 import AICodemaster as cm_glv03
from codenames.players.guesser_glove import AIGuesser as g_glv
from codenames.players.vector_codemaster import VectorCodemaster
from codenames.players.vector_guesser import VectorGuesser
from codenames.players.codemaster_w2vglove_03 import AICodemaster as cm_w2vglv03
from codenames.players.guesser_w2vglove import AIGuesser as g_w2vglv

class SharingExample:
    start_time = time.time()
    glove_50d = Game.load_glove_vecs("players/glove.6B.50d.txt")
    load1 = time.time() - start_time

    start_time = time.time()
    glove_100d = Game.load_glove_vecs("players/glove.6B.100d.txt")
    load2 = time.time() - start_time

    start_time = time.time()
    w2v = Game.load_w2v("players/GoogleNews-vectors-negative300.bin")
    load3 = time.time() - start_time

    Game.clear_results()

    text_trap = io.StringIO()
    sys.stdout = text_trap

    #
    cm_kwargs = {"glove_vecs": glove_100d}
    g_kwargs = {"glove_vecs": glove_50d}
    Game(cm_glv03, g_glv, seed=0, do_print=False,  game_name="glv03-glv", cm_kwargs=cm_kwargs, g_kwargs=g_kwargs).run()

    cm_kwargs = {"vectors": [glove_100d], "distance_threshold": 0.3, "same_clue_patience": 1, "max_red_words_per_clue": 3}
    g_kwargs = {"vectors": [glove_50d]}
    Game(VectorCodemaster, VectorGuesser, seed=0, do_print=False,  game_name="vectorglv03-vectorglv", cm_kwargs=cm_kwargs, g_kwargs=g_kwargs).run()

    #
    cm_kwargs = {"glove_vecs": glove_50d,  "word_vectors": w2v}
    g_kwargs = {"glove_vecs": glove_50d,  "word_vectors": w2v}
    Game(cm_w2vglv03, g_w2vglv, seed=0, do_print=False,  game_name="w2vglv03-w2vglv", cm_kwargs=cm_kwargs, g_kwargs=g_kwargs).run()

    cm_kwargs = {"vectors": [w2v, glove_50d], "distance_threshold": 0.3, "same_clue_patience": 1, "max_red_words_per_clue": 3}
    g_kwargs = {"vectors": [w2v, glove_50d]}
    Game(VectorCodemaster, VectorGuesser, seed=0, do_print=False,  game_name="vectorw2vglv03-vectorw2vglv", cm_kwargs=cm_kwargs, g_kwargs=g_kwargs).run()

    #
    cm_kwargs = {"vectors": [w2v, glove_50d, glove_100d], "distance_threshold": 0.3, "same_clue_patience": 1, "max_red_words_per_clue": 3}
    g_kwargs = {"vectors": [w2v, glove_50d, glove_100d]}
    Game(VectorCodemaster, VectorGuesser, seed=0, do_print=False,  game_name="vectorw2vglvglv03-vectorw2vglvglv", cm_kwargs=cm_kwargs, g_kwargs=g_kwargs).run()

    sys.stdout = sys.__stdout__

    print(load1, "s to load glove50d")
    print(load2, "s to load glove100d")
    print(load3, "s to load w2v")

    # display the results
    with open("results/bot_results_new_style.txt") as f:
        for line in f.readlines():
            game_json = json.loads(line.rstrip())
            game_name = game_json["game_name"]
            game_time = game_json["time_s"]
            game_score = game_json["total_turns"]

            print(game_time, game_score, game_name)



if __name__ == "__main__":
    SharingExample()