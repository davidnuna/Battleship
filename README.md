# Battleship AI

Battleship game vs an AI, made with python, using the tkinter framework for the GUI version. The AI uses a probability map ( checks the most likely spot after each move, based on the current table evolution ) for the hunting mode and a simple stack algorithm that utilizes a stack for the targeting mode. The computer player places his ships randomly each turn. 

A web version created with Flask is available here: https://github.com/neutralove/Flask-Battleship.

# Game Rules:

The game is played on a 8x8 grid, following the well-known paper game "battleship". The first grid is yours, whilst the second one is the enemy's! There are 2 phases covering the development of the game: The placing-phase and the attack-phase: 

## The Placing-Phase:

You must place exactly 3 unique battleships (horizontally or vertically): a Destroyer (2 squares), a Cruiser (3 squares) and a Battleship (4 squares).

In order to place any of these ships, simply click on your desired squares and after you are done press the "Place Battleship" button (you must place the battleships one by one, so you have to press the button after every ship placement).

After you're done placing all your ships, the attack phase begins.

## The Attack-Phase:

The goal is simple: destroy the enemy's fleet before he sinks yours. All you have to do is click the square on the enemy's grid where you reckon an enemy battleship might be located, whilst the enemy will do the same. If you manage to hit a battleship, the square will turn red, otherwise it will turn white.

If you manage to succeed, you can register your score (the number of times you attacked before you managed to sink the enemy fleet) by entering your name in the appearing area.

# Installation and usage

Clone the repository:
```
git clone https://github.com/neutralove/Battleship.git
```
There are 2 user interfaces available : a text-based one and a graphical one. The choice can be made in the settings.txt file.
After choosing the desired UI, simply start the application:
```
python main.py
```

