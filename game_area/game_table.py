# The module that contains the game_table class

from exceptions.exceptions import AreaTaken, SquareAlreadyHit

class game_table(object):
    def __init__(self):
        # Calls the function 'create_new_table'
        # Input: self - the current object
        self.create_new_table()
        
    def create_new_table(self):
        # Creates a new 8x8 matrix that will represent the game table
        # Input: self - the current object
        # Output: nothing
        self.__game_table = [["_" for x in range(8)] for y in range(8)]
    
    @property
    def get_table(self):
        # Getter for the 'game_table' instance
        # Input: self - the current object
        # Output: the game_table of the current object
        return self.__game_table
    
    def add_battleship(self, ship_start_coordinates, ship_end_coordinates, battleship_type):
        # Adds a new battleship if the new battleship does not overlap a previous one
        # Input: self - the current object -
        #        ship_start_coordinates - an object of type coordinates, the starting coordinates (x,y) of the new battleship
        #        ship_end_coordinates - an object of type coordinates, the ending coordinates (x,y) of the new battleship
        #        battleship_type - a string, the type of the battleship that will be placed ( destroyer - 2 squares, cruiser - 3 squares, battleship - 4 squares )
        # Output: nothing, if no exception is raised
        # Raises: AreaTaken, if the new battleship overlaps with a previous one
        fill_coordinates = []
        if ship_start_coordinates.get_coordinate_x == ship_end_coordinates.get_coordinate_x:
            coordinate_counter = min(ship_start_coordinates.get_coordinate_y, ship_end_coordinates.get_coordinate_y)
            while coordinate_counter <= max(ship_start_coordinates.get_coordinate_y, ship_end_coordinates.get_coordinate_y):
                fill_coordinates.append(coordinate_counter)
                coordinate_counter += 1
            for coordinate in fill_coordinates:
                if self.__game_table[coordinate-1][ship_start_coordinates.get_coordinate_x-1] != "_":
                    raise AreaTaken("Invalid battleship placing! The battleships cannot overlap!\n")
            for coordinate in fill_coordinates:
                self.__game_table[coordinate-1][ship_start_coordinates.get_coordinate_x-1] = str(battleship_type[0])
        elif ship_start_coordinates.get_coordinate_y == ship_end_coordinates.get_coordinate_y:
            coordinate_counter = min(ship_start_coordinates.get_coordinate_x, ship_end_coordinates.get_coordinate_x)
            while coordinate_counter <= max(ship_start_coordinates.get_coordinate_x, ship_end_coordinates.get_coordinate_x):
                fill_coordinates.append(coordinate_counter)
                coordinate_counter += 1
            for coordinate in fill_coordinates:
                if self.__game_table[ship_start_coordinates.get_coordinate_y-1][coordinate-1] != "_":
                    raise AreaTaken("Invalid battleship placing! The battleships cannot overlap!\n")
            for coordinate in fill_coordinates:
                self.__game_table[ship_start_coordinates.get_coordinate_y-1][coordinate-1] = str(battleship_type[0])

    def update_visible_map(self, coordinates):
        # Updates the visible map accordingly : if the square at the given coordinates contains a battleship, it is updated to 'X'. Otherwise, it is updated to '*'
        # Input: self - the current object
        #        coordinates - an object of type coordinates, the coordinates of the square to be updated
        # Output: True, if the value before the update
        # Raises: SquareAlreadyHit, if the square has already been hit
        if self.__game_table[coordinates.get_coordinate_y-1][coordinates.get_coordinate_x-1] == 'X' or self.__game_table[coordinates.get_coordinate_y-1][coordinates.get_coordinate_x-1] == '*':
            raise SquareAlreadyHit("Area already hit! There's nothing left to destroy, choose another square!\n")
        if self.__game_table[coordinates.get_coordinate_y-1][coordinates.get_coordinate_x-1] != '_':
            self.__game_table[coordinates.get_coordinate_y-1][coordinates.get_coordinate_x-1] = 'X' 
            return True
        self.__game_table[coordinates.get_coordinate_y-1][coordinates.get_coordinate_x-1] = '*' 
        return False
    
    def update_invisible_map(self, coordinates, battleship_hit):
        # Updates the invisible map accordingly : if the square at the given coordinates contained a battleship, it is updated to 'X'. Otherwise, it is updated to '*'
        # Input: self - the current object
        #        coordinates - an object of type coordinates, the coordinates of the square to be updated
        #        battleship_hit - a boolean type, True if the ship has been hit, False otherwise
        # Output: nothing
        if battleship_hit == True:
            self.__game_table[coordinates.get_coordinate_y-1][coordinates.get_coordinate_x-1] = 'X' 
        else:
            self.__game_table[coordinates.get_coordinate_y-1][coordinates.get_coordinate_x-1] = '*'
             
    def __str__(self):
        return str(self.__game_table)
