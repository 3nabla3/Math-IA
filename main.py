#!/usr/bin/python3

import random

class Card:
    suits = ["heart", "club", "spade", "diamond"]
    values = [str(v) for v in range(2, 11)] + ["jack", "queen", "king", "ace"]

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value.title()} of {self.suit}s"


class Deck:
    def __init__(self):
        self.cards = [
            Card(suit, value) for suit in Card.suits for value in Card.values
        ]

    def __str__(self):
        result = ""
        for card in self.cards:
            result += str(card) + "\n"
        return result

    @property
    def size(self):
        return len(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()


def print_cards(cards):
    for card in cards:
        print(card)


class Player:
    def __init__(self, name, card1, card2):
        self.name  = name
        self.card1 = card1
        self.card2 = card2

    def __str__(self):
        result = f"{self.name}'s cards:\n"
        result += "-------------------\n"
        result += str(self.card1) + "\n"
        result += str(self.card2) + "\n"
        return result


def main():
    num_players = 5
    deck = Deck()
    deck.shuffle()

    common_cards = [deck.deal() for _ in range(5)]
    print("Common cards:")
    print("-------------------")
    print_cards(common_cards)
    print()
    print()

    players = [Player(f"Player {i}",deck.deal(), deck.deal())for i in range(num_players)]
    for player in players:
        print(player)

if __name__ == "__main__":
    main()
