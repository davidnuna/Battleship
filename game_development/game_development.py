# Them module that contains the game_development class

from coordinates import coordinates
from exceptions.exceptions import AreaTaken
import random
from copy import deepcopy

class game_development(object):
    def __init__(self, validator, human_player, computer_player):
        # The constructor of this class
        # Input: self - the current object
        #        validator - an object of type validation, used to validate input
        #        human_player - an object of type player, the human player
        #        computer_player - an object of type player, the computer player
        self.__validator = validator
        self.__human_player = human_player
        self.__computer_player = computer_player
        self.__placed_ships = []
        self.__human_battleships_squares = 9
        self.__computer_battleships_squares = 9 
        self.__previous_shot_hit = False
        self.__high_chance_squares_stack = []
        self.__hunt_mode = False
    
    @property
    def get_human_visible_map(self):
        # Getter for the 'ally_visible_map' of the player instance
        # Input: self - the current object
        # Output: the table of the human player
        return self.__human_player.get_ally_visible_map
    
    @property
    def get_computer_invisible_map(self):
        # Getter for the 'enemy_invisible_map' of the player instance
        # Input: self - the current object
        # Output: the current table of the computer player
        return self.__human_player.get_enemy_invisible_map
    
    @property
    def get_computer_visible_map(self):
        # Getter for the 'ally_visible_map' of the player instance
        # Input: self - the current object
        # Output: the table of the human player
        return self.__computer_player.get_ally_visible_map
    
    @property
    def get_human_invisible_map(self):
        # Getter for the 'enemy_invisible_map' of the player instance
        # Input: self - the current object
        # Output: the current table of the human player
        return self.__computer_player.get_enemy_invisible_map
    
    def reset_game(self):
        # Functions that resets the game
        # Input: self - the current object
        # Output: nothing
        self.__placed_ships = []
        self.__human_battleships_squares = 9
        self.__computer_battleships_squares = 9 
        self.__previous_shot_hit = False
        self.__high_chance_squares_stack = []
        self.__hunt_mode = False
        self.__human_player.reset_table()
        self.__computer_player.reset_table()

    def place_random_battleships(self):
        # Places the 3 battleships randomly for the computer player
        # Input: self - the current object
        # Output: nothing
        number_of_battleships_placed = 0
        while number_of_battleships_placed != 3:
            coordinate_x_start = random.randrange(1,9)
            coordinate_y_start = random.randrange(1,9)
            coordinate_x_end = random.randrange(1,9)
            coordinate_y_end = random.randrange(1,9)
            ship_start_coordinates = coordinates(coordinate_x_start, coordinate_y_start)
            ship_end_coordinates = coordinates(coordinate_x_end, coordinate_y_end)
            try:
                self.__validator.validate_double_coordinates(ship_start_coordinates, ship_end_coordinates, self.__placed_ships)
                self.__computer_player.add_new_battleship(ship_start_coordinates, ship_end_coordinates, self.__placed_ships[-1])
                number_of_battleships_placed += 1
            except AreaTaken:
                self.__placed_ships.pop()         
            except Exception:
                pass

        self.__placed_ships = []
            
    def place_battleship(self, coordinate_x_start, coordinate_y_start, coordinate_x_end, coordinate_y_end):
        # Creates the object of type 'coordinates', validates it and tries to add a battleship at the given coordinates
        # Input: self - the current object
        #        coordinate_x_start - an integer, the x coordinate of the starting coordinates
        #        coordinate_y_start - an integer, the y coordinate of the starting coordinates
        #        coordinate_x_end - an integer, the x coordinate of the ending coordinates
        #        coordinate_y_end - an integer, the y coordinate of the ending coordinates    
        # Output: nothing
        # Raises: AreaTaken, InvalidCoordinates ( raises to the user interface class from the validates class )
        ship_start_coordinates = coordinates(coordinate_x_start, coordinate_y_start)
        ship_end_coordinates = coordinates(coordinate_x_end, coordinate_y_end)
        self.__validator.validate_double_coordinates(ship_start_coordinates, ship_end_coordinates, self.__placed_ships)
        try:
            self.__human_player.add_new_battleship(ship_start_coordinates, ship_end_coordinates, self.__placed_ships[-1])
        except AreaTaken as exception_message:
            self.__placed_ships.pop()
            raise AreaTaken(exception_message)
        
    def human_shoot_square(self, coordinate_x, coordinate_y):
        # Shoots a square as the human player
        # Input: self - the current object
        #        coordinate_x - an integer, the x coordinate
        #        coordinate_y - an integer, the y coordinate
        # Output: square_hit - a boolean type, True if the square contained a battleship, False otherwise
        # Raises: InvalidCoordinates ( raises to the user interface class from the validates class ) 
        coordinates_to_attack = coordinates(coordinate_x, coordinate_y)
        self.__validator.validate_single_coordinates(coordinates_to_attack)
        square_hit = self.__human_player.launch_attack(coordinates_to_attack)
        if square_hit == True:
            self.__computer_battleships_squares -= 1
        return square_hit
            
                
    def check_if_game_ended(self):
        # Checks if the game ended
        # Input: self - the current object
        # Output: square_hit - a boolean type, True if the square contained a battleship, False otherwise
        # Raises: InvalidCoordinates ( raises to the user interface class from the validates class ) 
        if self.__human_battleships_squares == 0:
            return "Computer"
        elif self.__computer_battleships_squares == 0:
            return "Human"
        return False
    
    def computer_shoot_square(self):
        # Shoots a square as the computer player
        # Input: self - the current object
        # Output: a list containing: square_hit - a boolean type, True if the square contained a battleship, False otherwise
        #                            coordinates_to_attack - an object of type coordinates, the coordinates at which the computer launched the attack
        # Raises: InvalidCoordinates ( raises to the user interface class from the validates class ) 
        while True:
            try:
                if self.__high_chance_squares_stack == []:
                    # If the stack is empty it means the computer is in hunt mode, so it will choose the squares with the highest probability of containing a ship
                    coordinates_to_attack = game_development.probability_map(self)
                    self.__hunt_mode = True
                else:
                    # If the stack is not empty, it will pick the coordinates from the stack and fire at it
                    square_from_stack = self.__high_chance_squares_stack.pop() 
                    coordinates_to_attack = coordinates(square_from_stack[1], square_from_stack[2])
                    self.__hunt_mode = False
                square_hit = self.__computer_player.launch_attack(coordinates_to_attack)
                if square_hit == True:
                    self.__human_battleships_squares -= 1
                    if self.__hunt_mode == True and self.__high_chance_squares_stack == []:
                        # If the shot was a success and the computer was in hunt mode, we add the 4 neighboring squares to the stack
                        if game_development.coordinates_in_range(self.__computer_player.get_enemy_invisible_map, coordinates_to_attack.get_coordinate_x-1-1, coordinates_to_attack.get_coordinate_y-1):
                            self.__high_chance_squares_stack.append(["LEFT", coordinates_to_attack.get_coordinate_x-1, coordinates_to_attack.get_coordinate_y]) 
                        if game_development.coordinates_in_range(self.__computer_player.get_enemy_invisible_map, coordinates_to_attack.get_coordinate_x-1, coordinates_to_attack.get_coordinate_y-1-1):
                            self.__high_chance_squares_stack.append(["UP", coordinates_to_attack.get_coordinate_x, coordinates_to_attack.get_coordinate_y-1]) 
                        if game_development.coordinates_in_range(self.__computer_player.get_enemy_invisible_map, coordinates_to_attack.get_coordinate_x+1-1, coordinates_to_attack.get_coordinate_y-1):
                            self.__high_chance_squares_stack.append(["RIGHT", coordinates_to_attack.get_coordinate_x+1, coordinates_to_attack.get_coordinate_y]) 
                        if game_development.coordinates_in_range(self.__computer_player.get_enemy_invisible_map, coordinates_to_attack.get_coordinate_x-1, coordinates_to_attack.get_coordinate_y+1-1):
                            self.__high_chance_squares_stack.append(["DOWN", coordinates_to_attack.get_coordinate_x, coordinates_to_attack.get_coordinate_y+1]) 
                    else:
                        # If the shot was a success and the computer was not in hunt mode, we add the next square to the stack and only keep in it the coordinates following the given direction ( horizontal or vertical )
                        if square_from_stack[0] == "LEFT" and game_development.coordinates_in_range(self.__computer_player.get_enemy_invisible_map, coordinates_to_attack.get_coordinate_x-1-1, coordinates_to_attack.get_coordinate_y-1):
                            self.__high_chance_squares_stack.append(["LEFT", coordinates_to_attack.get_coordinate_x-1, coordinates_to_attack.get_coordinate_y]) 
                            old_stack = deepcopy(self.__high_chance_squares_stack)
                            self.__high_chance_squares_stack = [element_in_stack for element_in_stack in old_stack if element_in_stack[0] == "LEFT" or element_in_stack[0] == "RIGHT"]
                        elif square_from_stack[0] == "UP" and game_development.coordinates_in_range(self.__computer_player.get_enemy_invisible_map, coordinates_to_attack.get_coordinate_x-1, coordinates_to_attack.get_coordinate_y-1-1):
                            self.__high_chance_squares_stack.append(["UP", coordinates_to_attack.get_coordinate_x, coordinates_to_attack.get_coordinate_y-1]) 
                            old_stack = deepcopy(self.__high_chance_squares_stack)
                            self.__high_chance_squares_stack = [element_in_stack for element_in_stack in old_stack if element_in_stack[0] == "UP" or element_in_stack[0] == "DOWN"]
                        elif square_from_stack[0] == "RIGHT" and game_development.coordinates_in_range(self.__computer_player.get_enemy_invisible_map, coordinates_to_attack.get_coordinate_x+1-1, coordinates_to_attack.get_coordinate_y-1):
                            self.__high_chance_squares_stack.append(["RIGHT", coordinates_to_attack.get_coordinate_x+1, coordinates_to_attack.get_coordinate_y])
                            old_stack = deepcopy(self.__high_chance_squares_stack)
                            self.__high_chance_squares_stack = [element_in_stack for element_in_stack in old_stack if element_in_stack[0] == "LEFT" or element_in_stack[0] == "RIGHT"]
                        elif square_from_stack[0] == "DOWN" and game_development.coordinates_in_range(self.__computer_player.get_enemy_invisible_map, coordinates_to_attack.get_coordinate_x-1, coordinates_to_attack.get_coordinate_y+1-1):
                            self.__high_chance_squares_stack.append(["DOWN", coordinates_to_attack.get_coordinate_x, coordinates_to_attack.get_coordinate_y+1]) 
                            old_stack = deepcopy(self.__high_chance_squares_stack)
                            self.__high_chance_squares_stack = [element_in_stack for element_in_stack in old_stack if element_in_stack[0] == "UP" or element_in_stack[0] == "DOWN"]
                    self.__previous_shot_hit = True
                else:
                    self.__previous_shot_hit = False
                return [square_hit, coordinates_to_attack]
            except Exception:
                pass
            
                
    
    def probability_map(self):
        # Creates a probability map for the current game_table ( each square contains the number of ways it can harbor a battleship of each type )
        # Input: self - the current object
        # Output: an object of type coordinates, containing the coordinates of the highest probability square
        player_map = deepcopy(self.__computer_player.get_enemy_invisible_map)
        probabilities = [[0 for x in range(8)] for y in range(8)]
        highest = 0
        for row_index in range(len(player_map)):
            for column_index in range(len(player_map)):
                probability = 0
                if player_map[row_index][column_index] == "_":
                    # Destroyer
                    if game_development.coordinates_in_range(player_map, row_index-1, column_index) == True and player_map[row_index-1][column_index] != "*":
                        probability += 1
                    if game_development.coordinates_in_range(player_map, row_index+1, column_index) == True and player_map[row_index+1][column_index] != "*":
                        probability += 1
                    if game_development.coordinates_in_range(player_map, row_index, column_index-1) == True and player_map[row_index][column_index-1] != "*":
                        probability += 1
                    if game_development.coordinates_in_range(player_map, row_index, column_index+1) == True and player_map[row_index][column_index+1] != "*":
                        probability += 1
                    
                    # Cruiser
                    if game_development.coordinates_in_range(player_map, row_index-2, column_index) == True and player_map[row_index-1][column_index] != "*" and player_map[row_index-2][column_index] != "*":
                        probability += 1
                    if game_development.coordinates_in_range(player_map, row_index+2, column_index) == True and player_map[row_index+1][column_index] != "*" and player_map[row_index+2][column_index] != "*":
                        probability += 1
                    if game_development.coordinates_in_range(player_map, row_index, column_index-2) == True and player_map[row_index][column_index-1] != "*" and player_map[row_index][column_index-2] != "*":
                        probability += 1
                    if game_development.coordinates_in_range(player_map, row_index, column_index+2) == True and player_map[row_index][column_index+1] != "*" and player_map[row_index][column_index+2] != "*":
                        probability += 1
                        
                    # Destroyer
                    if game_development.coordinates_in_range(player_map, row_index-3, column_index) == True and player_map[row_index-1][column_index] != "*" and player_map[row_index-2][column_index] != "*" and player_map[row_index-3][column_index] != "*":
                        probability += 1
                    if game_development.coordinates_in_range(player_map, row_index+3, column_index) == True and player_map[row_index+1][column_index] != "*" and player_map[row_index+2][column_index] != "*" and player_map[row_index+3][column_index] != "*":
                        probability += 1
                    if game_development.coordinates_in_range(player_map, row_index, column_index-3) == True and player_map[row_index][column_index-1] != "*" and player_map[row_index][column_index-2] != "*" and player_map[row_index][column_index-3] != "*":
                        probability += 1
                    if game_development.coordinates_in_range(player_map, row_index, column_index+3) == True and player_map[row_index][column_index+1] != "*" and player_map[row_index][column_index+2] != "*" and player_map[row_index][column_index+3] != "*":
                        probability += 1
                        
                if probability >= highest:
                    # Get the highest probability square
                    highest = probability
                    maximum_row_index = row_index
                    maximum_column_index = column_index
                probabilities[row_index][column_index] = probability
        return coordinates(maximum_column_index+1, maximum_row_index+1)
    
    @staticmethod
    def coordinates_in_range(player_map, row_index, column_index):
        # Checks if the coordinates are in range ( 1 - 8 )
        # Input: player_map - an object of type game_table, the map of the human player
        #        row_index - the index of the row to be checked
        #        column_index - the index of the column to be checked
        # Output: True, if the coordinates are in range, False otherwise
        try:
            if row_index < 0 or column_index < 0:
                return False
            if player_map[row_index][column_index] != "0":
                return True
        except IndexError:
            return False
        