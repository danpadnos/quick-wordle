import json
import math
from collections import defaultdict
from functools import lru_cache
from multiprocessing import Pool
from time import monotonic

from wordle_game import WordleGame
from wordle_patterns import observe_pattern


with open('puzzle_words.json', 'r') as f:
    _puzzle_words = json.load(f)
with open('valid_words.json', 'r') as f:
    _valid_words = json.load(f)


def _make_guess2pattern2secrets(valid_words, puzzle_words):
    print("calculating guess2pattern2secrets.... ")
    start_time = monotonic()
    guess2pattern2secrets = {}
    for guess in valid_words:
        pat2sec = defaultdict(set)
        for secret in puzzle_words:
            pat2sec[observe_pattern(guess, secret)].add(secret)
        guess2pattern2secrets[guess] = pat2sec
    end_time = monotonic()
    print(f"done in {end_time - start_time:.2f} seconds")
    return guess2pattern2secrets


_guess2pattern2secrets = _make_guess2pattern2secrets(_valid_words, _puzzle_words)


@lru_cache(maxsize=100)
def calc_entropy(guess: str, allowed_words: frozenset):
    pattern2prob = {}
    num_allowed = len(allowed_words)
    for pattern, secrets in _guess2pattern2secrets[guess].items():
        num_options = len(secrets & allowed_words)
        if num_options > 0:
            pattern2prob[pattern] = num_options / num_allowed
    return -1 * sum(prob * math.log(prob) for prob in pattern2prob.values())


@lru_cache(maxsize=100)
def max_entropy_guess(remaining_puzzle_words: frozenset):
    guess2entropy = {
        guess: calc_entropy(guess, remaining_puzzle_words) for guess in _guess2pattern2secrets.keys()
    }
    guess, entropy = max(guess2entropy.items(), key=lambda kv: kv[1])
    return guess, entropy


def play_game(game):
    remaining_puzzle_words = frozenset(_puzzle_words)

    while game.status() == 'playing':
        if len(remaining_puzzle_words) == 1:
            game.play_turn(list(remaining_puzzle_words)[0])
            break

        # pick max entropy of valid word given remaining words
        guess, entropy = max_entropy_guess(remaining_puzzle_words)

        # play turn and update remaining words
        pattern = game.play_turn(guess)
        remaining_puzzle_words &= _guess2pattern2secrets[guess][pattern]

    return game.status() == 'won', len(game.turns)


if __name__ == '__main__':
    start_time = monotonic()
    print(f"starting benchmark on {len(_puzzle_words):d} puzzle words...")

    with Pool(8) as p:
        results = p.map(play_game, (WordleGame(max_turns=6, secret_word=w) for w in _puzzle_words))

    end_time = monotonic()
    print(f"done in {end_time - start_time:.2f} seconds")
    print("=" * 20)
    print(f"total games: {len(results):d}")
    print(f"successful games: {sum(won for won, _ in results)}")
    print(f"average turns in successful games: {sum(turns for won, turns in results if won) / len(results):.2f}")
