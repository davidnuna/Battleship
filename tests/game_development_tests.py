# The module that contains the tests for the whole project

import unittest
from player import player
from game_development import game_development
from game_table import game_table
from validations import validation
from exceptions.exceptions import InvalidCoordinates, AreaTaken

class game_testing(unittest.TestCase):
    def setUp(self):
        self.__game_controller = game_development(validation(), player(game_table(), game_table(), game_table()), player(game_table(), game_table(), game_table()))
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_add_battleship__valid_input_updated_game_table(self):
        self.__game_controller.place_battleship(1, 1, 1, 3)
        self.assertEqual(self.__game_controller.get_human_visible_map[1][0], "C")  
    
    def test_add_battleship__invalid_coordinates_throw_exception(self):
        self.assertRaises(InvalidCoordinates, lambda: self.__game_controller.place_battleship(1, 1, -1, 3))
    
    def test_add_battleship__area_taken_throw_exception(self):
        self.__game_controller.place_battleship(5, 5, 5, 8)
        self.assertRaises(AreaTaken, lambda: self.__game_controller.place_battleship(5, 7, 5, 8))

    def test_human_shoot_square__valid_input_updated_game_table(self):
        self.__game_controller.human_shoot_square(5,5)
        self.assertEqual(self.__game_controller.get_computer_invisible_map[4][4], "*")  
    
    def test_human_shoot_square__invalid_coordinates_throw_exception(self):
        self.assertRaises(InvalidCoordinates, lambda: self.__game_controller.human_shoot_square(1, 9))
        
    def test_computer_shoot_square__updated_game_table(self):
        self.__game_controller.computer_shoot_square()
        self.assertEqual(True, "*" in self.__game_controller.get_human_invisible_map[4])
    
    def test_check_if_game_ended__game_not_finished_return_False(self):
        self.assertEqual(self.__game_controller.check_if_game_ended(), False)
        
    def test_place_random_battleships__updated_game_table(self):
        self.__game_controller.place_random_battleships()
        squares_with_battleships = 0
        for row_index in range(8):
            for column_index in range(8):
                if self.__game_controller.get_computer_visible_map[row_index][column_index] != "_":
                    squares_with_battleships += 1
        self.assertEqual(squares_with_battleships, 9)