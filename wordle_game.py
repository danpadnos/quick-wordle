from wordle_patterns import observe_pattern, WIN_PATTERN


class GameOverError(Exception):
    pass


class WordleGame:
    def __init__(self, max_turns, secret_word):
        self.max_turns = max_turns
        self.turns = []
        self.secret_word = secret_word

    def play_turn(self, guess):
        if self.status() != 'playing':
            raise GameOverError

        pattern = observe_pattern(guess, self.secret_word)
        self.turns.append((guess, pattern))

        return pattern

    def status(self):
        if self.turns and self.turns[-1][-1] == WIN_PATTERN:
            return 'won'
        elif len(self.turns) == self.max_turns:
            return 'lost'
        else:
            return 'playing'
