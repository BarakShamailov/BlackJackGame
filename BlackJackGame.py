import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True


class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        pass

    def __str__(self):
        return f'{self.rank} of {self.suit}'
        pass


class Deck:

    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit,rank))
        pass
    def __str__(self):
        print_deck = 'The deck is:'
        for i in self.all_cards:
            print_deck += '\n' + i.__str__()
        return print_deck
        pass

    def shuffle(self):
        random.shuffle(self.all_cards)
        pass

    def deal(self):
        return self.all_cards.pop()


    def length(self):
        return len(self.all_cards)


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.sum = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.sum += values[card.rank]
        if card.suit == 'Ace':
            self.aces +=1
        pass
    def __str__(self):
        hand_cards = ""
        for i in range(len(self.cards)):
            if i == len(self.cards)-1:
                hand_cards += ' ' + self.cards[i].__str__() + '.'
            else:
                hand_cards += self.cards[i].__str__() + ',\t'

        return f'Your cards are: {hand_cards}\nThe sum of the cards is - {self.sum}\n'

    def adjust_for_ace_to_1(self):
        # when the player have ace and his sum over 21 we adjust the ace value for him to 1
        while self.sum > 21 and self.aces:
            self.sum -= 10
            self.aces-= 1
        pass

def validiation_digit(bet_time=0):
    val = 0
    while True:
        try:
            if bet_time:
               val = int(input('How many chips would you like to bet? '))
            else:
                val = int(input("Please enter a amount of money: "))
        except ValueError:
            print("Looks like you did not enter an digits!")
            continue
        else:
            break

    return val

class Chips:

    def __init__(self):
        self.total = validiation_digit()
        self.bet = 0

    def win_bet(self):
        self.total += self.bet
        pass

    def lose_bet(self):
        self.total -= self.bet
        pass

def take_bet(chips):
    while True:
        chips.bet = validiation_digit(1)
        if chips.bet > chips.total:
            print("Sorry, you dont have enough money")
        else:
            break


def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace_to_1()


def hit_or_stand(deck, hand):
    global playing
    while True:
        action =  input("Would you like to Hit or Stand? Enter 'h' or 's': ")
        if not(action[0].lower() == 'h' or action[0].lower() == 's'):
            print("Wrong choice, please try again.")
            continue
        else:
            if action[0].lower() == 'h':
                hit(deck,hand)
                break
            else:
                print("Player stands. Dealer is playing.")
                playing = False
                break
    pass


def show_some(player, dealer):
    print("\nThe dealer hand-")
    print('< card hidden >')
    print(dealer.cards[1])
    print("\nThe player hand-\n"+ player.__str__())
    pass


def show_all(player, dealer):
    print("\nThe player hand-\n"+ player.__str__())
    print("\nThe dealer hand-\n" + dealer.__str__())
    pass


def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()
    pass


def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()
    pass


def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()
    pass


def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()
    pass

def replay():
    opt = ''
    while opt.lower() != 'y' and opt.lower() != 'n':
        opt = input("Would you like to play another hand? Enter 'y' or 'n' ")

    return opt.lower() == 'y'



if __name__ == '__main__':
    while True:
        # Print an opening statement
        print('\n'*100)
        print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
            Dealer hits until she reaches 17. Aces count as 1 or 11.')

        # Create & shuffle the deck, deal two cards to each player
        new_deck = Deck()
        new_deck.shuffle()
        player_hand = Hand()
        player_hand.add_card(new_deck.deal())
        player_hand.add_card(new_deck.deal())
        dealer_hand = Hand()
        dealer_hand.add_card(new_deck.deal())
        dealer_hand.add_card(new_deck.deal())

        # Set up the Player's chips

        player_chips = Chips()
        # Prompt the Player for their bet
        take_bet(player_chips)
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        while playing:  # recall this variable from our hit_or_stand function

            # Prompt for Player to Hit or Stand
            hit_or_stand(new_deck, player_hand)

            # Show cards (but keep one dealer card hidden)
            show_some(player_hand, dealer_hand)

            # If player's hand exceeds 21, run player_busts() and break out of loop
            if player_hand.sum > 21:
                player_busts(player_hand, dealer_hand, player_chips)
                break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        if player_hand.sum <= 21:

            while dealer_hand.sum < 17:
                hit(new_deck, dealer_hand)

            show_all(player_hand, dealer_hand)

            if dealer_hand.sum > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)
            elif dealer_hand.sum > player_hand.sum:
                dealer_wins(player_hand, dealer_hand, player_chips)
            elif player_hand.sum > dealer_hand.sum:
                player_wins(player_hand, dealer_hand, player_chips)
            else:
                print("Dealer and Player tie! It's a push.")
        # Inform Player of their chips total
        print(f"Your total chips are - {player_chips.total}")
        # Ask to play again
        if replay():
            playing = True
            continue
        else:
            break



