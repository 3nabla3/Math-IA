#!/usr/bin/python3

import random
import time
from multiprocessing import Process, Value, Manager
import os
import sys

# Card with a suit and rank
class Card:
    suits = ["heart", "club", "spade", "diamond"]
    ranks = [str(v) for v in range(2, 11)] + ["jack", "queen", "king", "ace"]
    values = list(range(1, 15))

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def val(self):
        if self.rank == "jack": return 11
        if self.rank == "queen": return 12
        if self.rank == "king": return 13
        if self.rank == "ace" : return 14
        return int(self.rank)

    def __lt__(self, other):
        return self.val() < other.val()

    def __str__(self):
        return f"{self.rank.title()} of {self.suit}s"


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
        for card in self.cards:
            if not self.cards[0].suit == card.suit:
                return None
        return self.cards[0].suit

    def in_order(self):
        status = None
        o = sorted(self.cards)
        in_order = True
        for i, c in enumerate(self.cards[:-1]):
            if not c.val() + 1 == self.cards[i + 1].val():
                return status
        status = self.cards[-1].val()
        return status

    def has_pair(self):
        status = []
        list_of_ranks = [c.val() for c in self.cards]
        for r in Card.values:
            if list_of_ranks.count(r) == 2:
                status.append(r)
        return status

    def has_triple(self):
        status = []
        list_of_ranks = [c.val() for c in self.cards]
        for r in Card.values:
            if list_of_ranks.count(r) == 3:
                status.append(r)
        return status

    def has_quad(self):
        status = []
        list_of_ranks = [c.val() for c in self.cards]
        for r in Card.values:
            if list_of_ranks.count(r) == 4:
                status.append(r)
        return status

    def check(self):
        # is it a straight / royal flush?
        temp1 = self.same_suit()
        temp2 = self.in_order()
        if temp1 and temp2:
            # is the highest card an ace
            if temp2 == 14:
                return ["RF", [temp1,]]
            else:
                return ["SF", [temp1, temp2]]

        # is it a four of a kind?
        temp = self.has_quad()
        if temp: return ["FoaK", temp]

        # is it a full house?
        temp1 = self.has_triple()
        temp2 = self.has_pair()
        if temp1 and temp2: return ["FH", temp1 + temp2]

        # is it a flush?
        temp = self.same_suit()
        if temp: return ["Flush", temp]

        # is it a straight
        temp = self.in_order()
        if temp: return ["Straight", temp]

        # is it a Three of a kind
        temp = self.has_triple()
        if temp: return ["ToaK", temp]

        # is it a two pair
        temp = self.has_pair()
        if len(temp) == 2: return ["TP", temp]

        # is it a pair
        temp = self.has_pair()
        if temp: return ["P", temp]

        # base condition
        temp = sorted([c.val() for c in self.cards])
        return ["HC", [temp[-1],]]


def worker(keep_going, return_dict, procnum, gcount, target):
    try:
        count = 0
        t1 = time.time()
        running = True
        c = None
        result = None
        while keep_going.value:
            # deal 5 random cards
            current_cards = [Card(random.choice(Card.suits), random.choice(Card.ranks)) for i in range(5)]

            c = Combo(current_cards)
            result = c.check()
            if result[0] == target:
                keep_going.value = False
                return_dict[procnum] = [c, result]
            count += 1

        gcount.value += count
    except(KeyboardInterrupt):
        pass



def main():
    keep_going = Value('b', True)
    count = Value('i', 0)
    return_dict = Manager().dict()
    target = sys.argv[1]
    assert target in ["HC", "P", "TP", "ToaK", "Straight", "Flush", "FH", "FoaK", "SF", "RF"]
    p = [Process(target=worker, args=(keep_going, return_dict, i, count, target)) for i in range(os.cpu_count())]
    for i in p:
        i.start()

    try:
        for i in p:
            i.join()
    except(KeyboardInterrupt):
        pass

    for combo, result in return_dict.values():
        print(combo)
        print(result)
        print()
        print()

    print(f"Took {count.value} tries")


if __name__ == "__main__":
    main()
