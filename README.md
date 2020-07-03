# GoZero-MCTS
My first endeavor at creating an RL bot based off of Monte Carlo Tree Search for the Go board game, from scratch. For reference on the variation of Go implemented, I use the [Chinese rules](https://www.cs.cmu.edu/~wjh/go/rules/Chinese.html).

## Usage
This program doesn't use any non-builtin python libraries with the exception of numpy. There is a graphical component which uses remi, but it's not required.

Therefore, you will only need at least:
* Python3
* Numpy 1.11 or (preferably) greater

The recommended way to use this is to run the `parse_sgf.py` with a .sgf file as input. If you don't know, SGF stands for [Smart Game Format](https://en.wikipedia.org/wiki/Smart_Game_Format) and is the way Go stores records of games. The program will then return the notation for the next move in the position.

For example: `python3 ./parse_sgf sample_file.sgf`

The most optimal way to use `parse_sgf.py` is to have another program constantly running on a server that calls this when pinged. That way performance isn't limited by personal hardware.

Another option is to use the graphical display in `display.py`. This brings up a Go board and allows you to directly play against the AI. However, this will be **very slow** as you'll be running it on local hardware. If you want to test this out, you will also need to install the latest version of remi through pip.

## Configuration
If you want to configure the performance of the AI or it's speed, there are a couple of things you can change to do so. If you are using the graphical display, you will most likely want to decrease the amount of calculation.

### Performance Boosts
* During simulation phase of the MCTS cycle, the program will, at any point in the game, select a random move to play. Speed can be optimized here by setting a probability for adding a move to be selected randomly. Line 88 of `MCTS.py` achieves this, and if you don't need this, you can comment it out.
* The bot is also mean to simulate until there is no more neutral territory, however, this takes a long time and so we'll only simulate the next 100 moves and select the side who's ahead. The count variable on line 70 of `MCTS.py` achieves this, and if you don't need this, remove all occurrences of count as well as anything nested.
* Also, by default the AI is given 20 seconds per move, and if you want it to perform better without requiring more CPU, you can increase it on line 16 of `MCTS.py`