import time
import json

from game import Game
from players.codemaster_glove_07 import AICodemaster as cm_glv07
from players.guesser_glove import AIGuesser as g_glv
from players.vector_codemaster import VectorCodemaster
from players.vector_guesser import VectorGuesser
from players.codemaster_w2vglove_07 import AICodemaster as cm_w2vglv07
from players.guesser_w2vglove import AIGuesser as g_w2vglv

class SharingExample:
    """Example of how to share vectors, pass kwargs, and call Game directly instead of by terminal"""

    start_time = time.time()
    glove_50d = Game.load_glove_vecs("players/glove.6B.50d.txt")
    print(f"{time.time() - start_time:.2f}s to load glove50d")

    start_time = time.time()
    glove_100d = Game.load_glove_vecs("players/glove.6B.100d.txt")
    print(f"{time.time() - start_time:.2f}s to load glove100d")

    start_time = time.time()
    w2v = Game.load_w2v("players/GoogleNews-vectors-negative300.bin")
    print(f"{time.time() - start_time:.2f}s to load w2v")

    print("\nclearing results folder...\n")
    Game.clear_results()

    seed = 0

    #
    print("starting original glove_glove game")
    cm_kwargs = {"glove_vecs": glove_100d}
    g_kwargs = {"glove_vecs": glove_50d}
    Game(cm_glv07, g_glv, seed=seed, do_print=False,  game_name="glv07-glv", cm_kwargs=cm_kwargs, g_kwargs=g_kwargs).run()

    print("starting VectorCodemaster/VectorGuesser glove-glove game")
    cm_kwargs = {"vectors": [glove_100d], "distance_threshold": 0.7, "same_clue_patience": 1, "max_red_words_per_clue": 3}
    g_kwargs = {"vectors": [glove_50d]}
    Game(VectorCodemaster, VectorGuesser, seed=seed, do_print=False,  game_name="vectorglv07-vectorglv", cm_kwargs=cm_kwargs, g_kwargs=g_kwargs).run()

    #
    print("starting original glovew2v-glovew2v game")
    cm_kwargs = {"glove_vecs": glove_50d,  "word_vectors": w2v}
    g_kwargs = {"glove_vecs": glove_50d,  "word_vectors": w2v}
    Game(cm_w2vglv07, g_w2vglv, seed=seed, do_print=False,  game_name="w2vglv07-w2vglv", cm_kwargs=cm_kwargs, g_kwargs=g_kwargs).run()

    print("starting VectorCodemaster/VectorGuesser glovew2v-glovew2v game")
    cm_kwargs = {"vectors": [w2v, glove_50d], "distance_threshold": 0.7, "same_clue_patience": 1, "max_red_words_per_clue": 3}
    g_kwargs = {"vectors": [w2v, glove_50d]}
    Game(VectorCodemaster, VectorGuesser, seed=seed, do_print=False,  game_name="vectorw2vglv07-vectorw2vglv", cm_kwargs=cm_kwargs, g_kwargs=g_kwargs).run()

    #
    print("starting VectorCodemaster/VectorGuesser gloveglovew2v-gloveglovew2v game")
    cm_kwargs = {"vectors": [w2v, glove_50d, glove_100d], "distance_threshold": 0.7, "same_clue_patience": 1, "max_red_words_per_clue": 3}
    g_kwargs = {"vectors": [w2v, glove_50d, glove_100d]}
    Game(VectorCodemaster, VectorGuesser, seed=seed, do_print=False,  game_name="vectorw2vglvglv07-vectorw2vglvglv", cm_kwargs=cm_kwargs, g_kwargs=g_kwargs).run()

    # display the results
    print(f"\nfor seed {seed} ~")
    with open("results/bot_results_new_style.txt") as f:
        for line in f.readlines():
            game_json = json.loads(line.rstrip())
            game_name = game_json["game_name"]
            game_time = game_json["time_s"]
            game_score = game_json["total_turns"]

            print(f"time={game_time:.2f}, turns={game_score}, name={game_name}")


if __name__ == "__main__":
    SharingExample()
