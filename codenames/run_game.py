import sys
import importlib
import argparse
import time

from game import Game
from players.guesser import *
from players.codemaster import *

class GameRun():
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Run the Codenames AI competition game.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("codemaster", help="Path to codemaster package or 'human'")
        parser.add_argument("guesser", help="Path to guesser package or 'human'")
        parser.add_argument("--seed", help="Random seed value for board state -- integer or 'time'", default='time')

        parser.add_argument("--w2v", help="Path to w2v file or None", default=None)
        parser.add_argument("--glove", help="Path to glove file or None", default=None)
        parser.add_argument("--wordnet", help="Name of wordnet file or None, most like ic-brown.dat", default=None)
        parser.add_argument("--glove_cm", help="Path to glove file or None", default=None)
        parser.add_argument("--glove_guesser", help="Path to glove file or None", default=None)

        parser.add_argument("--no_log", help="Supress logging", action='store_true', default=False)
        parser.add_argument("--no_print", help="Supress printing", action='store_true', default=False)
        parser.add_argument("--game_name", help="Name of game in log", default="default")

        args = parser.parse_args()

        self.do_log = not args.no_log
        self.do_print = not args.no_print
        self.game_name = args.game_name

        self.g_kwargs = {}
        self.cm_kwargs = {}

        # load codemaster class
        if args.codemaster == "human":
            self.codemaster = HumanCodemaster()
            if self.do_print: print('human codemaster')
        else:
            codemaster_module = importlib.import_module(args.codemaster)
            self.codemaster = codemaster_module.AICodemaster
            if self.do_print: print('loaded codemaster class')

        # load guesser class
        if args.guesser == "human":
            self.guesser = HumanGuesser()
            if self.do_print: print('human guesser')
        else:
            guesser_module = importlib.import_module(args.guesser)
            self.guesser = guesser_module.AIGuesser
            if self.do_print: print('loaded guesser class')

        # if the game is going to have an ai, load up word vectors
        if sys.argv[1] != "human" or sys.argv[2] != "human":
            if args.wordnet is not None:
                brown_ic = Game.load_wordnet(args.wordnet)
                self.g_kwargs["brown_ic"] = brown_ic
                self.cm_kwargs["brown_ic"] = brown_ic
                if self.do_print: print('loaded wordnet')

            if args.glove is not None:
                glove_vectors = Game.load_glove_vecs(args.glove)
                self.g_kwargs["glove_vecs"] = glove_vectors
                self.cm_kwargs["glove_vecs"] = glove_vectors
                if self.do_print: print('loaded glove vectors')

            if args.w2v is not None:
                w2v_vectors = Game.load_w2v(args.w2v)
                self.g_kwargs["word_vectors"] = w2v_vectors
                self.cm_kwargs["word_vectors"] = w2v_vectors
                if self.do_print: print('loaded word vectors')

            if args.glove_cm is not None:
                glove_vectors = Game.load_glove_vecs(args.glove_cm)
                self.cm_kwargs["glove_vecs"] = glove_vectors
                if self.do_print: print('loaded glove vectors')

            if args.glove_guesser is not None:
                glove_vectors = Game.load_glove_vecs(args.glove_guesser)
                self.g_kwargs["glove_vecs"] = glove_vectors
                if self.do_print: print('loaded glove vectors')

        # set seed so that board/keygrid can be reloaded later
        if args.seed == 'time':
            self.seed = time.time()
        else:
            self.seed = int(args.seed)


if __name__ == "__main__":
    game_setup = GameRun()

    game = Game(game_setup.codemaster,
                game_setup.guesser,
                seed=game_setup.seed,
                do_print=game_setup.do_print,
                do_log=game_setup.do_log,
                game_name=game_setup.game_name,
                cm_kwargs=game_setup.cm_kwargs,
                g_kwargs=game_setup.g_kwargs)

    game.run()