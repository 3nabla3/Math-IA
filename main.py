#!/usr/bin/python3

import random
import time
from multiprocessing import Process, Value, Manager
import os
import sys
import json

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

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank


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
                return "RF"
            else:
                return "SF"

        # is it a four of a kind?
        temp = self.has_quad()
        if temp: return "FoaK"

        # is it a full house?
        temp1 = self.has_triple()
        temp2 = self.has_pair()
        if temp1 and temp2: return "FH"

        # is it a flush?
        temp = self.same_suit()
        if temp: return "F"

        # is it a straight
        temp = self.in_order()
        if temp: return "S"

        # is it a Three of a kind
        temp = self.has_triple()
        if temp: return "ToaK"

        # is it a two pair
        temp = self.has_pair()
        if len(temp) == 2: return "TP"

        # is it a pair
        temp = self.has_pair()
        if temp: return "P"

        # base condition
        temp = sorted([c.val() for c in self.cards])
        return "HC"


def worker(keep_going, return_dict, procnum):
    try:
        combo_name = None
        running = True
        c = None
        # create a temp dict of combo freq
        amount_per_combo = {"HC": 0, "P": 0, "TP" : 0, "ToaK": 0, "S": 0, "F": 0, "FH": 0, "FoaK": 0, "SF": 0, "RF": 0}
        while keep_going.value:
            # deal 5 random cards
            current_cards = [Card(random.choice(Card.suits), random.choice(Card.ranks)) for i in range(5)]

            for i in range(len(current_cards)):
                for j in range(i, len(current_cards)):
                    if i == j:
                        continue

            c = Combo(current_cards)

            # check the 5 cards for combo
            combo_name = c.check()
            amount_per_combo[combo_name] += 1
    except(KeyboardInterrupt):
        pass
    finally:
        return_dict[procnum] = amount_per_combo


def save_work(file_name, this_round_amount_per_combo):
    # save the results to json
    if os.path.exists(file_name):
        g_amount_per_combo = {"HC": 0, "P": 0, "TP" : 0, "ToaK": 0, "S": 0, "F": 0, "FH": 0, "FoaK": 0, "SF": 0, "RF": 0}
        with open(file_name, 'r') as file:
            file_amount_per_combo = json.load(file)
            for key in file_amount_per_combo:
                g_amount_per_combo[key] = this_round_amount_per_combo[key] + file_amount_per_combo[key]
    else:
        g_amount_per_combo = this_round_amount_per_combo.copy()

    with open(file_name, 'w') as file:
        json.dump(g_amount_per_combo, file)
        print("Work saved!")

    return g_amount_per_combo


def main():
    # set global values
    keep_going = Value('b', True)
    file_name = 'results.json'

    # search time 10s by default
    search_time = 0
    if len(sys.argv) > 1:
        search_time = float(sys.argv[1])
    if len(sys.argv) > 2:
        file_name = sys.argv[2]

    print(file_name)

    if search_time < 0:
        raise ValueError("search time must be a positive value")


    start_time = time.time()

    # stop all processes after the seach time and wait for them
    while True:
        try:
            # create a global dict with freq of each combo
            this_round_amount_per_combo = {"HC": 0, "P": 0, "TP" : 0, "ToaK": 0, "S": 0, "F": 0, "FH": 0, "FoaK": 0, "SF": 0, "RF": 0}
            return_dict = Manager().dict()

            # create processes and start them
            p = [Process(target=worker, args=(keep_going, return_dict, i)) for i in range(os.cpu_count())]
            print()
            for i in p:
                i.start()

            time.sleep(3)
            keep_going.value = False
        # if the program is quit, display what ever is already found
        except(KeyboardInterrupt):
            keep_going.value = False
            print()
            break
        finally:
            for i in p:
                i.join()
            keep_going.value = True

            # populate that dict with the worker dict
            for procnum in return_dict:
                for combo_name in return_dict[procnum]:
                    this_round_amount_per_combo[combo_name] += return_dict[procnum][combo_name]

            g_amount_per_combo = save_work(file_name, this_round_amount_per_combo)

            this_round_total = sum(this_round_amount_per_combo.values())
            g_total = sum(g_amount_per_combo.values())
            print(this_round_total, "additional combos found")
            print()
            print("Combo Name\tRound #\t\tRound %\t\tTotal #\t\tTotal %")
            if (this_round_total > 0):
                for combo_name in this_round_amount_per_combo:
                    print(f"{combo_name}:\t\t{this_round_amount_per_combo[combo_name]}\t\t{round(this_round_amount_per_combo[combo_name] * 100 / this_round_total, 3)}%\t\t{g_amount_per_combo[combo_name]}\t\t{round(g_amount_per_combo[combo_name] * 100 / g_total, 3)}%")
                print()


    # print(f"Took {sum(g_amount_per_combo.values())} tries and {time.time() - start_time} seconds")


if __name__ == "__main__":
    main()
