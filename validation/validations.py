# The module that contains the validation class

from exceptions.exceptions import InvalidCoordinates, InvalidBattleship


class validation:
    def validate_double_coordinates(self, ship_start_coordinates, ship_end_coordinates, placed_ships):
        # Checks if the two given coordinates are valid
        # Input: self - the current object -
        #        ship_start_coordinates - an object of type coordinates, the starting coordinates (x,y) to be validated
        #        ship_end_coordinates - an object of type coordinates, the ending coordinates (x,y) to be validated
        #        placed_ships - a list, containing ( as strings ) the battleship types that have already been placed ( destroyer, cruiser, battleship )
        # Output: nothing
        # Raises: InvalidCoordinates, if the coordinates are not between 1 and 8 or if they don't represent a rectangle ( horizontally or vertically ) of length 2,3 or 4 
        #         InvalidBattleship, if the wanted battleship has already been placed        
        if ship_start_coordinates.get_coordinate_x < 1 or ship_start_coordinates.get_coordinate_x > 8 or ship_start_coordinates.get_coordinate_y < 1 or ship_start_coordinates.get_coordinate_y > 8:
            raise InvalidCoordinates("Invalid coordinates! The x coordinate must be between 'A' and 'H', whilst the y coordinate must be between '1' and '8'!\n") 
        
        if ship_end_coordinates.get_coordinate_x < 1 or ship_end_coordinates.get_coordinate_x > 8 or ship_end_coordinates.get_coordinate_y < 1 or ship_end_coordinates.get_coordinate_y > 8:
            raise InvalidCoordinates("Invalid coordinates! The x coordinate must be between 'A' and 'H', whilst the y coordinate must be between '1' and '8'!\n") 
        
        if ship_start_coordinates.get_coordinate_x != ship_end_coordinates.get_coordinate_x and ship_start_coordinates.get_coordinate_y != ship_end_coordinates.get_coordinate_y:
            raise InvalidCoordinates("Invalid coordinates! The battleships can only be placed in a straight line (horizontally or vertically) !\n")
        
        if ship_start_coordinates.get_coordinate_x == ship_end_coordinates.get_coordinate_x:
            if abs(ship_start_coordinates.get_coordinate_y - ship_end_coordinates.get_coordinate_y)+1 < 2 or abs(ship_start_coordinates.get_coordinate_y - ship_end_coordinates.get_coordinate_y)+1 > 4:
                raise InvalidCoordinates("Invalid coordinates! You can only place battleship on 2, 3 or 4 squares!\n")
            battleship_length = abs(ship_start_coordinates.get_coordinate_y - ship_end_coordinates.get_coordinate_y)+1
            if battleship_length == 2:
                battleship_type = "Destroyer"
            elif battleship_length == 3:
                battleship_type = "Cruiser"
            elif battleship_length == 4:
                battleship_type = "Battleship"
            if battleship_type in placed_ships:
                raise InvalidBattleship("Invalid battleship type! The wanted battleship has already been placed!\n")
            placed_ships.append(battleship_type)

        elif ship_start_coordinates.get_coordinate_y == ship_end_coordinates.get_coordinate_y:
            if abs(ship_start_coordinates.get_coordinate_x - ship_end_coordinates.get_coordinate_x)+1 < 2 or abs(ship_start_coordinates.get_coordinate_x - ship_end_coordinates.get_coordinate_x)+1 > 4:
                raise InvalidCoordinates("Invalid coordinates! You can only place battleship on 2, 3 or 4 squares!\n")
            battleship_length = abs(ship_start_coordinates.get_coordinate_x - ship_end_coordinates.get_coordinate_x)+1
            if battleship_length == 2:
                battleship_type = "Destroyer"
            elif battleship_length == 3:
                battleship_type = "Cruiser"
            elif battleship_length == 4:
                battleship_type = "Battleship"
            if battleship_type in placed_ships:
                raise InvalidBattleship("Invalid battleship type! The wanted battleship has already been placed!\n")
            placed_ships.append(battleship_type)

    def validate_single_coordinates(self, coordinates):
        # Checks if the coordinates are valid
        # Input: self - the current object -
        #        coordinates - an object of type coordinates, the coordinates to be validated
        # Output: nothing
        # Raises: InvalidCoordinates, if the coordinates are not between 1 and 8   
        if coordinates.get_coordinate_x < 1 or coordinates.get_coordinate_x > 8 or coordinates.get_coordinate_y < 1 or coordinates.get_coordinate_y > 8:
            raise InvalidCoordinates("Invalid coordinates! The x coordinate must be between 'A' and 'H', whilst the y coordinate must be between '1' and '8'!\n") 