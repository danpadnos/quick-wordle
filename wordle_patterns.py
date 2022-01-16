from collections import Counter

GREEN = 'V'
YELLOW = '?'
GREY = 'X'
NUM_LETTERS = 5
WIN_PATTERN = NUM_LETTERS * GREEN


def observe_pattern(guess: str, secret: str):
    pattern = ''
    counts = Counter(secret)

    for g, s in zip(guess, secret):
        if g == s:
            pattern += GREEN
            counts[g] -= 1
        elif g in secret and counts[g] > 0:
            pattern += YELLOW
            counts[g] -= 1
        else:
            pattern += GREY

    return pattern
