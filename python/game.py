import random
import codemaster
import guesser
import array

# https://codeshare.io/aJgPVZ
# must use python3 when running on terminal
def main():

    # open the text file for random selection - readonly
    f = open("CNWordList.txt", "r")

    # if successfully opened split and randomly generate 25 words
    if f.mode == 'r':

        global words
        # contains all words from text file as an array
        temp_array = f.read().splitlines()
        words = set([])
        # initialize the set words randomly
        for x in range(0, 25):
            words.add(random.choice(temp_array))

        # if duplicates were detected and the set length is not 25 then restart
        if len(words) != 25:
            main()

        # initialize back as a list
        words = list(words)

def random_map_generation():

    global map
    map = ["Red"]*8 + ["Blue"]*7 + ["Civilian"]*9 + ["Assassin"]
    random.shuffle(map)


def display_board():

    print(str.center("___________________________BOARD___________________________", 60))

    for i in range(len(words)):
        # newline for every 5 prints
        if i % 5 == 0:
            print("\n")
        # centers the output
        print(str.center(words[i], 10), " ", end='')

    print(str.center("\n___________________________________________________________", 60))

    print("\n")


def display_map():

    print("\n")
    print(str.center("____________________________MAP____________________________", 55))

    for i in range(len(map)):
        # newline for every 5 prints
        if i % 5 == 0:
            print("\n")
        # centers the output
        print(str.center(map[i], 10), " ", end='')

    print(str.center("\n___________________________________________________________", 55))

    print("\n")


def list_words():

    return words


# takes in an int index called guess to compare with the Map
def accept_guess(guess_index):

    # CodeMaster will always win with Red and lose with Blue or Assassin
    if map[guess_index] == "Red":

        if words.count("*Red*") >= 8:

            return "Win"

        words[guess_index] = "*Red*"
        return "Hit_Red"

        
    elif map[guess_index] == "Blue":

        words[guess_index] = "*Blue*"

        if words.count("*Blue*") >= 7:

            return "Lose"
            
        else:

            return "Still Going"

    elif map[guess_index] == "Assassin":

        words[guess_index] = "*Assassin*"
        return "Lose"

    else:
        words[guess_index] = "*Civilian*"
        return "Still Going"


def run():
    
    print("========================GAME START========================\n")

    while(string_win_condition != "Lose" or string_win_condition != "Win"):

        words_in_play = game.list_words()

        codemaster.get_board()
        clue, num = codemaster.give_clue()
        num = int(num)

        guesser.get_clue(clue)

        string_win_condition = "Hit_Red"

        while(string_win_condition == "Hit_Red" and num >= 0):

            num -= 1
            guesser.get_board()

            guess_answer = guesser.give_answer(words_in_play)

            guess_answer_index = words_in_play.index(guess_answer.upper())

            string_win_condition = game.accept_guess(guess_answer_index)

            game.display_board()


            # add score tracker here
            if string_win_condition == "Hit_Red":
                string_win_condition = "Hit_Red"

            elif string_win_condition == "Still Going":
                break

            elif string_win_condition == "Lose":
                print("You Lose")
                break

            elif string_win_condition == "Win":
                print("You Won")
                break



if __name__ == "__main__":

    main()
    random_map_generation()
    global string_win_condition
    string_win_condition = "Hit_Red"
    run()


