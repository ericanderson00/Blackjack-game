import random
import time

class Player:
    def __init__(self,name,bankroll):
        self.name = name
        self.bankroll = bankroll
        self.hand = []
        
        
    def add_card(self, card):
        self.hand.append(card)
    
    def hand_value(self):
        value = sum(card.value() for card in self.hand)
        aces = sum(1 for card in self.hand if card.rank =='A')
        
        #if the total value is > 21 and aces are present the method adjusts ace from 11 to 1 by subtracting 10
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value
    
    def clear_hand(self):
        self.hand = []        
        
    def __str__(self):
        hand_desc = ', '.join(str(card) for card in self.hand)
        hand_value = self.hand_value()
        return f"{self.name} has: {hand_desc} (Total Value: {hand_value})" 
        
        
#inheritance from Player
class Dealer(Player):
        def __init__(self):
            super().__init__(name="Dealer", bankroll=0)
        
        def should_hit(self):
            return self.hand_value() < 17
        def should_stand(self):
            return self.hand_value() >=17
             
             
class Card:
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit
        
    def value(self):
        if self.rank in ['J', 'Q','K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)
        
    def __str__(self):
         return f"{self.rank} of {self.suit}"
     
class Deck:
    def __init__(self):
         self.cards = [Card(rank,suit) for rank in('2','3','4','5','6','7','8','9','10','J','Q','K','A') for suit in ('Hears','Diamonds','Clubs','Spades')]
         random.shuffle(self.cards)
         
    def deal_card(self):
        return self.cards.pop()
     
     
class Game:
    def __init__(self, player_name, bankroll):
        self.deck = Deck()
        self.player = Player(player_name,bankroll)
        self.dealer = Dealer()
        
    def play_round(self):
        self.player.clear_hand()
        self.dealer.clear_hand()
        self.deck = Deck() #shuffles deck
        
        for _ in range(2): #just do the loop twice... meaning deal 1 card to player and dealer 2 times
            self.player.add_card(self.deck.deal_card())
            self.dealer.add_card(self.deck.deal_card())
            
        #player hitting or standing
        print(self.player)
        while(self.player.hand_value() <= 21):
            action = input("Would you like it hit or stand:").lower()
            if action == 'hit':
                self.player.add_card(self.deck.deal_card())
                print(self.player)
                
                if(self.player.hand_value() > 21):
                    print('Bust! You lose')
                    return -1
                else:
                    break
            elif action == 'stand':
                break
            else:
                print('Invalid input')
        
        #dealer hitting or standing
        print('\nDealers Turn')
        print(self.dealer)
        time.sleep(1)
        
        while(self.dealer.should_hit):
            self.dealer.add_card(self.deck.deal_card())
            print(self.dealer)
            if(self.dealer.hand_value() > 21):
                print('Dealer Bust! You Win')
                return 1
        
        #determining winner
        if(self.player.hand_value() == 21):
            print("Black Jack!")
            return 2
        
        elif self.player.hand_value() > self.dealer.hand_value():
            print("You Win")
            return 1
            
        elif self.player.hand_value() < self.dealer.hand_value():
            print("Dealer Wins")
            return -1
        else:
            print("its a tie")
            return 0
        
    def playGame(self):
        while self.player.bankroll > 0 :
            print(f"\nCurrent bankroll: ${self.player.bankroll}")
            bet = int(input("Enter bet: $"))
            if bet > self.player.bankroll:
                print("insufficient funds")
                continue
            result = self.play_round()
            if result == 1:
                self.player.bankroll += bet
            elif result == 2:
                self.player.bankroll += bet *1.5
            elif result == -1:
                self.player.bankroll -= bet
                
            if(self.player.bankroll <= 0):
                print('Game Over you are out of money')
                break
            
if __name__ == "__main__":
    name = input("Enter your name:")
    bankroll = int(input("Enter how much money to play with: $"))
    game = Game(name, bankroll)
    game.playGame()
            