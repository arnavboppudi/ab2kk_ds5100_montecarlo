# Die Game Analyzer

#### This project provides classes to create, simulate, and analyze die-based games. It consists of three primary classes: Die, Game, and Analyzer.

## Metadata

Language: Python
Libraries used: numpy, pandas

## Synopsis

### DIE CLASS


```python
die = Die(np.array([]))
print(die.show_state())

die.change_weight()
print(die.show_state())

print(die.roll()) 
```

### GAME CLASS


```python
die1 = Die(np.array([]))
die2 = Die(np.array([]))

game = Game([die1, die2])
game.play(n)

print(game.show_results())
print(game.show_results(format="narrow"))

```

### ANALYZER CLASS


```python
die1 = Die(np.array([]))
die2 = Die(np.array([]))

game = Game([die1, die2])
game.play(n)

analyzer = Analyzer(game)
print("The number of Jackpots:", analyzer.jackpot())
print(analyzer.face_counts_per_roll())
print(analyzer.combo_count())
print(analyzer.permutation_count())

```

## API

### DIE CLASS

**__init__**(faces): Sets up the die with faces.

**change_weight**(face, new_weight): Adjusts weight of a face.

**roll(times=1)**: Rolls the die.

**show_state()**: Displays die's current state.

### GAME CLASS

__init__(dice_list): Starts a game with dice list.

**play(num_rolls)**: Rolls dice multiple times.

**show_results(format="wide")**: Shows roll results in "wide" or "narrow" format.

### ANALYZER CLASS

**__init__(game)**: Begins analysis with a game.

**jackpot()**: Gives jackpot counts (all dice with same face).

**face_counts_per_roll()**: Shows face counts for rolls.

**combo_count()**: Lists combination frequencies.

**permutation_count()**: Lists permutation frequencies.


```python

```
