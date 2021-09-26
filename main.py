#!/usr/bin/python3

import random
import sys


# Card with a suit and rank
class Card:
    suits = ["heart", "club", "spade", "diamond"]
    ranks = [str(v) for v in range(2, 11)] + ["jack", "queen", "king", "ace"]
    values = list(range(1, 15))

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    @property
    def val(self):
        if self.rank == "jack": return 11
        if self.rank == "queen": return 12
        if self.rank == "king": return 13
        if self.rank == "ace" : return 14
        return int(self.rank)

    def __lt__(self, other):
        return self.val < other.val

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
        sorted_cards = sorted(self.cards)
        in_order = True
        # make this exception if the ace is used as a value of 1 and not of 14
        if [card.val for card in sorted_cards] == [2, 3, 4, 5, 14]:
            return 5
        for i, c in enumerate(sorted_cards[:-1]):
            if not c.val + 1 == sorted_cards[i + 1].val:
                return status
        status = sorted_cards[-1].val
        return status

    def has_pair(self):
        status = []
        list_of_ranks = [c.val for c in self.cards]
        for r in Card.values:
            if list_of_ranks.count(r) == 2:
                status.append(r)
        return status

    def has_triple(self):
        status = []
        list_of_ranks = [c.val for c in self.cards]
        for r in Card.values:
            if list_of_ranks.count(r) == 3:
                status.append(r)
        return status

    def has_quad(self):
        status = []
        list_of_ranks = [c.val for c in self.cards]
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
        temp = sorted([c.val for c in self.cards])
        return "HC"


def main():
    number_of_trials = 10 ** int(sys.argv[1])
    trials_completed = 0
    number_of_duplicates = 0
    amount_per_combo =              {"HC": 0, "P": 0, "TP" : 0, "ToaK": 0, "S": 0, "F": 0, "FH": 0, "FoaK": 0, "SF": 0, "RF": 0}
    expected_percent_per_combo =    {"HC": 50.12, "P": 42.26, "TP" : 4.754, "ToaK": 2.113, "S": 0.3925, "F": 0.1965, "FH": 0.1441, "FoaK": 0.02401, "SF": 0.001385, "RF": 0.0001539}

    while trials_completed < number_of_trials:
        # generate 5 random cards
        cards = []
        for i in range(5):
            suit = random.choice(Card.suits)
            rank = random.choice(Card.ranks)
            card = Card(suit, rank)
            cards.append(card)

        # make sure that two cards are not the same
        duplicate = False
        for i in range(len(cards)):
            for j in range(i + 1, len(cards)):
                if i != j and cards[i] == cards[j]:
                    number_of_duplicates += 1
                    duplicate = True
                    break

        if duplicate is True:
            continue

        # check what combo it falls under
        combo = Combo(cards)
        result = combo.check()
        # up the counter by 1
        amount_per_combo[result] += 1
        trials_completed += 1

    print()
    print("Combo name\tamount\t\tpercentage\texpected percentage")
    for combo_name in amount_per_combo:
        s = f"{combo_name}:\t\t"\
        f"{amount_per_combo[combo_name]}\t\t"\
        f"{format(amount_per_combo[combo_name] * 100 / trials_completed, '5.6f')}%\t\t"\
        f"{expected_percent_per_combo[combo_name]}%"
        print(s)


if __name__ == "__main__":
    main()
