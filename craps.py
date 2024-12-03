import random

craps_bets = {
    'pass' : False,
    'dont_pass' : False,
    '4' : False,
    '5' : False,
    '6' : False,
    '8' : False,
    '9' : False,
    '10' : False,
    'field' : False,
    'hard_4' : False,
    'hard_6' : False,
    'hard_8' : False,
    'hard_10' : False,
}

bet_payouts = {
    'pass' : 1,
    'dont_pass' : 1,
    '4' : 9/5,
    '5' : 7/5,
    '6' : 7/6,
    '8' : 7/6,
    '9' : 7/5,
    '10' : 9/5,
    'field' : 1,
    'hard_4' : 7,
    'hard_6' : 9,
    'hard_8' : 9,
    'hard_10' : 7,
}

pass_wins = [7, 11]
pass_loses = [2, 3, 12]
dont_pass_wins = [2, 3]
field_double_payouts = [2, 12]
contract_bets = ['pass', 'dont_pass', 'come', 'dont_come']
field_bets = [2, 3, 4, 9, 10, 11, 12]
place_bets = ['4', '5', '6', '8', '9', '10']
one_roll_bets = ['field']
hard_way_bets = ['hard_4', 'hard_6', 'hard_8', 'hard_10']

class Dice:
    def __init__(self):
        self.current_roll = 0
        self.roll_1 = 0
        self.roll_2 = 0
    
    def roll_dice(self):
        self.roll_1 = random.randint(1, 6)
        self.roll_2 = random.randint(1, 6)
        self.current_roll = self.roll_1 + self.roll_2
        print(f'\nThe dice roll and land on... [{self.roll_1}] [{self.roll_2}] - {self.current_roll}')
    
    def check_hard_ways(self, bet):
        if bet == 'hard_4':
            if self.roll_1 == 2 and self.roll_2 == 2:
                return True
            elif self.current_roll == 4:
                return False
            else:
                return
        elif bet == 'hard_6':
            if self.roll_1 == 3 and self.roll_2 == 3:
                return True
            elif self.current_roll == 6:
                return False
            else:
                return
        elif bet == 'hard_8':
            if self.roll_1 == 4 and self.roll_2 == 4:
                return True
            elif self.current_roll == 8:
                return False
            else:
                return
        elif bet == 'hard_10':
            if self.roll_1 == 5 and self.roll_2 == 5:
                return True
            elif self.current_roll == 10:
                return False
            else:
                return
        else:
            return

class Chips:
    def __init__(self, starting_chips=1000):
        self.total_chips = starting_chips

class Player:
    def __init__(self, name):
        self.name = name
        self.chips = Chips()
        self.bets = dict(craps_bets)
        self.saved_bets = {}

    def make_bet(self, bet, amount=0):
        if amount == 0:
            bet_amount = int(input(f'Enter bet amount for bet {bet}: '))
        else:
            bet_amount = amount
        if bet_amount > self.chips.total_chips:
            print(f'Error. Bet amount {bet_amount} greater than total chips ({self.chips.total_chips}). Bet was NOT made.')
            return
        self.bets[bet] = bet_amount
        self.chips.total_chips -= bet_amount
        print(f'{self.name} makes bet {bet} for {bet_amount} chips. Total chips is now at {self.chips.total_chips}. (excl. working bets)')

    def remove_bet(self, bet):
        bet_amount = self.bets[bet]
        self.bets[bet] = False
        self.chips.total_chips += bet_amount
        print(f'{self.name} removes bet {bet} for {bet_amount} chips. Total chips is now at {self.chips.total_chips}. (excl. working bets)')

    def win_bet(self, bet, payout_override=1):
        winnings = self.bets[bet] * (bet_payouts[bet] * payout_override)
        self.chips.total_chips += int(winnings)
        print(f'{self.name} new bankroll is {self.chips.total_chips} (excl. wokring bets)\n')

    def lose_bet(self, bet):
        self.bets[bet] = False
        print(f'{self.name} new bankroll is {self.chips.total_chips}\n')
    
    def take_down_bet(self, bet):
        self.chips.total_chips += self.bets[bet]
    
    def reset_bets(self):
        self.bets = dict(craps_bets)
    
class Game:
    def __init__(self):
        self.dice = Dice()
        self.point = 'Off'
        self.players = []
        self.point_established = False
        self.initialize_players()

    def set_point(self, point):
        print(f'Point is set at {point}')
        self.point = point

    def check_pass_wins(self):
        for player in self.players:
            if player.bets['pass'] != False:
                print(f'{player.name} wins on pass line.')
                player.win_bet('pass')
            elif player.bets['dont_pass'] != False:
                if self.dice.current_roll in [self.point, 7, 11]:
                    print(f'{player.name} loses on don\'t pass line.')
                    player.lose_bet('dont_pass')
    
    def check_pass_loses(self):
        for player in self.players:
            if player.bets['pass'] != False:
                print(f'{player.name} loses on pass line.')
                player.lose_bet('pass')
            elif player.bets['dont_pass'] != False:
                if self.dice.current_roll in [2, 3, 7]:
                    print(f'{player.name} wins on don\'t pass line.')
                    player.win_bet('dont_pass')
                elif self.dice.current_roll == 12:
                    print(f'{player.name} has a push on the don\'t pass line.')
    
    def check_place_bets(self):
        for player in self.players:
            for number in place_bets:
                if player.bets[number] != False and int(number) == self.dice.current_roll:
                    print(f'{player.name} wins on the {number}')
                    player.win_bet(number)
                else:
                    continue
    
    def lose_place_bets(self):
        for player in self.players:
            for number in place_bets:
                if player.bets[number] != False:
                    print(f'{player.name} loses on the {number}')
                    player.bets[number] = False
                else:
                    continue
    
    def bring_bets_down(self):
        for player in self.players:
            for key, value in player.bets.items():
                if value != False:
                    player.take_down_bet(key)
    
    def reset_all_bets(self):
        for player in self.players:
            player.reset_bets()

    def bet_menu(self):
        for player in self.players:
            print(f'\n[{player.name}] Bet Menu')
            while True:
                print(f'\nGame Info - [Point]: {self.point} | [Chips]: {player.chips.total_chips}')
                print(f'Current Bets: ', end='')
                for key, value in player.bets.items():
                    if value != False:
                        print(f'{key} - ${value}', end=' | ')
                menu_option = input(f'\n\n| (m)ake a bet | (r)emove bet |\n| (s)ave bet | (re)bet | (d)one | : ')
                menu_option = menu_option.lower()
                if menu_option == 'm':
                    self.bet_menu_make_bet(player)
                elif menu_option == 'r':
                    self.bet_menu_remove_bet(player)
                elif menu_option == 's':
                    player.saved_bets = dict(player.bets)
                    print('Bets saved successfully. Use the (re)bet option to quickly rebet with these saved bets.')
                elif menu_option == 're':
                    if len(player.saved_bets) == 0:
                        print('No bets saved.')
                    else:
                        for key, value in player.saved_bets.items():
                            if value != False and player.bets[key] == False:
                                player.make_bet(key, value)
                elif menu_option == 'd':
                    break
                else:
                    print('Invalid input.')
                
    def bet_menu_make_bet(self, player):
        print(f'\nPrinting available bets for {player.name} to make:')
        for key, value in player.bets.items():
            if key in contract_bets and self.point_established:
                continue
            elif value == False:
                print(f'{key}')
        while True:
            bet_option = input(f'Enter bet name to make bet, or (q) to return to bet menu: ')
            bet_option = bet_option.lower()
            if bet_option == 'q':
                break
            elif bet_option in player.bets.keys():
                if player.bets[bet_option] != False:
                    print('Invalid bet.')
                elif bet_option in contract_bets and self.point_established:
                    print('Invalid bet.')
                else:
                    player.make_bet(bet_option)
            else:
                print('Invalid input.')

    def bet_menu_remove_bet(self, player):
        print(f'\nPrinting available bets for {player.name} to remove:')
        for key, value in player.bets.items():
            if self.point_established and key in contract_bets:
                continue
            elif value != False:
                print(f'{key} - {value}')
        while True:
            bet_option = input(f'Enter bet name to remove bet, or (q) to return to bet menu: ')
            bet_option = bet_option.lower()
            if bet_option == 'q':
                break
            elif bet_option in player.bets.keys():
                if player.bets[bet_option] == False:
                    print('Invalid bet.')
                elif self.point_established and bet_option in contract_bets:
                    print('Invalid bet.')
                else:
                    player.remove_bet(bet_option)
            else:
                print('Invalid input.')

    def game_menu(self):
        print(' - Game Menu -')
        menu_option = input('Would you like to continue playing? (Y)es or (N)o: ')
        menu_option = menu_option.lower()
        while True:
            if menu_option == 'y':
                break
            elif menu_option == 'n':
                print('Thanks for playing!')
                quit()
            else:
                print('Invalid option.')

    def initialize_players(self):
        print('Initializing players (max 10)')
        while len(self.players) < 10:
            player_name = input('Enter player name, or (q) to finish: ')
            if player_name in self.players:
                print('Error, player already exisits. Enter a different name.')
                continue
            elif player_name.lower() == 'q':
                if len(self.players) == 0:
                    print('Error. You need at least 1 player.')
                    continue
                else:
                    break
            else:
                self.players.append(Player(player_name))

    def check_one_roll_bets(self):
        for player in self.players:
            for bet in one_roll_bets:
                if player.bets[bet] != False and self.dice.current_roll in field_bets:
                    print(f'{player.name} wins on the {bet}')
                    if self.dice.current_roll in field_double_payouts:
                        player.win_bet(bet, payout_override=2)
                    else:
                        player.win_bet(bet)
                elif player.bets[bet] != False:
                    print(f'{player.name} loses on the {bet}')
                    player.lose_bet(bet)
                else:
                    continue
    
    def check_hard_way_bets(self):
        for player in self.players:
            for bet in hard_way_bets:
                if player.bets[bet] != False and self.dice.check_hard_ways(bet):
                    print(f'{player.name} wins on the {bet}')
                    player.win_bet(bet)
                elif player.bets[bet] != False and self.dice.check_hard_ways(bet) == False:
                    print(f'{player.name} loses on the {bet}')
                    player.lose_bet(bet)
                else:
                    continue
    
    def lose_hard_way_bets(self):
        for player in self.players:
            for bet in hard_way_bets:
                if player.bets[bet] != False:
                    print(f'{player.name} loses on the {bet}')
                    player.bets[bet] = False

    def reset_game(self):
        self.point = 'Off'
        self.point_established = False
        self.reset_all_bets()
        self.game_menu()

game = Game()

while True:
    while True:
        game.bet_menu()
        game.dice.roll_dice()
        game.check_one_roll_bets()
        game.check_hard_way_bets()

        if game.dice.current_roll in pass_wins:
            if game.dice.current_roll == 7:
                game.lose_place_bets()
                game.lose_hard_way_bets()
            game.check_pass_wins()
        elif game.dice.current_roll in pass_loses:
            game.check_pass_loses()
        else:
            game.set_point(game.dice.current_roll)
            game.point_established = True
            game.check_place_bets()
            break

    while True:
        game.bet_menu()
        game.dice.roll_dice()
        game.check_one_roll_bets()

        if game.dice.current_roll == game.point:
            print('Point hits!\n')
            game.check_hard_way_bets()
            game.check_pass_wins()
            game.check_place_bets()
            game.bring_bets_down()
            break
        elif game.dice.current_roll == 7:
            print('7 out!\n')
            game.check_pass_loses()
            game.lose_place_bets()
            game.lose_hard_way_bets()
            break
        
        game.check_hard_way_bets()
        game.check_place_bets()

    game.reset_game()
