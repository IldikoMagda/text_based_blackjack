### text based blackjack game with computer dealer and human player###
##rules in this case##
#player must have a bank or account with their accumulated chips
#human can place bets 
# human starts with 2 cards open 
# comp starts with 1 card open 1 closed -- "dealer upcard"
#player goal: get closer to 21 than dealer 
# player can "hit" ---> get another card 
# player can "stand" ---> stop getting cards
#face cards count as a value of 10
#aces can count as 1 or 11, favourably to the player
#dealer goes until 17 or higher or bust 
#then it's compared to player card values. can be a tie!!! bets go back to player
#double: player can double if they have 2 cards. this means the bet is doubled
# and the player only gets 1 additional card

import random
from time import sleep
import os 

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':1}


class Card:
    "This class creates each card"
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Player:
    "This class creates player, its hand, which is empty upon creation"
    def __init__(self,name, balance = 100):
        self.name = name
        # A new player has no cards
        self.all_cards = []
        self.balance = balance
        #self.handvalue = handvalue


    def __str__(self):
        return f"{self.name} has {len(self.all_cards)} cards and £{self.balance}"

    def get_name(self):
        return self.name

    def show_cards(self):
        for i in range(len(self.all_cards)):
            print(self.all_cards[i])
        #return self.all_cards #not sure this is neccessary, we'll see

    def add_cards(self,new_cards):
        if type(new_cards) == type([]):
            self.all_cards.extend(new_cards)
        else:
            self.all_cards.append(new_cards)

    def reset_hand(self):
        #this will reset player hand after each round
        self.all_cards = []
        #I don't think you need to return this btw 
        return self.all_cards

class Account(Player):
    "This class will handle player account that can be used to put bets"
    "This will also hold the dealer's 'account' "
    def __init__(self,classplayer):
        self.name = classplayer.name
        self.balance = classplayer.balance

    def get_balance(self):
        return self.balance    

    def __str__(self): 
        return (f"{self.name}'s account has £{self.balance}")

    def add_to_account(self, amount):
        self.balance = self.balance + amount

    def take_from_account(self, amount):
        if self.balance - amount  > 0 or self.balance - amount == 0: 
            self.balance = self.balance - amount
        else: 
            print("You don't have enough chips to use")
            print(f"You have {self.balance}")
 
class Dealer: 
    "This class will have cards in hand, an upcard and will be able to hit or stand"
    def __init__(self):
        self.whole_hand = []
        self.balance =100000000

    def __str__(self):
        return f"The dealer has {len(self.whole_hand)} cards and the upcard is ..."

    def get_dealer_balance(self):
        return self.balance

    def upcard(self):
        upcard = self.whole_hand[0]
        return upcard
    
    def dealer_allcards(self):
        return self.whole_hand

    def add_cards(self,new_cards):
        if type(new_cards) == type([]):
            self.whole_hand.extend(new_cards)
        else:
            self.whole_hand.append(new_cards)

    def show_dcards(self):
        for i in range(len(self.whole_hand)):
            print(self.whole_hand[i])

    def reset_hand(self):
        #this will reset dealer hand after each round
        self.whole_hand = []
        return self.whole_hand


class Deck:
    "This class will have the whole deck of cards. Shuffle method, deal method"
        
    def __init__(self):
        # Note this only happens once upon creation of a new Deck
        self.all_cards = [] 
        for suit in suits:
            for rank in ranks:
                # This assumes the Card class has already been defined!
                self.all_cards.append(Card(suit,rank))
                
    def shuffle(self):
        # Note this doesn't return anything, shuffle in place
        random.shuffle(self.all_cards)

    def deal_one(self):
        # Note we remove one card from the list of all_cards
        return self.all_cards.pop()

class UserInput:
    "This class handles all methods requiring user inputs for the game. E.g: hit or stand or to continue playing"
    
    def __init__(self,human, bet, move):
        self.human = human
        self.bet = bet
        self.move = move

    @staticmethod
    def get_username():
        human = input("Who am I playing with today? ")
        return human

    @staticmethod
    def get_bet():
        bet = "string"
        while type(bet) == str:
                bet = input("Place your bet: ")
                try: 
                    bet = float(bet)
                    return bet
                except:
                    print("please enter how much you'd like to bet using numbers ")
                    bet = "string"
    @staticmethod
    def hit_or_stand():
        moves = ["H", "S"]
        move = ""
        while move not in moves:
            move = input("Hit or Stand next? Press H or S ").upper()
            return move

    @staticmethod
    def hit_stand_or_double():
        firstmoves = ["H", "S", "D"]
        move = ""
        while move not in firstmoves:
            move = input("Hit or Stand or Double? Press H or S or D ").upper()
            return move

    @staticmethod
    def play_again():
        playmore = ["Y", "N"]
        quitornot = "maybe"
        while quitornot not in playmore:
            quitornot = input("Would you like to continue playing? Y/N? ").upper()
            return quitornot
        
class WinCheck:
    " This class handles all logic and method to decide who won the round of blackjack"
    def __init__(self, dealerhand, playerhand):
        #look for player whole hand and dealer whole hand
        self.dealerhand = Dealer.whole_hand #list
        self.playerhand = Player.all_cards #list[i].value -->int 
        self.run() # trying to get checks run automatically

    @staticmethod
    def ace_or_not(cards):
        eachcardrank =[]
        for i in cards: 
            eachcardrank.append(i.rank)
        if 'Ace' in eachcardrank:
            return True
        else:
            return False

    def run(self):
        self.ace_or_not() #check if there is an ace
        self.check_over21() #check if anyone busted

    @staticmethod
    def original_value(hand):
        value = 0 
        for i in range(len(hand)):
            value = value + hand[i].value
        return value

    @staticmethod
    def ace_11_value(hand):
        value = 10 
        for i in range(len(hand)):
            value = value + hand[i].value
        return value 

    @staticmethod
    def check_over21(handvalue):
        if handvalue > 21:
            over21 = True
            return over21
        else:
            over21 = False
            return over21 #return false 

    @staticmethod
    def check_over17(handvalue):
        if handvalue >= 17:
            return True 
        else:
            return False

    @staticmethod
    def win_check_by_compare(dealervalue, playervalue):
        #check winner when noone busted
        #boolean, dealer is winner by default
        #returns one when tie
        dealerwin =True
        tie = 1
        dealer = 21 - dealervalue #difference between 21 and cards in hand  0
        player = 21 - playervalue # 4
        if player > dealer: 
            return dealerwin
        elif player ==dealer:
            return tie
        else:
            return dealerwin == False


game_on = True 
while game_on: 
    #set game 

    #set player 
    name1 = UserInput.get_username()
    player = Player(name1)
    #set dealer
    dealer = Dealer()
    #set account 
    playeraccount = Account(player)

    eachround = True 

    while eachround:
        #set deck 
        mydeck = Deck()
        #shuffle deck 
        mydeck.shuffle()
        
        # deal initial cards to players 
        #player cards
        player.add_cards(mydeck.deal_one())
        player.add_cards(mydeck.deal_one())

        #dealer cards 
        dealer.add_cards(mydeck.deal_one())
        dealer.add_cards(mydeck.deal_one())

        #show cards and dealer upcard
        print(player)
        sleep(1)
        player.show_cards()
        sleep(2.5)
        print(dealer)
        upcard = dealer.upcard()
        print(upcard)
        sleep(2)

        #get user bets
        bet = UserInput.get_bet()

        #player moves
        move_counter = 1
        move_on = True
        #hit/stand/double 
        first_move = UserInput.hit_stand_or_double() # returns a string

        #win variables 
        pl_win = False
        dl_win = False
        tie = False


        #player can only double in the first round
        while move_counter == 1 and move_on:
            if first_move == "D": #double
                player.add_cards(mydeck.deal_one())
                bet = bet *2
                move_counter += 1
                player.show_cards()
                move_on == False
                break          
            
            if first_move == "H": #hit
                player.add_cards(mydeck.deal_one())
                sleep(1)
                print("You have these cards now: ")
                move_counter += 1
                player.show_cards() 
                move_on == True

            if first_move =="S": #stand 
                move_counter += + 1
                move_on ==False
                break 

            #player move choice after 1st round: hit/stand
            while move_on and move_counter != 1:
                #check value with ace ==1 
                original_value = WinCheck.original_value(player.all_cards)
                #check if player busted
                bust = WinCheck.check_over21(original_value)
                #if over 21, round over
                if bust:
                    move_on == False
                    print("Player Busted")
                    dl_win =True
                    #maybe break out too much 
                    break


                else:
                    #hit/stand
                    more_moves = UserInput.hit_or_stand()

                    if more_moves == "H":
                        player.add_cards(mydeck.deal_one())
                        sleep(1)
                        player.show_cards()
                        sleep(2)
                        #check value with ace ==1 
                        player_handvalue = WinCheck.original_value(player.all_cards)
                        #check if player busted-- bool 
                        bust = WinCheck.check_over21(player_handvalue)
                        #if over 21, round over
                        if bust:
                            move_on == False
                            print("Over 21!! ")
                            dl_win = True
                            break 
                        else:
                            move_counter += 1
                            move_on = True
                    
                    else:
                        move_on == False
                        break
 
        pl_hand_value = WinCheck.original_value(player.all_cards)
        #check if player busted-- bool 
        bust = WinCheck.check_over21(pl_hand_value)
        #if over 21, round over
        if bust: 
            # round over, player lost
            print("Player Busted. The dealer won this round") 
            dl_win = True
            break 
        else: 
            # dealer gets cards until it is => 17 --> first check values 
            dealer_hand = dealer.whole_hand
            player_hand = player.all_cards
            #check for ace 
            ace_round = WinCheck.ace_or_not(dealer_hand)
            dhand_original_value = WinCheck.original_value(dealer_hand) #int 
            dbust = WinCheck.check_over21(dhand_original_value) 
            dstand = WinCheck.check_over17(dhand_original_value)
            #player with ace 11 value
            pl_softhand_value = WinCheck.ace_11_value(player_hand)
            #bool
            pl_ace_round = WinCheck.ace_or_not(player_hand)
                       
            #first round stand on dealer/no ace
            if dbust == False and dstand == True and ace_round == False:
                    #show hand value of dealer
                    print(f"The dealer has {dhand_original_value} in his hand")
                    sleep(1)
                    print("Let's compare hands")
                    sleep(2)
                    print("The dealer had these cards: ")
                    dealer.show_dcards()
                    
                    if pl_ace_round == False: 
                        #check winner 
                        #returns true if dealer wins 
                        #1 if tie
                        winner = WinCheck.win_check_by_compare(dhand_original_value,pl_hand_value)

                        #bets sorting function 
                        if winner == False: 
                            print("Player Won")
                            pl_win = True
                        elif winner == True: 
                            print("The dealer won this round")
                            dl_win = True

                        else: 
                            print("We've got a tie, all bets go back without loss")
                            tie = True
                    
                    #player has an ace/ dealer no ace
                    if pl_ace_round == True:

                        winnersoft = WinCheck.win_check_by_compare(dhand_original_value,pl_softhand_value)
                        winnerhard = WinCheck.win_check_by_compare(dhand_original_value,pl_hand_value)
                        
                        if winnersoft or winnerhard == False: 
                            print("Player won")
                            pl_win = True
                        elif winnersoft and winnerhard == True:
                            print("The dealer won this round")
                            dl_win =True
                        else: 
                            print("We've got a tie, all bets go back without loss")
                            tie = True


            ####DEALER NO ACE #####
            while ace_round == False and dstand ==False and dbust == False: 
                print("It's time for the dealer to get some cards ")
                sleep(2)
                dealer.add_cards(mydeck.deal_one())
                print("Now the dealer has the following cards: ")
                sleep(3)
                dealer.show_dcards()
                dhand_value = WinCheck.original_value(dealer_hand)
                dbust = WinCheck.check_over21(dhand_value)
                dstand = WinCheck.check_over17(dhand_value) #bool
                ace_round = WinCheck.ace_or_not(dealer_hand)

                if dbust == True:
                    #show dealer hand value 
                    print(f"The dealer has {dhand_value} in his hand")
                    sleep(1.5)
                    print("Dealer busted!! ")
                    sleep(0.5)
                    print("You won this round.")
                    pl_win = True
                    break
                if dstand == True: 
                    #show hand value of dealer
                    print(f"The dealer has {dhand_value} in his hand")
                    sleep(1.5)
                    print("Let's compare hands")
                    sleep(1.5)
                    
                    if pl_ace_round == False: 
                        #check winner 
                        #returns true if dealer wins 
                        #1 if tie
                        winner = WinCheck.win_check_by_compare(dhand_value,pl_hand_value)

                        if winner == False: 
                            sleep(0.5)
                            print("Player Won")
                            pl_win = True
                            break
                        if type(winner) ==int : 
                            sleep(0.5)
                            print("We've got a tie, all bets go back without loss")
                            tie = True
                            break
                        if winner == True:
                            sleep(0.5) 
                            print("The dealer won this round")
                            dl_win = True 
                            break
                    
                    #player has an ace/ dealer no ace
                    if pl_ace_round == True:

                        winnersoft = WinCheck.win_check_by_compare(dhand_value,pl_softhand_value)
                        winnerhard = WinCheck.win_check_by_compare(dhand_value,pl_hand_value)
                        
                        # true if dealer wins 
                        if winnersoft == False or winnerhard == False: 
                            sleep(0.5)
                            print("Player won")
                            pl_win = True

                        elif winnersoft and winnerhard == True:
                            sleep(0.5)
                            print("The dealer won this round")
                            dl_win = True
                            
                        else: 
                            sleep(0.5)
                            print("We've got a tie, all bets go back without loss") 
                            tie = True

            ###DEALER ACE ROUND #####
            while ace_round == True:
                new_dhand_softvalue = WinCheck.ace_11_value(dealer_hand) #int
                new_dhand_hardvalue = WinCheck.original_value(dealer_hand)
                dbust = WinCheck.check_over21(new_dhand_hardvalue) #3
                dstand = WinCheck.check_over17(new_dhand_softvalue) #13
                #player ace round 
                #bool
                pl_ace_round = WinCheck.ace_or_not(player_hand)
                print("The dealer has these cards now: ")
                sleep(0.7)
                dealer.show_dcards()

                if dbust == True:
                    sleep(1)
                    print("player has won this round. You won:  You now have: ")
                    pl_win = True
                    ace_round = False
                    break

                if dstand == True:
                    #ace round stand  on dealer /player no ace
                    print("let's compare hands now")
                    sleep(0.5)
                    if pl_ace_round == False: 
                        #check winner 
                        #returns true if dealer wins 
                        #1 if tie
                        winner = WinCheck.win_check_by_compare(new_dhand_softvalue,pl_hand_value)
                        if winner == False: 
                            print("Player Won")
                            pl_win = True
                            break
                        elif type(winner) == int: 
                            print("We've got a tie, all bets go back without loss")
                            tie = True
                            break
                        else: 
                            print("The dealer won this round")
                            dl_win = True

                    #ace round stand on dealer /player has ace 
                    if pl_ace_round == True: 
                        #check winner 
                        #returns true if dealer wins 
                        #1 if tie
                        print("time to compare hands and see who wins this time: ")
                        sleep(0.7)
                        winnersoft = WinCheck.win_check_by_compare(new_dhand_softvalue,pl_softhand_value)
                        winnerhard = WinCheck.win_check_by_compare(new_dhand_softvalue,pl_hand_value)
                        
                        if winnersoft == False or winnerhard == False: 
                            print("Player won")
                            pl_win = True
                            break
                        elif winnersoft == True and winnerhard == True:
                            print("The dealer won this round")
                            dl_win = True
                            break
                        if type(winnersoft)==int and winnerhard == True: 
                            print("We've got a tie, all bets go back without loss")
                            tie = True 
                        if type(winnerhard)==int and winnersoft == True: 
                            print("We've got a tie, all bets go back without loss")
                            tie = True 

                    
                    ace_round = False
                    break

    
        
        #### here comes the bets sorting#### 
        if pl_win == True: 
            #bet added to account, keep bet
            #shall I add 1.5X if blackjack?
            Account.add_to_account(player,bet)
            print(f'You now have £ {player.balance}')
            
        if dl_win == True: 
            Account.take_from_account(player, bet)
            print(f"You lost your bet. Now you have £ {player.balance}")
            Account.add_to_account(dealer, bet)

        if tie == True:
            print(f"All bets went back")
            print(f"{player.name} has £ {player.balance} at the moment")

        ### ask to play again with the same account
        answer = UserInput.play_again()
        
        if answer == 'N':
            game_on = False
            break
        
        else: 
            #reset hands if play again # 
            Dealer.reset_hand(dealer)
            Player.reset_hand(player)

        # clear console 

        clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        clearConsole()
