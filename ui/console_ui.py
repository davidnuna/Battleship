# The text-based console user interface

from exceptions.exceptions import InvalidCoordinates, InvalidBattleship, AreaTaken, SquareAlreadyHit
from prettytable import PrettyTable
from copy import deepcopy

class console_ui(object):
    def __init__(self, game_controller):
        self.__game_controller = game_controller
    
    def ui_show_human_maps(self):
        human_game_pretty_table = PrettyTable()
        human_game_pretty_table.field_names = [" ", "A", "B", "C", "D", "E", "F", "G", "H"]
        coordinate_y = 0
        while coordinate_y < 8:
            game_table_copy = deepcopy(self.__game_controller.get_human_visible_map[coordinate_y])
            game_table_copy.insert(0, coordinate_y+1)
            human_game_pretty_table.add_row(game_table_copy)
            coordinate_y += 1
        opponent_game_pretty_table = PrettyTable()
        opponent_game_pretty_table.field_names = [" ", "A", "B", "C", "D", "E", "F", "G", "H"]
        coordinate_y = 0
        while coordinate_y < 8:
            game_table_copy = deepcopy(self.__game_controller.get_computer_invisible_map[coordinate_y])
            game_table_copy.insert(0, coordinate_y+1)
            opponent_game_pretty_table.add_row(game_table_copy)
            coordinate_y += 1
        print("             YOUR  TABLE")
        print(human_game_pretty_table)
        print("             ENEMY TABLE")  
        print(opponent_game_pretty_table)
    
    def ui_show_computer_maps(self):
        computer_game_pretty_table = PrettyTable()
        computer_game_pretty_table.field_names = [" ", "A", "B", "C", "D", "E", "F", "G", "H"]
        coordinate_y = 0
        while coordinate_y < 8:
            game_table_copy = deepcopy(self.__game_controller.get_computer_visible_map[coordinate_y])
            game_table_copy.insert(0, coordinate_y+1)
            computer_game_pretty_table.add_row(game_table_copy)
            coordinate_y += 1
        opponent_game_pretty_table = PrettyTable()
        opponent_game_pretty_table.field_names = [" ", "A", "B", "C", "D", "E", "F", "G", "H"]
        coordinate_y = 0
        while coordinate_y < 8:
            game_table_copy = deepcopy(self.__game_controller.get_human_invisible_map[coordinate_y])
            game_table_copy.insert(0, coordinate_y+1)
            opponent_game_pretty_table.add_row(game_table_copy)
            coordinate_y += 1
        print("             YOUR  TABLE")
        print(computer_game_pretty_table)
        print("             ENEMY TABLE")  
        print(opponent_game_pretty_table)
        

    def ui_place_battleships(self):
        number_of_battleships_placed = 0
        while number_of_battleships_placed != 3:
            try:
                coordinates = input("Coordinates: ").split()
                if len(coordinates) != 5:
                    raise InvalidCoordinates("Invalid coordinates! Please enter the coordinates in the specified format (column line to column line) !\n")
                coordinate_x_start = ord(coordinates[0])-64
                coordinate_y_start = int(coordinates[1])
                coordinate_x_end = ord(coordinates[3])-64
                coordinate_y_end = int(coordinates[4])
                self.__game_controller.place_battleship(coordinate_x_start, coordinate_y_start, coordinate_x_end, coordinate_y_end)
                number_of_battleships_placed += 1
                self.ui_show_human_maps()
            except ValueError:
                print("Invalid coordinates! The chosen rows must be integers !\n")
            except (InvalidCoordinates, InvalidBattleship, AreaTaken) as exception_message:
                print(exception_message)

    def ui_advance_the_game(self):
        game_ended = False
        while game_ended == False:
            try:
                coordinates = input("Coordinates: ").split()
                if len(coordinates) != 2:
                    raise InvalidCoordinates("Invalid coordinates! Please enter the coordinates in the specified format (column line) !\n")
                coordinate_x = ord(coordinates[0])-64
                coordinate_y = int(coordinates[1])
                square_hit = False
                square_hit = self.__game_controller.human_shoot_square(coordinate_x, coordinate_y)
                if square_hit == True:
                    print("Nice shot! It was a clear hit!\n")
                else:
                    print("The shot missed! Try again!\n")
                if self.__game_controller.check_if_game_ended() != False:
                    if self.__game_controller.check_if_game_ended() == "Human":
                        print("You won! You defeated the entire enemy fleet!\n")
                    else:
                        print("You lost! Your fleet has been completely annihilated!\n")
                    return
                square_hit = False
                square_hit = self.__game_controller.computer_shoot_square()[0]
                if square_hit == True:
                    print("The computer hit a part of your fleet! Destroy his before he destroys yours !\n")
                else:
                    print("The computer missed! Nice positioning!\n")
                self.ui_show_human_maps()
                if self.__game_controller.check_if_game_ended() != False:
                    if self.__game_controller.check_if_game_ended() == "Human":
                        print("You won! You defeated the entire enemy fleet!\n")
                    else:
                        print("You lost! Your fleet has been completely annihilated!\n")
                    return
            except ValueError:
                print("Invalid coordinates! The chosen rows must be integers !\n")
            except (InvalidCoordinates, SquareAlreadyHit) as exception_message:
                print(exception_message)
            
        
    def run(self):
        self.__game_controller.place_random_battleships()
        print("Welcome to the Battleship game!")
        print("Let's start by placing your battleships! You can place exactly 3 ships, one of each from the following:")
        print("A battleship (4 squares)")
        print("A cruiser (3 squares)")
        print("A destroyer (2 squares) ")
        print("Please place any of them by typing the 2 desired coordinates (column line to column line): ")
        #self.ui_show_computer_maps()
        self.ui_show_human_maps()
        self.ui_place_battleships()
        print("Great! Now you can start playing the game! Enter the coordinates (column line) of the square you want to shoot down!")
        self.ui_advance_the_game()
        print("Game over! Thanks for playing!\n")
            
            
            
