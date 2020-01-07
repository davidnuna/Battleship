# The main module, where the application starts

from console_ui import console_ui
from gui import gui
from player import player
from game_development import game_development
from game_table import game_table
from exceptions.exceptions import InvalidUI
from validations import validation

def run():  
    validator = validation()
    human_visible_map = game_table()            
    computer_invisible_map = game_table()        
    computer_visible_map = game_table()
    human_invisible_map = game_table()
    
    human_player = player(human_visible_map, computer_invisible_map, computer_visible_map)
    computer_player = player(computer_visible_map, human_invisible_map, human_visible_map)
    game_controller = game_development(validator, human_player, computer_player)
    try:
        with open("settings.properties", "r") as settings_file:
            chosen_ui = settings_file.readlines()[2].split()[2]
            if chosen_ui == "ConsoleUI":
                chosen_ui = console_ui(game_controller)
                chosen_ui.run() 
            elif chosen_ui == "GUI":
                chosen_ui = gui(game_controller)
                chosen_ui.run() 
            else:
                raise InvalidUI("Invalid UI! Please check the 'settings.properties' file!")
    except InvalidUI as exception_message:
        print(exception_message)
    
if __name__=='__main__':
    run()
    