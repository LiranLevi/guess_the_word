import argparse
import random
import csv
from typing import List, Dict


def load_words(file_path: str, limit: int = 0) -> List:
    category_word_pairs = []
    with open(file_path, 'r') as wfp:
        reader = csv.DictReader(wfp)
        for row in reader:
            category = row["category"].strip()
            word = row["word"].strip()

            if not category.isalpha() or not word.isalpha():
                print(f"Invalid characters in entry: {row}. Only English letters are allowed.")
                continue
            category_word_pairs.append((category.lower(), word.lower()))

    random_words = random.sample(category_word_pairs, len(category_word_pairs))

    return random_words[:min(limit, len(random_words))] if limit > 0 else random_words


def is_valid_guess(guessed_letter: str) -> bool:
    return len(guessed_letter) == 1 and guessed_letter.isalpha()


def play_game(words: List, players: List) -> Dict:
    players_scores = {}
    for player in players:
        players_scores[player] = 0

    for category, word in words:

        word = word.lower()
        hidden_word = ['_'] * len(word)
        guessed_letters_set = set()
        indexed_letters = list(enumerate(word))
        player_idx = 0

        while '_' in hidden_word:
            print(f"Category: {category}")
            print(f"Word: {''.join(hidden_word)}")
            print(f"Letters already tried: {sorted(guessed_letters_set)}")
            print(f"{players_scores}")
            player = players[player_idx]
            guessed_letter = input(f"{player}, Please enter your guess letter: ").strip().lower()

            if not is_valid_guess(guessed_letter):
                print("Invalid input. Please enter a single English letter.\n")
                continue

            if guessed_letter in guessed_letters_set:
                print("Letter already guessed. Try again.\n")
                continue

            guessed_letters_set.add(guessed_letter)

            if guessed_letter in word:
                points_counter = 0
                for idx, letter in indexed_letters:
                    if guessed_letter == letter:
                        hidden_word[idx] = guessed_letter
                        points_counter += 1
                players_scores[player] += points_counter
                print(f"It's correct guess! '{guessed_letter}' appears {points_counter} time(s) in the word.\n")
            else:
                print(f"It's wrong guess. '{guessed_letter}' doesn't appear in the word.\n")

            player_idx = (player_idx + 1) % len(players)

        print(f"The word is: '{word}'\n")

    return players_scores


def main():
    parser = argparse.ArgumentParser(prog="Guess The Word Game")
    parser.add_argument("filepath", type=str,
                        help="Path to the CSV file containing words")
    parser.add_argument("--wordslimit", type=int, default=0,
                        help="Limit the number of words for the game")
    parser.add_argument("--players", type=str, nargs='+',
                        help="Names of the players", required=True)

    args = parser.parse_args()

    words = load_words(args.filepath, args.wordslimit)
    players_scores = play_game(words, args.players)

    max_score = max(players_scores.values())

    game_winner = [player for player, score in players_scores.items() if score == max_score and max_score > 0]

    if len(game_winner) > 1:
        print(f"There is a winners in this game and the winners are: "
              f"{' and '.join(game_winner)} with {max_score} points each!")
    elif max_score > 0:
        print(f"The winner is: {game_winner[0]}, with {max_score} points!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)

