from random import shuffle

class Deck:
    def __init__(self):
        self.stack = [('A', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5),
                      ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10),
                      ('J', 10), ('Q', 10), ('K', 10)] * 4
        self.shuffle()

    def shuffle(self):
        shuffle(self.stack)


class Dealer(object):
    def __init__(self, name="Dealer"):
        self.name = name
        self.hand = []
        self.score = 0


class Player(Dealer):
    def __init__(self, name, funds=100, bet=10):
        super().__init__(name)
        self.funds = funds
        self.bet = bet

    def place_bet(self):
        print(f"Your current bet is {self.bet}")
        choice = input("Would you like to increase it? (Y/N): ").lower()
        while True:
            if choice.startswith('y'):
                bet = input("Enter new bet: ")
                try:
                    bet = float(bet)
                    self.bet = bet
                    return
                except TypeError:
                    print("Please enter valid number or (N) to exit: ")
                    continue
            elif choice.startswith('n'):
                return
            else:
                print("Please enter valid input (Y/N): ")
                continue

    @staticmethod
    def hit_or_stick():
        while True:
            choice = input("Do you want another card? (Y/N): ").lower()
            if choice.startswith('y'):
                return True
            elif choice.startswith('n'):
                return False
            else:
                print("Enter valid choice (Y/N): ")
                continue
