import random
import os
import sys
# Bunny_Hungry_Game
class RabbitGame:
    def __init__(self, cols):
        # Initialize the RabbitGame class with specified number of columns
        self.cols = cols
        self.grid = ['-'] * cols
        self.carrot_picked = False
        self.rabbit_col = 0
        self.rabbit_hole_col = 0
        self.carrot_col = 0
        self.place_elements() # Initialize game elements

    def place_elements(self):
        # Generate random positions for rabbit, rabbit hole, and carrot
        self.rabbit_col = random.randint(0, self.cols - 1)
        self.grid[self.rabbit_col] = 'r'
        
        # Ensure rabbit hole is placed at a different position from rabbit
        self.rabbit_hole_col = random.randint(0, self.cols - 1)
        while self.rabbit_hole_col == self.rabbit_col:
            self.rabbit_hole_col = random.randint(0, self.cols - 1)
        self.grid[self.rabbit_hole_col] = 'O'
        
        # Ensure carrot is placed at a different position from rabbit and hole
        self.carrot_col = random.randint(0, self.cols - 1)
        while self.carrot_col == self.rabbit_col or self.carrot_col == self.rabbit_hole_col:
            self.carrot_col = random.randint(0, self.cols - 1)
        self.grid[self.carrot_col] = 'c'

    def print_game(self):
        # Clear the terminal and print the current game state
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.stdout.write('\r' + ''.join(self.grid))
        sys.stdout.flush()

    def play(self):
        while True:
            self.print_game() # Display the current game state
            
            action = input("\nWhat do you want to do? (a/d/p/j/quit): ").lower()
            
            if action == "quit":
                print("\nThanks for playing!")
                break
            elif action == "a" or action == "d":
                self.move_rabbit(action)
            elif action == "p":
                # Check if rabbit is adjacent to the carrot and the carrot is not picked
                if abs(self.rabbit_col - self.carrot_col) == 1 and not self.carrot_picked:
                    self.pick_carrot() # Pick the carrot
                # Check if rabbit is adjacent to the rabbit hole and the carrot is picked
                elif abs(self.rabbit_col - self.rabbit_hole_col) == 1 and self.carrot_picked:
                    self.drop_carrot() # Drop the carrot into the rabbit hole
            elif action == "j":
                self.jump() # Make the rabbit jump across the hole
            else:
                print("Invalid action. Try again.")
    
            # Check if the rabbit is adjacent to the hole and the carrot is dropped,changing R to C
            if self.grid[self.rabbit_col] =='C':
                self.end_game()

    def move_rabbit(self, direction):
        new_col = self.rabbit_col
        
        if direction == "a":
            new_col -= 1
        elif direction == "d":
            new_col += 1
        # Check if the new column is within bounds, not a carrot, and not the rabbit hole
        if (0 <= new_col < self.cols) and (self.grid[new_col] != 'c') and (new_col != self.rabbit_hole_col):
            self.grid[self.rabbit_col] = '-' # Clear the current rabbit position
            self.rabbit_col = new_col # Update the rabbit's new position
            self.grid[self.rabbit_col] = 'r' if not self.carrot_picked else 'R' # Update grid with new rabbit position

    def pick_carrot(self):
        # Check if rabbit is adjacent to the left or right of the carrot and the carrot is not picked
        if (self.rabbit_col == self.carrot_col - 1 and not self.carrot_picked) or \
           (self.rabbit_col == self.carrot_col + 1 and not self.carrot_picked):
                self.grid[self.rabbit_col] = 'R' # Update grid to show rabbit with picked carrot
                self.grid[self.carrot_col] = '-'
                self.carrot_picked = True


    def drop_carrot(self):
        # Check if rabbit is adjacent to the left or right of the rabbit hole and the carrot is picked
        if (self.rabbit_col == self.rabbit_hole_col - 1 and self.carrot_picked) or \
           (self.rabbit_col == self.rabbit_hole_col + 1 and self.carrot_picked):
                self.grid[self.rabbit_col] = 'C' # Update grid to show rabbit with dropped carrot
                self.carrot_picked = False

    def jump(self):
        # Check if rabbit is adjacent to the left or right of the rabbit hole
        if abs(self.rabbit_col - self.rabbit_hole_col) == 1:
            self.grid[self.rabbit_col] = '-'
            # Calculate new rabbit position based on the direction of the hole
            self.rabbit_col = self.rabbit_hole_col + 1 if self.rabbit_col < self.rabbit_hole_col else self.rabbit_hole_col - 1
             # Update grid with new rabbit position, considering if carrot is picked or not
            self.grid[self.rabbit_col] = 'r' if not self.carrot_picked else 'R'

    def end_game(self):
        self.print_game() # Display the final game state
        print("\nCongratulations! Mr. Bunny collected the carrot and dropped it in the rabbit hole.")
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again == "yes":
            self.grid = ['-'] * self.cols
            self.carrot_picked = False
            self.place_elements()
            self.play() # Restart the game loop

if __name__ == "__main__":
    cols = 50 # Define the number of columns for the game
    game = RabbitGame(cols) # Create an instance of the RabbitGame class with the specified number of columns
    try:
        game.play()
    except KeyboardInterrupt:
        print("\nGame terminated by user.") # Handle termination if the user interrupts the game
 