# Game Play
# To play a hand of Blackjack the following steps must be followed:

# Create a deck of 52 cards
# Shuffle the deck
# Ask the Player for their bet
# Make sure that the Player's bet does not exceed their available chips
# Deal two cards to the Dealer and two cards to the Player
# Show only one of the Dealer's cards, the other remains hidden
# Show both of the Player's cards
# Ask the Player if they wish to Hit, and take another card
# If the Player's hand doesn't Bust (go over 21), ask if they'd like to Hit again.
# If a Player Stands, play the Dealer's hand. The dealer will always Hit until the Dealer's value meets or exceeds 17
# Determine the winner and adjust the Player's chips accordingly
# Ask the Player if they'd like to play again


# Step 1: Import the random module.

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


# Class Definitions
# Step 2: Create a Card Class

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


# Step 3: Create a Deck Class
# Here we might store 52 card objects in a list that can later be shuffled.

class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


# Step 4: Create a Hand Class

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self, card):
        # card passed in in from
        # Deck.deal() --> single Card(suit,rank)
        self.cards.append(card)
        self.value += values[card.rank]

        # track aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):

        # IF TOTAL VALUE > 21 AND I STILL HAVE AN ACE
        # THEN CHANGE MY ACE TO BE 1 INSTEAD OF 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# Step 5: Create a Chips Class

class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# Function Defintions

# Step 6: Write a function for taking bets

def take_bet(chips):

    while True:

        try:
            chips.bet = int(input("How many chips would you like to bet"))
        except:
            print("Sorry please provide an integar")
        else:
            if chips.bet > chips.total:
                print(
                    f'Sorry, you do have enough chips you have {chips.total}')
            else:
                break


# Step 7: Write a function for taking hits

def hit(deck, hand):

    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()


# Step 8: Write a function prompting the Player to Hit or Stand

def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while True:
        x = input('Hit or Stand? Enter h or s ')

        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print("Player Stands Dealer's Turn")
            playing = False

        else:
            print("Sorry, I did not understand that, Please Enter h or s only!")
            continue
        break


# Step 9: Write functions to display cards

def show_some(player, dealer):

    # Show only ONE of the dealer's cards
    print("\n Dealer's Hand: ")
    print("First card hidden!")
    print(dealer.cards[1])

    # Show all (2 cards) of the player's hand/cards
    print("\n Player's Hand:")
    for card in player.cards:
        print(card)


def show_all(player, dealer):

    # show all the dealer's cards
    print("\n Dealer's Hand:")
    for card in dealer.cards:
        print(card)

    # calculate and display value (J+K = 20)
    print(f"Value of Player's Hand is: {player.value}")

    # show all the players cards
    print("\n Player's Hand:")
    for card in player.cards:
        print(card)


# Step 10: Write functions to handle end of game scenarios

def player_busts(player, dealer, chips):
    print("BUST PLAYER!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("PLAYER WINS!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("PLAYER WINS! DEALER BUSTED!")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("DEALER WINS")
    chips.lose_bet()


def push(player, dealer):
    print("Dealer and player tie! PUSH")


# And now on to the game!!

while True:
    # Print an opening statement
    print("Welcome to BlackJack")

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)

            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)

        else:
            push(player_hand, dealer_hand)

    # Inform Player of their chips total
    print(f"\n Player total chips are at: {player_chips.total}")

    # Ask to play again
    new_game = input("Would you like to play agian? y/n ")

    if new_game[0].lower() == 'y':
        playing = True
        continue

    else:
        print("Thank you for playing")
        break
