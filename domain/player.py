# The module that contains the player class


class player:
    def __init__(self, ally_visible_map, enemy_invisible_map, enemy_visible_map):
        # Every player will have access to 3 maps: his own, the enemy's current map ( which is empty at first ) and the enemy's map
        # Input: self - the current object
        #        ally_visible_map - an object of type 'game_table', the map of the current player
        #        enemy_invisible_map - an object of type 'game_table', the current map of the opposing player
        #        enemy_visible_map - an object of type 'game_table', the map of the opposing player
        self.__ally_visible_map = ally_visible_map 
        self.__enemy_invisible_map = enemy_invisible_map
        self.__enemy_visible_map = enemy_visible_map
    
    def reset_table(self):
        # Functions that clears every game table of the current player
        # Input: self - the current object
        # Output: nothing
        self.__ally_visible_map.create_new_table()
        self.__enemy_invisible_map.create_new_table()
        self.__enemy_visible_map.create_new_table()
        
    @property
    def get_ally_visible_map(self):
        # Getter for the 'ally_visible_map' instance
        # Input: self - the current object
        # Output: the table of the current player
        return self.__ally_visible_map.get_table

    @property
    def get_enemy_invisible_map(self):
        # Getter for the 'enemy_invisible_map' instance
        # Input: self - the current object
        # Output: the current table of the opposing player
        return self.__enemy_invisible_map.get_table
    
    @property
    def get_enemy_visible_map(self):
        # Getter for the 'enemy_visible_map' instance
        # Input: self - the current object
        # Output: the table of the opposing player
        return self.__enemy_visible_map.get_table
    
    def add_new_battleship(self, ship_start_coordinates, ship_end_coordinates, battleship_type):
        # Calls the function that adds a new battleship at the position given by 'ship_start_coordinates' and 'ship_end_coordinates'
        # Input: self - the current object
        #        ship_start_coordinates - an object of type coordinates, the starting coordinates (x,y) of the new battleship
        #        ship_end_coordinates - an object of type coordinates, the ending coordinates (x,y) of the new battleship
        #        battleship_type - a string, the type of the battleship that will be placed ( destroyer - 2 squares, cruiser - 3 squares, battleship - 4 squares )
        # Output: nothing
        self.__ally_visible_map.add_battleship(ship_start_coordinates, ship_end_coordinates, battleship_type)
    
    def launch_attack(self, coordinates):
        # Checks the square at the given coordinates and updates the two maps ( the one for the player and for the enemy ) accordingly
        # Input: self - the current object
        #        coordinates - an object of type coordinates, the coordinates of the squares to be checked
        # Output: battleship_hit - a boolean type ( True or False ), True if there was a battleship at the given squares, False otherwise
        battleship_hit = self.__enemy_visible_map.update_visible_map(coordinates)
        self.__enemy_invisible_map.update_invisible_map(coordinates, battleship_hit)
        return battleship_hit