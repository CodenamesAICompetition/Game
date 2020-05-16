# Codenames AI Competition Framework

This is the Codenames AI Competition Framework.  The purpose of this framework is to enable an AI competition for the game "Codenames" by Vlaada Chvatil.  There are large number of AI competitions built around games (and even more platforms using games as a testbed for AI), but with few exceptions these have focused on things that AI is likely to be good at (fine, pixel-perfect control or search through a large state space).  The purpose of this competition is to test AI in a framework that:

* Requires the understanding of language
* Requires communication, in a semantically meaningful way, with players of unknown provenance --  the player on the other side of the table may be a human or it may be another, unaffiliated, bot
* Requires understanding words with multiple meanings

**Further installation requirements are found below.**

## Submissions

Entrants in the competition will be able to submit up to two bots (at most 1 Codemaster and 1 Guesser)

## Running the game from terminal instructions

To run the game, the terminal will require a certain amount of arguments.
Where the order is:
* args[0] = run_game.py
* args[1] = package.MyCodemasterClass
* args[2] = package.MyGuesserClass

**run_game.py simply handles system arguments then called game.Game().
See below for more details about calling game.Game() directly.**

Optionally if certain word vectors are needed, the directory to which should be specified in the arguments here.
5 argument parsers have been provided:
* --w2v *path/to/word_vectors*
  * (to be loaded by gensim)
* --glove *path/to/glove_vectors*
  *  (in stanford nlp format)
* --wordnet ic-brown.dat or ic-semcor.dat
  * (nltk corpus filename)

* --glove_cm *path/to/glove_vectors*
  * (legacy argument for glove_glove.py)
* --glove_guesser *path/to/glove_vectors*
  * (legacy argument for glove_glove.py)

An optional seed argument can be used for the purpose of consistency against the random library.
* --seed *Integer value* or "time"
  * ("time" uses Time.time() as the seed)

Other optional arguments include:
* --no_log
  * raise flag for suppressing logging
* --no_print
  * raise flag for suppressing printing to std out
* --game_name *String*
  * game_name in logfile

An example simulation of a *wordnet codemaster* and a *word2vec guesser* in the terminal from codenames/:  
`$ python run_game.py players.codemaster_wn_lin.AICodemaster players.guesser_w2v.AIGuesser --seed 3442 --w2v players/GoogleNews-vectors-negative300.bin  --wordnet ic-brown.dat`

An example of running glove codemaster and glove guesser with different glove vectors (removed glove_glove.py)
`$ python run_game.py players.codemaster_glove_07.AICodemaster players.guesser_glove.AIGuesser --seed 3442 --glove_cm players/glove.6B.50d.txt --glove_guesser players/glove.6B.100d.txt`

## Running the game from calling Game(...).run()

The class Game() that can be imported from game.Game is the main framework class.

An example of calling generalized vector codemaster and guesser from python code rather than command line
```
    cm_kwargs = {"vectors": [w2v, glove_50d, glove_100d], "distance_threshold": 0.3, "same_clue_patience": 1, "max_red_words_per_clue": 3}
    g_kwargs = {"vectors": [w2v, glove_50d, glove_100d]}
    Game(VectorCodemaster, VectorGuesser, seed=0, do_print=False,  game_name="vectorw2vglvglv03-vectorw2vglvglv", cm_kwargs=cm_kwargs, g_kwargs=g_kwargs).run()
```

See simple_example.py for an example of sharing word vectors,
passing kwargs to guesser/codemaster through Game,
and calling Game.run() directly.

## Game Class

The main framework class that calls your AI bots.

As mentioned above, a Game can be created/played directly by importing game.Game,
initializing with the args below, and calling the run() method.

```
Class that setups up game details and 
calls Guesser/Codemaster pair to play the game

Args:
    codemaster (:class:`Codemaster`):
        Codemaster (spymaster in Codenames' rules) class that provides a clue.
    guesser (:class:`Guesser`):
        Guesser (field operative in Codenames' rules) class that guesses based on clue.
    seed (int or str, optional): 
        Value used to init random, "time" for time.time(). 
        Defaults to "time".
    do_print (bool, optional): 
        Whether to keep on sys.stdout or turn off. 
        Defaults to True.
    do_log (bool, optional): 
        Whether to append to log file or not. 
        Defaults to True.
    game_name (str, optional): 
        game name used in log file. Defaults to "default".
    cm_kwargs (dict, optional): 
        kwargs passed to Codemaster.
    g_kwargs (dict, optional): 
        kwargs passed to Guesser.
```

## Codemaster Class
Any Codemaster bot is a python 3 class that derives from the supplied abstract base class Codemaster in `codemaster.py`.  The bot must implement three functions:
```
__init__(self)
set_game_state(words_on_board : List[str], key_grid : List[str]) -> None
get_clue() -> Tuple[str,int]
```
#### *details*

'__init__' **kwargs are passed through (can be used to pass pre-loaded word vectors to reduce load times for common NLP resources).  Some common examples are the Brown Corpus from NLTK's wordnet, the multi-dimensional GloVe vectors, and the 300 dimensional pre-trained Google NewsNewsBin word2vec vectors.

`set_game_state` is passed the list of words on the board, as well as the key grid provided to spymasters (codemasters).  The `words` are either: an all upper case word found in the English language or one of 4 special tokens: `'*Red*', '*Blue*', '*Civilian*', '*Assassin*'` indicating that the word that was originally at that location has been guessed and been found to be of that type.  The `key_grid` is a list of `'*Red*', '*Blue*', '*Civilian*', '*Assassin*'` indicating whether a spot on the board is on the team of the codemaster (`'*Red*'`), the opposing team (`'*Blue*'`), a civilian (`'*Civilian*'`), or the assassin (`'*Assassin*'`).


`get_clue` returns a tuple containing the clue, a single English word, and the number of words the Codemaster intends it to cover.

## Guesser Class

Any Guesser bot is a python 3 class that derives from the supplied abstract base class Guesser in `guesser.py`.  The bot must implement four functions:

```
__init__(self)
set_board(words: List[str]) -> None
set_clue(clue: str, num_guesses: int) -> None
keep_guessing -> bool
get_answer() -> Str
```

#### *details*

`__init__` is as above with the codemaster.

`set_board` is passed the list of words on the board.  The `words` are either: an all upper case word found in the English language or one of 4 special tokens: `'*Red*', '*Blue*', '*Civilian*', '*Assassin*'` indicating that the word that was originally at that location has been guessed and been found to be of that type.

`set_clue` is passed the clue and the number of guesses it covers, as supplied by the `get_clue` of the codemaster through the Game class.

`keep_guessing` is a function that the game engine checks to see if the bot chooses to keep guessing, as the bot must only make at least one guess, but may choose to guess until it has gone to the number supplied by get_clue + 1.

`get_answer` returns the current guess of the Guesser, given the state of the board and the previous clue.



## Rules of the Game

Codenames is a game of language understanding and communication.  The competition takes place in a single team style of play -- The Codemaster and Guesser are both on the Red team, and their goal is to discover their words as quickly as possible, while minimizing the number of incorrect guesses.

At the start of the game, the board consists of 25 English words:

DAY SLIP SPINE WAR CHICK
FALL HAND WALL AMAZON DEGREE
GIANT CENTAUR CLOAK STREAM CHEST
HAM DOG EMBASSY GRASS FLY
CAPITAL OIL COLD HOSPITAL MARBLE

The Codemaster has access to a hidden map that tells them the identity of all of the words:

*Red* *Red* *Civilian* *Assassin* *Red*
*Red* *Civilian* *Red* *Civilian* *Civilian*
*Civilian* *Civilian* *Civilian* *Blue* *Civilian*
*Red* *Civilian* *Red* *Red*

Meaning that the words that Codemaster wants their teammate to guess are:

DAY, SLIP, CHICK, FALL, WALL, CAPITAL, HOSPITAL, MARBLE

The Codemaster then supplies a clue and a number (the number of guesses the Guesser is obligated to make):

e.g., `('pebble',2)`

The clue must:
* Be semantically related to what the Codemaster wants their guesser to guess -- no using words to tell the position of the words
* Be a single English word
* NOT be derived from or derive one of the words on the board -- i.e. days or cloaked are not valid clues

The guesser then returns a list of their guesses, in order of importance:

e.g. `['MARBLE', 'STREAM']`

This would result in them guessing 1 word correctly -- MARBLE -- and guessing one that is linked to a civilian -- STREAM.  If instead the guesser had guessed:

`['STREAM', 'MARBLE']`

Then the result would be in 1 incorrect guess -- STREAM -- and their turn would have ended at that point.  It is important for the guesser to correctly order their guesses, as ordering is important.

If a guesser guesses an invalid clue, their turn is forfeit.

Play proceeds, passing back and forth, until one of 3 outcomes is achieved:

* All of the Red tiles have been found -- the team wins
* All of the Blue tiles have been found -- the team loses
* The single *Assassin* tile is found -- the team loses

## Competition Rules

Competition results will be scored by the number of turns required to guess all 8 red words. Scores will be calculated in an inverse proportional fashion, so the lower the better. 

* The average number of turns the codemaster/guesser takes will be the score given to each paired bot.
* Guessing an assassin-linked word or the 7 blue words before all 8 red words will result in an instant loss and a score of 25 turns or points.

Codemaster bots will be swapped and trialed with multiple guessers and conversely guesser bots will be swapped with codemasters to ensure and maximize variability and fairness.

In other words you'll be paired up with other player's bots, and scored/tested to see how well your AI can perform within a more general context of Natural Language Understanding.

## Prerequisite: Installation and Downloads
Note: The installation of the [Anaconda Distribution](https://www.anaconda.com/distribution/) should be used for certain dependencies to work without issues. Also installing NLTK and gensim through conda is much simpler and less time consuming than the below alternatives.

Example installation order:
```
(base) conda create --name codenames python=3.6
(base) conda activate codenames
(codenames) conda install gensim
(codenames) pip install -U gensim
(codenames) pip install -U nltk
(codenames) python
>>> import nltk
>>> nltk.download('all')
>>> exit()
(codenames) pip install -U colorama
(codenames) git clone https://github.com/CodenamesAICompetition/Game.git
(codenames) cd codenames
```

Alternatively you can use your system's packaging system. (*apt-get* on Debian, or *MacPorts/Homebrew* on macOS)
Or just use Python's packaging system, pip3, which is included by default from the Python binary installer.

To check that everything is installed without error type in a terminal:  
`$ python3 -c "import scipy, numpy, gensim.models.keyedvectors, argparse, importlib, nltk, nltk.corpus, nltk.stem"`

Installing Gensim:

* Using Anaconda:
```conda install gensim```

* For Windows User using Conda Prompt(as well as the command on top):
```pip install -U gensim```

* For macOS, using Anaconda(same as above) or easy_install:
```sudo easy_install --upgrade gensim```

Installation of NLTK on macOS/linux:
* Install python3 on your operation system. If python 2 and python 3 coexists in your Operating System than you must specify `python3` for your commands.
* For macOS users, who don't have `pip3` or `python3` recognized in terminal, simply open terminal and type in `brew install python3` and check to see if `pip3` is a recognized command. If it is move on to the next step, if not type `brew postinstall python3`, or alternatively visit the [Python](https://python.org) website.
* Type in `sudo pip3 install -U nltk`
* Finally type in terminal (this installs all nltk packages, as opposed to a select few):
```
python
>>> import nltk
>>> nltk.download('all')
```

*Note for Windows user: Use the conda bash prompt for general purpose testing/running (as opposed to git bash)*

Installation of NLTK on Windows:
```pip install -U nltk```
```
python
>>> import nltk
>>> nltk.download('all')
```

Install colorama for colored console output:
```pip install -U colorama```


### These files can optionally be installed as well, provide path through command arguments:
* [Glove Vectors](https://nlp.stanford.edu/data/glove.6B.zip) (~2.25 GB)
* [Google News Vectors](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit) (~3.5 GB)
