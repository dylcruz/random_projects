import random

# Global variables for suits and ranks
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')  # Possible suits in a deck
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
         'Jack', 'Queen', 'King', 'Ace')  # Possible ranks in a deck

# Dictionary to map card ranks to their values in Blackjack
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

# Setting the maximum and minimum bets
MIN_BET = 5
MAX_BET = 50

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
    
    def reset(self):
        """
        Resets hand values back to initial
        """
        self.cards = []
        self.value = 0
        self.aces = 0


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
        self.double_down_bet = 0 # Current double down bet amount

    def win_bet(self):
        """
        Increase total chips by bet amount when the player wins.
        """
        total_bet = self.bet + self.double_down_bet
        winnings = total_bet * 2
        self.total += winnings

    def push(self):
        """
        Players gets their original and double down bets back
        """
        total_bet = self.bet + self.double_down_bet
        self.total += total_bet

    def win_bet_blackjack(self):
        """
        Increase total chips by bet amount * 1.5 when the player wins with blackjack (10 or face card plus ace)
        """
        self.total += self.bet + (self.bet * 1.5)
        self.total = int(self.total)

    def double_down(self):
        """
        Checks to ensure player has enough chips to double down, then makes the bet
        """
        if self.bet <= self.total:
            self.double_down_bet = self.bet
            self.total -= self.double_down_bet
            print(f'Double down! New bet amount is {self.bet + self.double_down_bet}.')
            return True
        else:
            print(f'You don\'t have enough chips to double down.')
            return False
    
    def reset_bets(self, rebet=False):
        self.double_down_bet = 0
        if rebet:
            return
        else:
            self.bet = 0


class Player:
    """
    Class to keep track of an individual player
    """
    def __init__(self, name, starting_chips=100):
        # Initialize a hand, chips, and game variables for a player
        self.hand = Hand()
        self.chips = Chips(total=starting_chips)
        self.name = name
        self.playing = False
        self.skip_dealer_hit = False
        self.rebet = False
    
    def reset(self):
        # Resets player variables for next hand
        self.playing = False
        self.skip_dealer_hit = False
        self.hand.reset()


class Game:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()


    def reset_and_shuffle_deck(self):
        self.deck = Deck()
        self.deck.shuffle()


    def take_bet(self, chips, rebet=False):
        """
        Ask the player for their bet amount and handle exceptions.
        """
        if rebet and chips.bet <= chips.total:
            print(f"Rebetting the previous amount: {chips.bet} chips.")
            chips.total -= chips.bet
            return
        elif rebet and chips.bet > chips.total:
            print("Sorry, you don't have enough chips to rebet the previous amount.")

        while True:
            try:
                print(f'You have {chips.total} chips available.')
                bet = int(input(f"How many chips would you like to bet? (min: {MIN_BET} / max: {MAX_BET}): "))
            except ValueError:
                # Handle the case where the input is not an integer
                print("Sorry, a bet must be an integer!")
            else:
                if bet > chips.total:
                    # Check if the bet exceeds the player's total chips
                    print(f"Sorry, your bet can't exceed {chips.total}")
                elif bet < MIN_BET or bet > MAX_BET:
                    # Check if bet is within limits
                    print(f'Sorry! Bet must be between {MIN_BET} and {MAX_BET} chips.')
                else:
                    chips.bet = bet
                    chips.total -= chips.bet
                    break  # Exit the loop if the bet is valid


    def hit(self, deck, hand):
        """
        Add a card to the hand and adjust for aces.
        """
        hand.add_card(deck.deal_one())  # Deal a card from the deck and add it to the hand
        hand.adjust_for_ace()           # Adjust for aces if necessary


    def players_turn(self, deck, player):
        """
        Prompt the player to hit, stand, or double down.
        """
        while True:
            x = input("Would you like to Hit, Stand, or Double Down? Enter 'h', 's', or 'd': ")

            if x[0].lower() == 'h':
                self.hit(deck, player.hand)  # Player chooses to hit, so deal another card
            elif x[0].lower() == 's':
                print("Player stands. Dealer is playing.")
                player.playing = False  # Player chooses to stand, end their turn
            elif x[0].lower() == 'd':
                if player.chips.double_down(): # Checks to make sure player has enough chips to double down
                    self.hit(deck, player.hand)
                    player.playing = False # You cannot hit anymore after doubling down
                else:
                    continue     
            else:
                print("Sorry, please enter 'h', 's', or 'd'.")
                continue  # Invalid input, prompt again
            break  # Exit the loop after a valid input


    def show_some(self, player_hand, dealer_hand):
        """
        Show the player's cards and one of the dealer's cards (hide the other).
        """
        print("\nDealer's Hand:")
        print(" <card hidden>")          # Hide the first dealer card
        print('', dealer_hand.cards[1])        # Show the second dealer card
        print(f'Dealer\'s visible total: {dealer_hand.cards[1].value}') # Show decimal value of dealer's visible card
        print("\nPlayer's Hand:", *player_hand.cards, sep='\n ')  # Show all player's cards
        print(f'Player\'s total: {player_hand.value}')  # Show decimal value of player's hand


    def show_all(self, player_hand, dealer_hand):
        """
        Show all cards of both player and dealer.
        """
        print("\nDealer's Hand:", *dealer_hand.cards, sep='\n ')
        print("Dealer's Hand =", dealer_hand.value)
        print("\nPlayer's Hand:", *player_hand.cards, sep='\n ')
        print("Player's Hand =", player_hand.value)


    def hand_outcome(self, outcome, chips):
        """
        Handle's various game outcomes such as a player busting or winning etc.
        """
        if outcome == 'player_busts':
            print("Player busts!")
        elif outcome == 'dealer_busts':
            print("Dealer busts!")
            chips.win_bet()
        elif outcome == 'player_wins':
            print("Player wins!")
            chips.win_bet()
        elif outcome == 'dealer_wins':
            print("Dealer wins!")
        elif outcome == 'push':
            chips.push()
            print("Dealer and Player tie! It's a push.")
        elif outcome == 'player_blackjack':
            print("Blackjack! Player wins!")
            chips.win_bet_blackjack()


    def check_blackjack(self, player, dealer_hand):
        if player.hand.is_blackjack():
            if dealer_hand.is_blackjack():
                self.show_all(player.hand, dealer_hand)
                self.hand_outcome('push', player.chips)
                player.skip_dealer_hit = True
            else:
                self.show_all(player.hand, dealer_hand)
                self.hand_outcome('player_blackjack', player.chips)
                player.skip_dealer_hit = True
        else:
            if dealer_hand.is_blackjack():
                self.show_all(player.hand, dealer_hand)
                self.hand_outcome('dealer_wins', player.chips)
                player.skip_dealer_hit = True
            else:
                player.playing = True


# Game logic starts here

# Create a game and add a player
game = Game()
p1 = Player('Player 1')


while True:
    # Print an opening statement
    print("\nWelcome to Blackjack!")

    # Deal two cards to each player   
    p1.hand.add_card(game.deck.deal_one())
    p1.hand.add_card(game.deck.deal_one())

    dealer_hand = Hand()
    dealer_hand.add_card(game.deck.deal_one())
    dealer_hand.add_card(game.deck.deal_one())

    # Prompt the player for their bet if they are not using the quick rebet feature
    game.take_bet(p1.chips, p1.rebet)

    # Show cards (but keep one dealer card hidden)
    game.show_some(p1.hand, dealer_hand)

    # Checks to see if the player or dealer initial hand is 21. If so, the game is automatically over
    game.check_blackjack(p1, dealer_hand)

    while p1.playing:
        # Prompt for player to choose what to do
        game.players_turn(game.deck, p1)

        # Show cards (but keep one dealer card hidden)
        game.show_some(p1.hand, dealer_hand)

        # If player's hand exceeds 21, player busts and loop breaks
        if p1.hand.value > 21:
            game.hand_outcome('player_busts', p1.chips)
            break

    # If player hasn't busted, and game hasn't ended early due to blackjack, the dealer now draws cards
    if p1.hand.value <= 21 and not p1.skip_dealer_hit:

        # Dealer hits until their value is 17 or more
        while dealer_hand.value < 17:
            game.hit(game.deck, dealer_hand)

        # Show all cards
        game.show_all(p1.hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            game.hand_outcome('dealer_busts', p1.chips)
        elif dealer_hand.value > p1.hand.value:
            game.hand_outcome('dealer_wins', p1.chips)
        elif dealer_hand.value < p1.hand.value:
            game.hand_outcome('player_wins', p1.chips)
        else:
            game.hand_outcome('push', p1.chips)

    # Inform player of their chips total
    print(f"\nPlayer's winnings stand at {p1.chips.total}")

    # Resets the player's hand
    p1.reset()

    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' for yes, 'r' to rebet, or 'n' to quit: ")

    if new_game[0].lower() == 'y':
        p1.rebet = False
        p1.chips.reset_bets()
    elif new_game[0].lower() == 'r':
        p1.rebet = True
        p1.chips.reset_bets(rebet=p1.rebet)
    else:
        print("Thanks for playing!")
        break  # Exit the game
