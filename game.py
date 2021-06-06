"""
Randomized card game

Plays card game against computer using Threads
"""

import threading
import random
import time

HAND_SIZE = 7

class Player(threading.Thread):

    cards = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)

    def __init__(self, id, main, lock):
        threading.Thread.__init__(self)                          # Initialize Thread class
        self.hand = random.choices(Player.cards, k = HAND_SIZE)  # Randomly select 7 cards
        self.id = id
        self.main_pile = main
        self.lock = lock
    
    def run(self):
        while len(self.hand) != 0:

            # max(): This is a sorting algortihm.
            # Place before the lock so both threads run simultaneously.
            next_card = max(self.hand)

            with self.lock:
                # This runs only once to place first card on pile
                if len(self.main_pile) == 0:
                    self.main_pile.append(next_card)
                    time.sleep(0.5)

                # If the game is over, end loop
                elif self.main_pile[-1] == "Game Over":
                    break
                
                # If your card number is higher than the one on top of the pile
                elif self.main_pile[-1] < next_card:
                    # Put card on main pile
                    self.main_pile.append(self.hand.pop())
                    time.sleep(0.5)

                # If your card number if lower than the one on top of the pile
                elif self.main_pile[-1] > next_card:
                    # Put card on main pile
                    self.main_pile.append(self.hand.pop())  
                    # And draw 1
                    self.draw()
                    time.sleep(0.5)

                # If your card is the same as the one on top of the pile
                elif self.main_pile[-1] == next_card:
                    # Discard
                    self.hand.pop()
                    time.sleep(0.5)
                
                print(f"Card on top of pile: {self.main_pile[-1]}")
                # if self.id != "Computer":
                self.get_hand()

        # Let other player/computer know that the game is over
        self.main_pile.append("Game Over")
        # Choose winner
        if len(self.hand) == 0:
            print(f"{self.id} won")

    # Draws card from deck, the card is random  
    def draw(self):
        self.hand.append(random.choice(Player.cards))

    # Prints current hand
    def get_hand(self):
        print(f"{self.id} hand: {self.hand}\n")

def display_rules():
    print("This is a card game.")
    print("Instructions:")
    print("1. Two players grab 7 cards from the card deck (random cards).")
    print("2. Each player puts their highest number card on the")
    print("   pile at the middle if the card is a higher number.")
    print("   than the card that is on top of the pile.")
    print("3. If the card is a lower number, the player stil puts card on the")
    print("   pile but has to draw one.")
    print("4. If the card is the same as the one on top, the player discards.")
    print("5. The player with the empty hand wins!")

def main():
    main_pile = []           # Main pile

    lock = threading.Lock()  # Used to control access to the same pile

    display_rules()
    x = input("Press enter to start...")

    player_1 = Player("Player 1", main_pile, lock)
    computer = Player("Computer", main_pile, lock)

    player_1.get_hand()

    # Start both threads
    player_1.start()
    computer.start()

    # Join both threads
    player_1.join()
    computer.join()
    

if __name__ == '__main__':
    main()