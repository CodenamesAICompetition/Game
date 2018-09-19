import game
import codemaster

class bot_guesser:

    def __init__():
        pass
    
    def get_clue(clue):

        print(clue)


    def get_board(board_list):

       #game.display_board()
       pass

    def give_answer(words):

        # answer input
        answer_input = input("Guesser:\nPlease enter a valid Word >> ")
        type(answer_input)

        while not is_valid(answer_input, words):
            print("Input Invalid")
            answer_input = input("Guesser:\nPlease enter a valid Word >> ")
            type(answer_input)

        return answer_input


    def is_valid(result, words):

        if result.upper() in words:
            return True

        else:
            return False