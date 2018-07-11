import random

class Desk(object):
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer = Dealer()
        self.dealer.hit(self.deck)
        self.player = Player()
        self.player.hit(self.deck)
        self.player.hit(self.deck)
        self.gambles = 0

    def player_hit(self):
        self.player.hit(self.deck)
    
    def dealer_hit(self):
        self.dealer.hit(self.deck)

    def new_game(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player.clearhand()
        self.dealer.clearhand()
        self.player.hit(self.deck)
        self.player.hit(self.deck)
        self.dealer.hit(self.deck)
        self.gambles = 0

    def gambled(self, value):
        self.gambles += value
        self.gambles += self.dealer.gamble(value)
    
    def getgamble(self):
        return self.gambles/2

class Deck(object):
    def __init__(self):
        self.deck = []
        for suit in ('heart', 'diamond', 'club', 'spades'):
            for value in ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'):
                self.deck.append((suit, value))

    def getdeck(self):
        return self.deck

    def setdeck(self, card=('heart', 'A')):
        self.deck.pop(self.deck.index(card))

    def shuffle(self):
        self.deck.sort(key=lambda _: random.randint(1, 1000))

    def drawCard(self):
        return self.deck.pop(0)


class Player(object):
    def __init__(self):
        self.hand = []
        self.bank = 1000

    def hit(self, deck):
        suit, value = deck.drawCard()
        self.hand.append(tuple(((suit,value))))
        return 1

    def stand(self):
        return 0

    def gamble(self, value):
        if self.bank - value >= 0:
            self.bank -= value
            return value
        else:
            return -1

    def show_hand(self):
        print(self.hand)
    
    def getbank(self):
        return self.bank
    
    def clearhand(self):
        self.hand.clear()

    def hand_sum(self):
        sum_hand = 0
        number_of_as = 0
        for card in self.hand:
            if card[1] == 'J' or card[1] == 'Q' or card[1] == 'K' or card[1] == '10':
                sum_hand += 10
            elif card[1] == 'A':
                sum_hand += 11
                number_of_as += 1
            else:
                sum_hand += int(card[1])
        while number_of_as > 0:
            if sum_hand > 21:
                sum_hand -= 10
                number_of_as -= 1
            elif sum_hand == 21:
                number_of_as = 0
        return sum_hand


    
    def addfunds(self, value):
        self.bank += value

class Dealer(Player):
    
    def __init__(self):
        self.hand = []
        self.bank = 100000000
    
    def chance_of_hitting(self):
        chance = random.randint(0,100)
        if self.hand_sum() <= 11:
            return 1
        elif self.hand_sum() < 21 and chance > 50:
            return 1
        else:
            return 0




desk = Desk()
while True:
    print("You have %d dollars. How much would you like to gamble?"%(desk.player.getbank()))

    while(True):    
        answer = desk.player.gamble(int(input()))
        if  answer == -1:
            print("You don't have that much money, try again")
        else:
            desk.gambled(answer)
            break

    print("Your hand:", end ='')
    desk.player.show_hand()
    print()
    print("Dealer's hand: ", end = '')
    desk.dealer.show_hand()
    print()
    while (int(input("What would you like to do?\n1.Hit\n2.Stand\n"))) == 1:
        desk.player_hit()
        print("Your hand:", end = '')
        desk.player.show_hand()
        print()



    if desk.player.hand_sum() > 21:
        print("You busted. You lose {a} dollars.".format(a = desk.getgamble()))
        desk.dealer.addfunds(desk.getgamble()*2)
    else:

        while(desk.dealer.chance_of_hitting()):
            desk.dealer_hit()
            print("Dealer's hand: ", end = '')
            desk.dealer.show_hand()
            print()


        print("Your hand:", end = '')
        desk.player.show_hand()
        print()
        print("Dealer's hand: ", end = '')
        desk.dealer.show_hand()
        print()
        if  desk.dealer.hand_sum() > 21:
            print("Dealer busted. You won {a} dollars!".format(a = desk.getgamble()*2))
            desk.player.addfunds(desk.getgamble()*2)
        elif desk.player.hand_sum() > desk.dealer.hand_sum():
            desk.player.addfunds(desk.getgamble()*2)
            print("You won {a} dollars!".format(a = desk.getgamble()*2))
        else:
            desk.dealer.addfunds(desk.getgamble()*2)
            print("You lost {a} dollars.".format(a = desk.getgamble()))

    if str(input("Do you want to keep playing[yes/no]:\n")) == 'yes':
        desk.new_game()
    else:
        break

