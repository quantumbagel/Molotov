# Molotov

_Molotov is a bot for the insanely addictive game Bomb Party (jklm.fun)_

_Programmed on Python 3.10_

# What is Bomb Party?

Bomb Party is a simple game where you try to create words that contain a certain subset. For example, an answer to the subset 'AC' might be 'catarACt' or 'sACk'.

Given that I am kind of bad at this game, I made a bot for it!


# Setup

One command (linux):
`git clone https://github.com/quantumbagel/Molotov.git && cd Molotov && pip3 install -r requirements.txt && python3 molotov.py`

You will need git and python3 to run Molotov.

You will need a Bomb Party game open to complete setup, just follow the instructions from `molotov.py`!



# Running

Just run `python3 molotov.py` to activate. If you move or resize your jklm.fun window, run `python3 molotov.py --reconfigure` and follow the setup again!



# When things go wrong...

Just post the full output of the program under Issues and I will try to fix it as best I can!



# Explaining config.yml

- join-game: this is the x/y coordinates of the Join Game button
- join-game-color: the RGB of the Join Game button
- letter: the x/y of the subset
- current-turn: the RGB of the text box
- record: the record of the bot
- delay: the delay for typing (to impersonate >:)
