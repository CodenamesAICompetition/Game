# Codenames AI Competition Framework

This is the Codenames AI Competition Framework.  The purpose of this framework is to enable an AI competition for the game "Codenames" by Vlaada Chvatil.  There are large number of AI competitions built around games (and even more platforms using games as a testbed for AI), but with few exceptions these have focused on things that AI is likely to be good at (fine, pixel-perfect control or search through a large state space).  The purpose of this competition is to test AI in a framework that:

* Requires the understanding of language
* Requires communication, in a semantically meaningful way, with players of unknown provenance --  the player on the other side of the table may be a human or it may be another, unaffiliated, bot
* Requires understanding words with multiple meanings

## Submissions

Entrants in the competition will be able to submit up to two bots (at most 1 Codemaster and 1 Guesser)

### Running the game and Terminal instructions
To run the following game, the terminal will require a certain amount of arguments. 
Where the order is:
* args[0] = game.py
* args[1] = codemaster package
* args[2] = guesser package

Optionally if certain word vectors are needed, the directory to which should be specified in the arguments here.
3 argument parsers have been provided:
* --w2v path/to/word_vectors
* --wordnet ic-brown.dat or ic-semcor.dat
* --glove path/to/glove_vectors

An optional seed argument can be used for the purpose of consistency against the random library.
* --seed *Integer value*

An example simulation of a *wordnet codemaster* and a *word2vec guesser* in the terminal:  
`$ python game.py players.codemaster_wn_lin players.guesser_w2v --seed 3442 --w2v players/GoogleNews-vectors-negative300.bin  --wordnet ic-brown.dat`

### Codemaster
The Codemaster bot is a python 3 class that derives from the supplied `codemaster.py`.  The bot must make use of the two functions:
`__init__(self, brown_ic=None, glove_vecs=None, word_vectors=None)`


`receive_game_state(words : List[Str], map : List[Str]) -> None`

and

`give_clue() -> Tuple[Str,int]`

'__init__' is given 3 initially empty datasets by default (to reduce load times for common NLP resources), argument values that hold directories of word vectors get passed through here. The Brown Corpus from NLTK, 300 dimensional GloVe vectors, and the pretrained 300 dimensional pre-trained Google NewsNewsBin word2vec vectors are commonly used here.

`receive_game_state` is passed the list of words on the board, as well as the map of hidden information.  The `words` are either: an all upper case word found in the English language or one of 4 special tokens: `'*Red*', '*Blue*', '*Civilian*', '*Assassin*'` indicating that the word that was originally at that location has been guessed and been found to be of that type.  The `hidden_map` is a list of `'*Red*', '*Blue*', '*Civilian*', '*Assassin*'` indicating whether a spot on the board is on the team of the codemaster (`'*Red*'`), the opposing team (`'*Blue*'`), a civilian (`'*Civilian*'`), or the assassin (`'*Assassin*'`).


`give_clue` returns a tuple containing the clue, a single English word, and the number of words the Codemaster intends it to cover.  

### Guesser

The Guesser bot is a python 3 class that derives from the supplied `guesser.py`.  The bot must make use of the four functions:

`__init__(self, brown_ic=None, glove_vecs=None, word_vectors=None)`

`get_board(words: List[str]) -> None`

`get_clue(clue:Str, guesses:int) -> None`

`keep_guessing -> bool`

and


`give_answer() -> Str`

`__init__` is as above with the codemaster.

`get_board` is passed the list of words on the board.  The `words` are either: an all upper case word found in the English language or one of 4 special tokens: `'*Red*', '*Blue*', '*Civilian*', '*Assassin*'` indicating that the word that was originally at that location has been guessed and been found to be of that type.

`get_clue` is passed the clue and the number of guesses it covers, as supplied by the `give_clue` of the codemaster.

`keep_guessing` is a function that the game engine checks to see if the bot chooses to keep guessing, as the bot must only make at least one guess, but may choose to guess until it has gone to the number supplied by get_clue + 1.

`give_answer` returns the current guess of the Guesser, given the state of the board and the previous clue.



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

Competition rules have not been fully settled yet.

## Prerequisite: Installation and Downloads
Note: The use of [Anaconda3](https://www.anaconda.com/distribution/) must be used for certain dependencies to work without issues. Also installing NLTK and gensim through conda is simpler and less time consuming.

Installation of NLTK on macOS/linux:
* Install python3 on your operation system. If python 2 and python 3 coexists in your Operating System than you must specify `python3` for your commands.
* For macOS users, who don't have `pip3` or `python3` recognized in terminal, simply open terminal and type in `brew install python3` and check to see if `pip3` is a recognized command. If it is move on to the next step, if not type `brew postinstall python3`
* Type in `sudo pip3 install -U nltk`
* Finally type in terminal (this installs wordnet):
```
python
>>> import nltk
>>> nltk.download('all')
```
Installation of NLTK on Windows:
* Head over to the [nltk website](https://pypi.org/project/nltk/#files)
* Download the nltk file from the above link
* Start a terminal and change into the nltk directory
* Finally type in:
```
python setup.py install
```

* After the above steps create a python file called "set.py"
* Add these 2 lines of code:
```
import nltk
nltk.download('all')
```
* Then run the program by typing "python set.py"
* Nltk should now be installed

Installing Gensim:

* For windows, using anaconda:
```conda install gensim```

* For macOS, using easy_install or anaconda(same as above):
```sudo easy_install --upgrade gensim```

### These files should be installed as well, place them under your codenames/players/ directory:
* https://nlp.stanford.edu/data/glove.6B.zip (~2.25 GB)
* https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit (~3.5 GB)
