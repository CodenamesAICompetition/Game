import game


def get_board():

    game.display_board()
    game.display_map()


def give_clue():

    clue_input = input("Input CM Clue:\nPlease enter a Word followed by a space and a Number >> ")
    type(clue_input)

    clue = clue_input.split()
    return clue

