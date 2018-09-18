import game
import codemaster
import guesser

# must use python3 when running 
if __name__ == "__main__":

    game.main()
    game.random_map_generation()
    string_win_condition = "Hit_Red"
    #game .run()
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





