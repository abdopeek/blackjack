from random import choice

file = open('results.csv', 'w')


def shuffle(ls, left=None, right=0):  # fisher-yates shuffle
    if not left:
        ls = ls[::2] + ls[1::2]
        left = len(ls[1::2])

    if right > left:  # base case, all elements have been shuffled
        return ls

    if right < left:  # recursive step 1: if there are still elements in org list ( sorting lhs )
        choice_left = choice(range(right, left))  # pick a random number from start to end index
        ls[right], ls[choice_left] = ls[choice_left], ls[right]  # swap out numbers

    if left + right < len(ls): # recursive step 2: if there are still elements in the right ( sorting rhs )
        choice_right = choice(range(right+left, len(ls)))  # pick random number between mid and end ( rhs )
        ls[-1 - right], ls[choice_right] = ls[choice_right], ls[-1 - right]  # swap

    return shuffle(ls, left, right+1)


class Table:
    def __init__(self, player):
        self.dealer = Dealer()
        self.deck = Deck()
        self.player = Player(player)

        file.write('winner,dealer_hand,player_hand\n')
        self.setup_game()

    def new_game(self):
        self.dealer = Dealer()
        self.player.score = 0
        self.player.hand = []
        self.deck = Deck()

        self.setup_game()
        self.main()

    def setup_game(self):
        self.deck.shuffle()  # shuffle cards before starting game
        self.player.place_bet()
        self.deal_card(self.player)  # deal card to player, then dealer, then player.
        self.deal_card(self.dealer)
        self.deal_card(self.player)
        self.calculate_score(self.player)
        self.calculate_score(self.dealer)

        self.main()  # main game

    def main(self):
        while True:
            print(self)
            player_move = self.player.hit_or_stick()
            if player_move:
                self.deal_card(self.player)
                self.calculate_score(self.player)
            else:
                self.dealer_hit()

    def dealer_hit(self):
        while True:
            if self.dealer.score < 17:
                self.deal_card(self.dealer)
                self.calculate_score(self.dealer)
                print(self)  # prints __str__
            elif self.dealer.score >= 17:
                self.check_final_score()

    def __str__(self):
        dealer_hand = [card for card, v in self.dealer.hand]
        p_hand = [card for card, v in self.player.hand]

        print(f"Dealer hand: {dealer_hand}")
        print(f"Dealer score: {self.dealer.score}\n")

        print(f"Your hand: {p_hand}")
        print(f"Your score: {self.player.score}\n")

        print(f"Your current bet: {self.player.bet}")
        print(f"Your current funds: {self.player.funds}")
        print('-' * 40)

        return ''

    def calculate_score(self, p):
        val = sum(card[1] for card in p.hand)  # eg A22
        if val <= 11 and any(card[0] == "A" for card in p.hand):
            val += 10
        p.score = val
        self.check_win(p.score, p)

    def deal_card(self, p):
        deck = self.deck
        p.hand.append(deck.stack.pop())

    def check_win(self, score, player):
        if score > 21:
            print(self)
            print(f"{player.name} busts")
            try:
                player.payout(False)
                file.write(f'{self.player.name},"{self.dealer.hand}","{self.player.hand}"\n')
            except:
                self.player.payout(True)
                file.write(f'{self.player.name},"{self.dealer.hand}","{self.player.hand}"\n')
            self.end_game()
        elif score == 21:
            print(self)
            print(f"{player.name} blackjack")
            try:
                player.payout(True)
                file.write(f'{self.player.name},"{self.dealer.hand}","{self.player.hand}"\n')
            except:
                file.write(f'{self.player.name},"{self.dealer.hand}","{self.player.hand}"\n')
            self.end_game()
        else:
            return

    def check_final_score(self):
        dealer_score = self.dealer.score
        player_score = self.player.score

        if dealer_score > player_score:
            print("Dealer wins!")
            file.write(f'{self.player.name},"{self.dealer.hand}","{self.player.hand}"\n')
            self.end_game()
        else:
            print(f"You win!")
            file.write(f'{self.player.name},"{self.dealer.hand}","{self.player.hand}"\n')
            self.player.payout(True)
            self.end_game()

    def end_game(self):
        funds = self.player.funds
        if funds:
            again = input("Do you want to play again (Y/N): ")
            if again.lower().startswith('y'):
                self.new_game()
            elif again.lower().startswith('n'):
                exit(1)
        else:
            print("You're all out of money! Get it up and come back :(")
            exit(0)


class Deck:
    def __init__(self):
        self.stack = [('A', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5),
                      ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10),
                      ('J', 10), ('Q', 10), ('K', 10)] * 4
        self.shuffle()

    def shuffle(self):
        self.stack = shuffle(self.stack)


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
        while True:
            choice = input("Would you like to change your bet (Y/N): ")
            if choice.startswith('n'):
                self.funds -= self.bet
                return
            elif choice.startswith('y'):
                bet = input("Enter your new bet: ")
                try:
                    bet = float(bet)
                    if bet > self.funds:
                        print("You don't have that much funds!")
                        continue
                    self.bet = bet
                    self.funds -= self.bet
                    return
                except ValueError:
                    print("Please enter valid number or (N) to exit: ")
                    continue
            else:
                print("Invalid input, (Y/N): ")
                continue

    def payout(self, win):
        if win:
            self.funds += self.bet + (self.bet * 2)
        else:
            pass

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


name = 'tom'
table = Table(name)
