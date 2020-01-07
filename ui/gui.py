# The graphical user interface

from tkinter import *
import tkinter.messagebox
from copy import deepcopy
from exceptions.exceptions import InvalidCoordinates, InvalidBattleship, AreaTaken, SquareAlreadyHit


class gui:
    def __init__(self, game_controller):
        self.__game_controller = game_controller
        self.__root_window = Tk()
        self.__left_frame = Frame(self.__root_window, width = 550, height = 550, bg = "#3CB371",  highlightthickness = 5, highlightbackground = "#2E4053")
        self.__right_frame = Frame(self.__root_window, width = 550, height = 550, bg=  "#FF6347", highlightthickness = 5, highlightbackground = "#2E4053")
        self.__right_frame.pack_propagate(0)
        self.__right_frame.grid_propagate(0)
        self.__left_frame.pack_propagate(0)
        self.__left_frame.grid_propagate(0)
        self.__left_canvas = Canvas(self.__left_frame, width = 397, height = 397, background = "#3CB371")
        self.__right_canvas = Canvas(self.__right_frame, width = 397, height = 397, background = "#FF6347")
        self.__status_bar_left = Label(self.__left_frame, font = ("Helvetica", 12), text = "Placing the battleships...", bg = "#3CB371", bd = 1, relief = RIDGE, anchor = CENTER, fg = "white", borderwidth=2)
        self.__status_bar_right = Label(self.__right_frame, font = ("Helvetica", 12), text = "Waiting for the battleships to be placed... ", bg = "#FF6347", bd = 1, relief = RIDGE, anchor = CENTER, fg = "white", borderwidth=2)
        self.__status_bar_left.pack(side=BOTTOM, fill=X)
        self.__status_bar_right.pack(side=BOTTOM, fill=X)
        self.__left_frame.pack(side = LEFT, fill = BOTH, expand = True)
        self.__right_frame.pack(side = RIGHT, fill = BOTH, expand = True)
        self.__left_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.__right_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.create_table(self.__left_canvas, self.__left_frame, "#3CB371")
        self.create_table(self.__right_canvas, self.__right_frame, "#FF6347" )

    def create_table(self, canvas, frame, color):
        for line in range(0, 8):
            canvas.create_line(line * 50, 0, line * 50, 400, width=2, fill = "white")
        for line in range(0, 8):
            canvas.create_line(0, line * 50, 400, line * 50, width=2, fill = "white")
        horizontal_label = Label(frame, text= "A", bg = color, font = ("Helvetica", 16), fg = "white")
        x_coordinate = 85
        square_number = 0
        while square_number < 8:
            square_number += 1
            label_copy = Label(frame, text = chr(ord(horizontal_label["text"]) + square_number-1), bg = color, font = ("Helvetica", 16), fg = "white")
            label_copy.place(y = 38, x = x_coordinate)
            x_coordinate += 50
        
        vertical_label = Label(frame, text= "1", bg = color, font = ("Helvetica", 16), fg = "white")
        y_coordinate = 80
        square_number = 0
        while square_number < 8:
            square_number += 1
            label_copy = Label(frame, text = chr(ord(vertical_label["text"]) + square_number-1), bg = color, font = ("Helvetica", 16), fg = "white")
            label_copy.place(y = y_coordinate, x = 40)
            y_coordinate += 50
    
    def fill_cell(self, event, color, current_battleship, list_of_battleships):
        for battleship in list_of_battleships:
            if [event.y // 50 + 1, event.x // 50 + 1] in battleship:
                return
        if [event.y // 50 + 1, event.x // 50 + 1] in current_battleship:
            current_battleship.remove([event.y // 50 + 1, event.x // 50 + 1])
            self.__left_canvas.create_rectangle((event.x//50)*50+1, (event.y//50)*50+1, (event.x//50)*50 + 48, (event.y//50)*50 + 48, fill = self.__left_canvas["background"], outline = self.__left_canvas["background"])
        else:
            current_battleship.append([event.y // 50 + 1, event.x // 50 + 1])
            self.__left_canvas.create_rectangle((event.x//50)*50+1, (event.y//50)*50+1, (event.x//50)*50 + 48, (event.y//50)*50 + 48, fill = color)
            
    def fill_battleship(self, color, battleship):
        for square in battleship:
            self.__left_canvas.create_rectangle((((square[1]-1)*50)//50)*50+1, (((square[0]-1)*50)//50)*50+1, (((square[1]-1)*50)//50)*50 + 48, (((square[0]-1)*50)//50)*50 + 48, fill = color, outline = self.__left_canvas["background"])
            if color != "#006400": 
                continue
            if len(battleship) == 2:
                self.__left_canvas.create_text((((square[1]-1)*50)//50)*50+25, (((square[0]-1)*50)//50)*50+25, text = "D", font = ("Helvetica", 15), fill = "white")
            elif len(battleship) == 3:
                self.__left_canvas.create_text((((square[1]-1)*50)//50)*50+25, (((square[0]-1)*50)//50)*50+25, text = "C", font = ("Helvetica", 15), fill = "white")            
            else:
                self.__left_canvas.create_text((((square[1]-1)*50)//50)*50+25, (((square[0]-1)*50)//50)*50+25, text = "B", font = ("Helvetica", 15), fill = "white")
          
    def check_square_coverage(self, battleship):
        battleship_length = 0
        if battleship[0][0] == battleship[-1][0]:
            battleship_length = battleship[-1][1] - battleship[0][1] + 1
        elif battleship[0][1] == battleship[-1][1]:
            battleship_length = battleship[-1][0] - battleship[0][0] + 1
        else:
            return True
        if battleship_length == len(battleship):
            return True
        else:
            return False

    def ui_place_battleships(self):
        def place_battleship(self, number_of_battleships_placed, current_battleship, list_of_battleships):
            try:
                current_battleship.sort()
                if self.check_square_coverage(current_battleship) == False:
                    raise InvalidBattleship("Invalid coordinates! You can only place battleship on 2, 3 or 4 squares!\n")
                self.__game_controller.place_battleship(current_battleship[0][1], current_battleship[0][0], current_battleship[-1][1], current_battleship[-1][0])
                self.__status_bar_left["text"] = "Battleship successfully placed!"
                list_of_battleships.append(deepcopy(current_battleship))
                number_of_battleships_placed.append("X")
                self.fill_battleship("#006400", deepcopy(current_battleship))
            except IndexError:
                self.__status_bar_left["text"] = "Invalid coordinates! You can only place battleship on 2, 3 or 4 squares!"
            except (InvalidCoordinates, InvalidBattleship, AreaTaken) as exception_message:
                self.__status_bar_left["text"] = str(exception_message).strip("\n")
                self.fill_battleship("#3CB371", deepcopy(current_battleship))
            if len(number_of_battleships_placed) == 3:
                confirm_button.pack_forget()
                self.__status_bar_left["text"] = "All battleships have been placed! Let's switch to the attack phase!"
                self.__status_bar_right["text"] = "Waiting for a target..."
                self.__left_canvas.unbind("<Button-1>")
                self.__right_canvas.bind("<Button-1>", (lambda event: self.ui_advance_the_game(event)))    
                return
            current_battleship.clear()

        list_of_battleships = []
        current_battleship = []
        number_of_battleships_placed = []
        self.__left_canvas.bind("<Button-1>", (lambda event: self.fill_cell(event, "white", current_battleship, list_of_battleships)))
        confirm_button = Button(self.__left_frame, fg = "white", bg = "#3CB371", font = ("Helvetica", 12), text="Place Battleship", activeforeground = "black", activebackground = "#3CB371", cursor = "hand2", command = lambda: place_battleship(self, number_of_battleships_placed, current_battleship, list_of_battleships))
        confirm_button.pack(side = BOTTOM, pady = 5)
        
    def update_cell_human(self, event, color):
        self.__right_canvas.create_rectangle((event.x//50)*50+1, (event.y//50)*50+1, (event.x//50)*50 + 48, (event.y//50)*50 + 48, fill = color, outline = self.__right_canvas["background"])
        
    def update_cell_computer(self, coordinates, color):
        self.__left_canvas.create_rectangle((coordinates.get_coordinate_x-1)*50+1, (coordinates.get_coordinate_y-1)*50+1, (coordinates.get_coordinate_x-1)*50 + 48, (coordinates.get_coordinate_y-1)*50 + 48, fill = color, outline = self.__left_canvas["background"])
        
    def ui_advance_the_game(self, event):
        try:
            square_hit = False
            square_hit = self.__game_controller.human_shoot_square((event.x//50+1), (event.y//50)+1)
            if square_hit == True:
                self.update_cell_human(event, "#3CB371")
                self.__status_bar_right["text"] = str("Nice shot! It was a clear hit!")
            else:
                self.update_cell_human(event, "white")
                self.__status_bar_right["text"] = str("The shot missed! Try again!")
            if self.__game_controller.check_if_game_ended() != False:
                if self.__game_controller.check_if_game_ended() == "Human":
                    tkinter.messagebox.showinfo("Game Over!", "You won! You defeated the entire enemy fleet!")
                else:
                    tkinter.messagebox.showinfo("Game Over!", "You lost! Your fleet has been completely annihilated!")
                self.__right_canvas.unbind("<Button-1>")
                user_answer = tkinter.messagebox.askquestion("New Game", "Press Yes to play again or No to exit the application")
                if user_answer == "no":
                    self.__root_window.destroy()
                else:
                    self.__game_controller.reset_game()
                    self.__right_canvas.delete(ALL)
                    self.__left_canvas.delete(ALL)
                    self.create_table(self.__left_canvas, self.__left_frame, "#3CB371")
                    self.create_table(self.__right_canvas, self.__right_frame, "#FF6347")
                    self.__status_bar_left["text"] =  str("Placing the battleships...")
                    self.__status_bar_right["text"] = str("Waiting for the battleships to be placed... ")
                    self.start_game()
            square_hit = False
            square_hit_and_coordinates = self.__game_controller.computer_shoot_square()
            square_hit = square_hit_and_coordinates[0]
            coordinates = square_hit_and_coordinates[1]
            if square_hit == True:
                self.update_cell_computer(coordinates, "#FF6347")
                self.__status_bar_left["text"] = str("The computer hit a part of your fleet! Destroy his before he destroys yours !")
            else:
                self.update_cell_computer(coordinates, "white")
                self.__status_bar_left["text"] = str("The computer missed! Nice positioning!")
            if self.__game_controller.check_if_game_ended() != False:
                if self.__game_controller.check_if_game_ended() == "Human":
                    tkinter.messagebox.showinfo("Game Over!", "You won! You defeated the entire enemy fleet!")
                else:
                    tkinter.messagebox.showinfo("Game Over!", "You lost! Your fleet has been completely annihilated!")
                self.__right_canvas.unbind("<Button-1>")
                user_answer = tkinter.messagebox.askquestion("New Game", "Press Yes to play again or No to exit the application")
                if user_answer == "no":
                    self.__root_window.destroy()
                else:
                    self.__game_controller.reset_game()
                    self.__right_canvas.delete(ALL)
                    self.__left_canvas.delete(ALL)
                    self.create_table(self.__left_canvas, self.__left_frame, "#3CB371")
                    self.create_table(self.__right_canvas, self.__right_frame, "#FF6347")
                    self.__status_bar_left["text"] =  str("Placing the battleships...")
                    self.__status_bar_right["text"] = str("Waiting for the battleships to be placed... ")
                    self.start_game()
        except (InvalidCoordinates, SquareAlreadyHit) as exception_message:
            self.__status_bar_right["text"] = str(exception_message).strip("\n")  
         
    def start_game(self):
        self.__game_controller.place_random_battleships()
        self.ui_place_battleships()
        
    def run(self):
        self.__root_window.title("Battleship game")
        self.start_game()
        self.__root_window.mainloop()
        