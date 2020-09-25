#!/usr/bin/python3

import random


# Card with a suit and rank
class Card:
    suits = ["heart", "club", "spade", "diamond"]
    ranks = [str(v) for v in range(2, 11)] + ["jack", "queen", "king", "ace"]

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def _val(self):
        if self.rank == "jack": return 11
        if self.rank == "queen": return 12
        if self.rank == "king": return 13
        return int(self.rank)

    def __lt__(self, other):
        return self._val() < other._val()

    def __str__(self):
        return f"{self.rank.title()} of {self.suit}s"


# List of 52 playing cards each represented once
class Deck:
    def __init__(self):
        self.cards = [
            Card(suit, value) for suit in Card.suits for value in Card.ranks
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

    def same_suit(self):
        status = True
        for card in self.cards:
            if not self.cards[0].suit == card.suit:
                status = False

        print("Are all of the cards the same suit?")
        print("yes") if status else print("no")
        return status

    def in_order(self):
        status = True
        o = sorted(self.cards)
        status = self.cards == o

        print("Are the cards in order?")
        print("yes") if status else print("no")
        return status

    def check(self):
        # is it a straight / royal flush?
        if self.same_suit() and self.in_order():
            print("Is the highest card a king?")
            if sorted(self.cards)[-1].rank == "king":
                print("yes")
                return "Royal flush"
            else:
                print("no")
                return "Straight flush"

        # is it a four of a kind
        list_of_ranks = [c.rank for c in self.cards]
        print("Are there four of a kind?")
        for r in Card.ranks:
            if list_of_ranks.count(r) == 4:
                print("yes")
                return "Four of a kind"
        print("no")


        # base condition
        return "High card"


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

    current_cards = [Card("heart", "2"), Card("club", "2"), Card("heart", "2"),Card("heart", "2"), Card("heart", "king")]

    print("Current cards:")
    print("------------------------------")
    c = Combo(current_cards)
    print(c)
    print()
    print("Thought process:")
    print("------------------------------")
    decision = c.check()
    print()
    print("Decision:")
    print("------------------------------")
    print(decision)


if __name__ == "__main__":
    main()
