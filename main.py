#!/usr/bin/python3

import random


# Card with a suit and rank
class Card:
    suits = ["heart", "club", "spade", "diamond"]
    values = [str(v) for v in range(2, 11)] + ["jack", "queen", "king", "ace"]

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank.title()} of {self.suit}s"


# List of 52 playing cards each represented once
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


# List of 5 cards that can be checked for combinations
class Combo:
    def __init__(self, cards):
        assert len(cards) == 5
        self.cards = cards

    def __str__(self):
        result = ""
        for card in self.cards:
            result += str(card) + "\n"
        return result

    def check(self):
        # if all the suits are the same
        status = True
        for card in self.cards:
            if not self.cards[0].suit == card.suit:
                status = False

        print(status)


def print_cards(cards):
    for card in cards:
            print(card)


def main():
    # Create the deck
    d = Deck()
    d.shuffle()

    # deal 5 random cards
    current_cards = []
    for i in range(5):
        current_cards.append(d.deal())

    current_cards = [Card("heart", "jack"),Card("heart", "7"), Card("diamond", "4"), Card("heart", "2"), Card("heart", "9")]
    c = Combo(current_cards)
    c.check()

if __name__ == "__main__":
    main()
