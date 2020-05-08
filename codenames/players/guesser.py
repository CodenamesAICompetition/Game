from abc import ABC, abstractmethod

class Guesser(ABC):
    """guesser abstract class that mimics a field operative in the codenames game"""

    def __init__(self):
        """Handle pretrained vectors and declare instance vars"""
        pass

    @abstractmethod
    def set_board(self, words_on_board):
        """Set function for the current game board"""
        pass

    @abstractmethod
    def set_clue(self, clue, num_guesses):
        """Set function for current clue and number of guesses this class should attempt"""
        pass

    @abstractmethod
    def keep_guessing(self):
        """Return True if guess attempts remaining otherwise False"""
        pass

    @abstractmethod
    def get_answer(self):
        """Return the top guessed word based on the clue and current game board"""
        pass


class HumanGuesser(Guesser):
    """Guesser derived class for human interaction"""

    def __init__(self):
        super().__init__()
        pass

    def set_clue(self, clue, num):
        print("The clue is:", clue, num)

    def set_board(self, words):
        self.words = words

    def get_answer(self):
        answer_input = input("Guesser makes turn.\nPlease enter a valid Word >> ")
        type(answer_input)

        while not self._is_valid(answer_input):
            print("Input Invalid")
            print(self.words)
            answer_input = input("Please enter a valid Word >> ")
            type(answer_input)
        return answer_input

    def keep_guessing(self):
        return True

    def _is_valid(self, result):
        if result.upper() in self.words:
            return True
        else:
            return False
