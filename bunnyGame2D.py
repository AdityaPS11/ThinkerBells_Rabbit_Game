import random
import os
import sys
import curses

class RabbitGame:
    def __init__(self, stdscr):
        self.grid = []
        self.carrot_picked = False
        self.rabbit_row, self.rabbit_col = 0, 0
        self.rabbit_holes = []
        self.carrots = []
        self.stdscr = stdscr

    def generate_2d_map(self, rows, cols):
        # Clear existing data
        self.rabbit_holes.clear()
        self.carrots.clear()

        # Generate an empty 2D map
        self.grid = [['-'] * cols for _ in range(rows)]

        # Place rabbit
        self.rabbit_row = random.randint(0, rows - 1)
        self.rabbit_col = random.randint(0, cols - 1)
        self.grid[self.rabbit_row][self.rabbit_col] = 'r'

        # Generate positions for rabbit holes
        available_positions = [(row, col) for row in range(rows) for col in range(cols)]
        available_positions.remove((self.rabbit_row, self.rabbit_col))

        # Place rabbit holes
        for _ in range(self.num_holes):
            hole_row, hole_col = random.choice(available_positions)
            self.rabbit_holes.append((hole_row, hole_col))
            available_positions.remove((hole_row, hole_col))

        # Place carrots, ensuring they are not adjacent to holes or other carrots
        for _ in range(self.num_carrots):
            carrot_row, carrot_col = random.choice(available_positions)
            adjacent_positions = [
                (carrot_row - 1, carrot_col),
                (carrot_row + 1, carrot_col),
                (carrot_row, carrot_col - 1),
                (carrot_row, carrot_col + 1)
            ]
            adjacent_positions = [
                pos for pos in adjacent_positions
                if (pos in available_positions) and (pos not in self.rabbit_holes)
            ]

            if adjacent_positions:
                carrot_row, carrot_col = random.choice(adjacent_positions)
            else:
                carrot_row, carrot_col = random.choice(available_positions)

            self.carrots.append((carrot_row, carrot_col))
            available_positions.remove((carrot_row, carrot_col))

        # Mark rabbit holes and carrots on the grid
        for hole_row, hole_col in self.rabbit_holes:
            self.grid[hole_row][hole_col] = 'O'
        for carrot_row, carrot_col in self.carrots:
            self.grid[carrot_row][carrot_col] = 'c'

    def print_game(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in self.grid:
            formatted_row = ' '.join(row)
            sys.stdout.write(formatted_row + '\n')
        sys.stdout.flush()

        if (self.rabbit_row, self.rabbit_col) in self.rabbit_holes and not self.carrot_picked:
            sys.stdout.write("\nCongratulations! Mr. Bunny entered the rabbit hole.\nPress Enter to play again or any other key to quit;\n")
            sys.stdout.flush()

    def move_rabbit(self, direction):
        new_row, new_col = self.rabbit_row, self.rabbit_col

        if direction == "a":
            new_col -= 1
        elif direction == "d":
            new_col += 1
        elif direction == "w":
            new_row -= 1
        elif direction == "s":
            new_row += 1
        elif direction == "wa":
            new_row -= 1
            new_col -= 1
        elif direction == "wd":
            new_row -= 1
            new_col += 1
        elif direction == "sa":
            new_row += 1
            new_col -= 1
        elif direction == "sd":
            new_row += 1
            new_col += 1

        # Check if the new position is valid
        if (0 <= new_row < len(self.grid)) and (0 <= new_col < len(self.grid[0])) and (self.grid[new_row][new_col] != 'c') and ((new_row, new_col) not in self.rabbit_holes):
            self.grid[self.rabbit_row][self.rabbit_col] = '-'
            self.rabbit_row, self.rabbit_col = new_row, new_col
            self.grid[self.rabbit_row][self.rabbit_col] = 'r' if not self.carrot_picked else 'R'

    def pick_carrot(self):
        adjacent_positions = [
            (self.rabbit_row - 1, self.rabbit_col),
            (self.rabbit_row + 1, self.rabbit_col),
            (self.rabbit_row, self.rabbit_col - 1),
            (self.rabbit_row, self.rabbit_col + 1)
        ]

        for row, col in adjacent_positions:
            if (0 <= row < len(self.grid)) and (0 <= col < len(self.grid[0])) and self.grid[row][col] == 'c' and not self.carrot_picked:
                self.grid[self.rabbit_row][self.rabbit_col] = 'R'
                self.grid[row][col] = '-'
                self.carrot_picked = True
                break

    def drop_carrot(self):
        adjacent_positions = [
            (self.rabbit_row - 1, self.rabbit_col),
            (self.rabbit_row + 1, self.rabbit_col),
            (self.rabbit_row, self.rabbit_col - 1),
            (self.rabbit_row, self.rabbit_col + 1)
        ]

        for row, col in adjacent_positions:
            if (0 <= row < len(self.grid)) and (0 <= col < len(self.grid[0])) and (row, col) in self.rabbit_holes and self.carrot_picked:
                self.grid[self.rabbit_row][self.rabbit_col] = '-'
                self.rabbit_row, self.rabbit_col = row, col
                self.carrot_picked = False
                self.print_game()
                break

    def jump(self):
        adjacent_holes = [
            (hole_row, hole_col) for hole_row, hole_col in self.rabbit_holes
            if (abs(self.rabbit_row - hole_row) == 1 and self.rabbit_col == hole_col) or
               (abs(self.rabbit_col - hole_col) == 1 and self.rabbit_row == hole_row)
        ]
        
        if adjacent_holes:
            hole_row, hole_col = adjacent_holes[0]
            self.grid[self.rabbit_row][self.rabbit_col] = '-'
        
            if abs(self.rabbit_row - hole_row) == 1 and self.rabbit_col == hole_col:
                if self.rabbit_row < hole_row:
                    self.rabbit_row = hole_row + 1
                else:
                    self.rabbit_row = hole_row - 1
            elif abs(self.rabbit_col - hole_col) == 1 and self.rabbit_row == hole_row:
                if self.rabbit_col < hole_col:
                    self.rabbit_col = hole_col + 1
                else:
                    self.rabbit_col = hole_col - 1
        
            self.grid[self.rabbit_row][self.rabbit_col] = 'r' if not self.carrot_picked else 'R'

    def main(self):
        while True:
            self.stdscr.clear()
            self.stdscr.addstr("Instructions\nPress Enter to play the game; Press any other key to quit;")
            key = self.stdscr.getch()
            if key != ord('\n'):
                curses.endwin()
                return
            
            curses.echo()
            self.stdscr.addstr("\nEnter the number of rows: ")
            self.stdscr.refresh()
            rows = int(self.stdscr.getstr().decode())

            self.stdscr.addstr("\nEnter the number of columns: ")
            self.stdscr.refresh()
            cols = int(self.stdscr.getstr().decode())
            
            self.stdscr.addstr("Enter the number of carrots (more than 1): ")
            self.stdscr.refresh()
            self.num_carrots = int(self.stdscr.getstr().decode())
            
            self.stdscr.addstr("\nEnter the number of rabbit holes (more than 1): ")
            self.stdscr.refresh()
            self.num_holes = int(self.stdscr.getstr().decode())
            
            curses.noecho()  # Disable text input echoing
            self.generate_2d_map(rows, cols)
            self.play()

    def play(self):
        while True:
            while True:
                self.print_game()

                action = self.stdscr.getch()

                if action == ord('q'):
                    curses.endwin()
                    break
                elif action == ord('a') or action == ord('d') or action == ord('w') or action == ord('s'):
                    self.move_rabbit(chr(action))
                elif action == ord('p'):
                    if self.carrot_picked:
                        self.drop_carrot()
                    else:
                        self.pick_carrot()
                elif chr(action) in ['wa', 'wd', 'sa', 'sd']:
                    self.move_rabbit(chr(action))
                elif action == ord('j'):
                    self.jump()

                if (self.rabbit_row, self.rabbit_col) in self.rabbit_holes and not self.carrot_picked:
                    self.print_game()
                    play_again = self.stdscr.getch()
                    self.stdscr.clear()
                    if play_again != ord('\n'):
                        curses.endwin()
                        sys.exit()
                    else:
                        break
            else:
                continue
            break

def main(stdscr):
    game = RabbitGame(stdscr)
    game.main()

if __name__ == "__main__":
    curses.wrapper(main)
