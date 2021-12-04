import sys
import importlib
import argparse
import time
import os

from game import Game
from players.guesser import *
from players.codemaster import *

class GameRun:
    """Class that builds and runs a Game based on command line arguments"""

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Run the Codenames AI competition game.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("redcodemaster", help="import string of form A.B.C.MyClass or 'human'")
        parser.add_argument("redguesser", help="import string of form A.B.C.MyClass or 'human'")

        parser.add_argument("bluecodemaster", help="import string of form A.B.C.MyClass or 'human'")
        parser.add_argument("blueguesser", help="import string of form A.B.C.MyClass or 'human'")

        parser.add_argument("--seed", help="Random seed value for board state -- integer or 'time'", default='time')

        parser.add_argument("--w2v", help="Path to w2v file or None", default=None)
        parser.add_argument("--glove", help="Path to glove file or None", default=None)
        parser.add_argument("--wordnet", help="Name of wordnet file or None, most like ic-brown.dat", default=None)
        parser.add_argument("--glove_cm", help="Path to glove file or None", default=None)
        parser.add_argument("--glove_guesser", help="Path to glove file or None", default=None)

        parser.add_argument("--no_log", help="Suppress logging", action='store_true', default=False)
        parser.add_argument("--no_print", help="Suppress printing", action='store_true', default=False)
        parser.add_argument("--game_name", help="Name of game in log", default="default")

        parser.add_argument("--pause", help="Pause the game after every turn", default=False)

        args = parser.parse_args()

        self.pause = args.pause

        self.do_log = not args.no_log
        self.do_print = not args.no_print
        if not self.do_print:
            self._save_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')
        self.game_name = args.game_name

        self.g_kwargs = {}
        self.cm_kwargs = {}

        # load codemaster classes
        if args.redcodemaster == "human":
            self.redcodemaster = HumanCodemaster
            print('human red codemaster')
        else:
            self.redcodemaster = self.import_string_to_class(args.redcodemaster)
            print('loaded red codemaster class')

        if args.bluecodemaster == "human":
            self.bluecodemaster = HumanCodemaster
            print('human blue codemaster')
        else:
            self.bluecodemaster = self.import_string_to_class(args.bluecodemaster)
            print('loaded blue codemaster class')

        # load guesser class
        if args.redguesser == "human":
            self.redguesser = HumanGuesser
            print('human red guesser')
        else:
            self.redguesser = self.import_string_to_class(args.redguesser)
            print('loaded red guesser class')

        if args.blueguesser == "human":
            self.blueguesser = HumanGuesser
            print('human blue guesser')
        else:
            self.blueguesser = self.import_string_to_class(args.blueguesser)
            print('loaded blue guesser class')

        # if the game is going to have an ai, load up word vectors
        if sys.argv[1] != "human" or sys.argv[2] != "human":
            if args.wordnet is not None:
                brown_ic = Game.load_wordnet(args.wordnet)
                self.g_kwargs["brown_ic"] = brown_ic
                self.cm_kwargs["brown_ic"] = brown_ic
                print('loaded wordnet')

            if args.glove is not None:
                glove_vectors = Game.load_glove_vecs(args.glove)
                self.g_kwargs["glove_vecs"] = glove_vectors
                self.cm_kwargs["glove_vecs"] = glove_vectors
                print('loaded glove vectors')

            if args.w2v is not None:
                w2v_vectors = Game.load_w2v(args.w2v)
                self.g_kwargs["word_vectors"] = w2v_vectors
                self.cm_kwargs["word_vectors"] = w2v_vectors
                print('loaded word vectors')

            if args.glove_cm is not None:
                glove_vectors = Game.load_glove_vecs(args.glove_cm)
                self.cm_kwargs["glove_vecs"] = glove_vectors
                print('loaded glove vectors')

            if args.glove_guesser is not None:
                glove_vectors = Game.load_glove_vecs(args.glove_guesser)
                self.g_kwargs["glove_vecs"] = glove_vectors
                print('loaded glove vectors')

        # set seed so that board/keygrid can be reloaded later
        if args.seed == 'time':
            self.seed = time.time()
        else:
            self.seed = int(args.seed)

    def __del__(self):
        """reset stdout if using the do_print==False option"""
        if not self.do_print:
            sys.stdout.close()
            sys.stdout = self._save_stdout

    def import_string_to_class(self, import_string):
        """Parse an import string and return the class"""
        parts = import_string.split('.')
        module_name = '.'.join(parts[:len(parts) - 1])
        class_name = parts[-1]

        module = importlib.import_module(module_name)
        my_class = getattr(module, class_name)

        return my_class


if __name__ == "__main__":
    game_setup = GameRun()

    game = Game(game_setup.redcodemaster,
                game_setup.redguesser,
                game_setup.bluecodemaster,
                game_setup.blueguesser,
                game_setup.pause,
                seed=game_setup.seed,
                do_print=game_setup.do_print,
                do_log=game_setup.do_log,
                game_name=game_setup.game_name,
                cm_kwargs=game_setup.cm_kwargs,
                g_kwargs=game_setup.g_kwargs)

    game.run()
