import random

# Global variables for suits and ranks
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')  # Possible suits in a deck
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
         'Jack', 'Queen', 'King', 'Ace')  # Possible ranks in a deck

# Dictionary to map card ranks to their values in Blackjack
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

class Card:
    """
    A class representing a single playing card.
    """
    def __init__(self, suit, rank):
        """
        Initialize a card with suit and rank.
        """
        self.suit = suit  # Suit of the card (Hearts, Diamonds, etc.)
        self.rank = rank  # Rank of the card (Two, Three, etc.)
        self.value = values[rank]  # Numerical value of the card based on Blackjack rules

    def __str__(self):
        """
        Return a string representation of the card.
        """
        return f"{self.rank} of {self.suit}"


class Deck:
    """
    A class representing a deck of 52 playing cards.
    """
    def __init__(self):
        """
        Initialize the deck with all 52 cards.
        """
        self.all_cards = []  # Start with an empty list to hold all Card objects
        for suit in suits:
            for rank in ranks:
                # Create a Card object for each suit and rank, and add it to the deck
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)

    def shuffle(self):
        """
        Shuffle the deck.
        """
        random.shuffle(self.all_cards)  # Use random.shuffle to shuffle the deck

    def deal_one(self):
        """
        Deal one card from the deck.
        """
        return self.all_cards.pop()  # Remove and return the last card from the deck


class Hand:
    """
    A class representing a player's or dealer's hand.
    """
    def __init__(self):
        """
        Initialize an empty hand.
        """
        self.cards = []      # List to store Card objects in the hand
        self.value = 0       # Total value of the hand
        self.aces = 0        # Number of aces in the hand

    def add_card(self, card):
        """
        Add a card to the hand.
        """
        self.cards.append(card)      # Add the card to the hand
        self.value += card.value     # Add the card's value to the hand's total value

        # Track aces to adjust their value later if needed
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        """
        Adjust the value of the hand if there are aces and total value is over 21.
        """
        # If total value > 21 and there's an ace, reduce the total value by 10
        # (treat the ace as 1 instead of 11)
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
    
    def is_blackjack(self):
        return self.value == 21 and len(self.cards) == 2


class Chips:
    """
    A class to keep track of a player's chips.
    """
    def __init__(self, total=100):
        """
        Initialize chips with a default total of 100.
        """
        self.total = total  # Total chips the player has
        self.bet = 0        # Current bet amount

    def win_bet(self):
        """
        Increase total chips by bet amount when the player wins.
        """
        self.total += self.bet

    def lose_bet(self):
        """
        Decrease total chips by bet amount when the player loses.
        """
        self.total -= self.bet

    def win_bet_blackjack(self):
        """
        Increase total chips by bet amount * 1.5 when the player wins with blackjack (10 or face card plus ace)
        """
        self.total += self.bet * 1.5
        self.total = int(self.total)


def take_bet(chips, rebet=False):
    """
    Ask the player for their bet amount and handle exceptions.
    """
    if rebet and chips.bet <= chips.total:
        print(f"Rebetting the previous amount: {chips.bet} chips.")
        return
    elif rebet and chips.bet > chips.total:
        print("Sorry, you don't have enough chips to rebet the previous amount.")

    while True:
        try:
            bet = int(input("How many chips would you like to bet? "))
        except ValueError:
            # Handle the case where the input is not an integer
            print("Sorry, a bet must be an integer!")
        else:
            if chips.bet > chips.total:
                # Check if the bet exceeds the player's total chips
                print(f"Sorry, your bet can't exceed {chips.total}")
            else:
                chips.bet = bet
                break  # Exit the loop if the bet is valid


def hit(deck, hand):
    """
    Add a card to the hand and adjust for aces.
    """
    hand.add_card(deck.deal_one())  # Deal a card from the deck and add it to the hand
    hand.adjust_for_ace()           # Adjust for aces if necessary


def hit_or_stand(deck, hand):
    """
    Prompt the player to hit or stand.
    """
    global playing  # Use the global variable 'playing' to control the game flow

    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's': ")

        if x[0].lower() == 'h':
            hit(deck, hand)  # Player chooses to hit, so deal another card
        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False  # Player chooses to stand, end their turn
        else:
            print("Sorry, please enter 'h' or 's'.")
            continue  # Invalid input, prompt again
        break  # Exit the loop after a valid input


def show_some(player, dealer):
    """
    Show the player's cards and one of the dealer's cards (hide the other).
    """
    print("\nDealer's Hand:")
    print(" <card hidden>")          # Hide the first dealer card
    print('', dealer.cards[1])        # Show the second dealer card
    print(f'Dealer\'s visible total: {dealer.cards[1].value}') # Show decimal value of dealer's visible card
    print("\nPlayer's Hand:", *player.cards, sep='\n ')  # Show all player's cards
    print(f'Player\'s total: {player.value}')  # Show decimal value of player's hand


def show_all(player, dealer):
    """
    Show all cards of both player and dealer.
    """
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)

def hand_outcome(outcome, chips):
    """
    Handle's various game outcomes such as a player busting or winning etc.
    """
    if outcome == 'player_busts':
        print("Player busts!")
        chips.lose_bet()
    elif outcome == 'dealer_busts':
        print("Dealer busts!")
        chips.win_bet()
    elif outcome == 'player_wins':
        print("Player wins!")
        chips.win_bet()
    elif outcome == 'dealer_wins':
        print("Dealer wins!")
        chips.lose_bet()
    elif outcome == 'push':
        print("Dealer and Player tie! It's a push.")
    elif outcome == 'player_blackjack':
         print("Blackjack! Player wins!")
         chips.win_bet_blackjack()

# Game logic starts here

# Set up the player's chips
player_chips = Chips()  # Default total of 100 chips

# Initially set rebet to false
rebet = False

while True:
    # Print an opening statement
    print("\nWelcome to Blackjack!")

    # Create & shuffle the deck
    deck = Deck()
    deck.shuffle()

    # (Re)sets blackjack win condition to false for the upcoming hand
    player_win_bj = False

    # Deal two cards to each player
    player_hand = Hand()
    player_hand.add_card(deck.deal_one())
    player_hand.add_card(deck.deal_one())    

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_one())
    dealer_hand.add_card(deck.deal_one())

    # Prompt the player for their bet if they are not using the quick rebet feature
    take_bet(player_chips, rebet=rebet)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    # Checks to see if the player's initial hand adds up to 21. If it does, they win automatically
    if player_hand.is_blackjack():
        if dealer_hand.is_blackjack():
            show_all(player_hand, dealer_hand)
            hand_outcome('push', player_chips)
        else:
            show_all(player_hand, dealer_hand)
            hand_outcome('player_blackjack', player_chips)
    else:
        if dealer_hand.is_blackjack():
            show_all(player_hand, dealer_hand)
            hand_outcome('dealer_wins', player_chips)
        else:
            playing = True


    while playing:
        # Prompt for player to hit or stand
        hit_or_stand(deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, player busts and loop breaks
        if player_hand.value > 21:
            hand_outcome('player_busts', player_chips)
            break

    # If player hasn't busted, and didn't  already win via blackjack, play dealer's hand
    if player_hand.value <= 21 and not player_win_bj:

        # Dealer hits until their value is 17 or more
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            hand_outcome('dealer_busts', player_chips)
        elif dealer_hand.value > player_hand.value:
            hand_outcome('dealer_wins', player_chips)
        elif dealer_hand.value < player_hand.value:
            hand_outcome('player_wins', player_chips)
        else:
            hand_outcome('push', player_chips)

    # Inform player of their chips total
    print(f"\nPlayer's winnings stand at {player_chips.total}")

    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' for yes, 'r' to rebet, or 'n' to quit: ")

    if new_game[0].lower() == 'y':
        rebet = False
    elif new_game[0].lower() == 'r':
        rebet = True
    else:
        print("Thanks for playing!")
        break  # Exit the game
