import numpy as np
import pandas as pd

class Die:
    def __init__(self, faces): #sets up initial state for a new object of the Die class
        # Check if faces is a numpy array
        if not isinstance(faces, np.ndarray):
            raise TypeError("Input faces should be a numpy array")

        # Check if faces' dtype is either string or number
        if faces.dtype.kind not in ['i', 'u', 'f', 'U', 'S']:
            raise TypeError("Faces should contain either strings or numbers")

        # Check if all faces are distinct
        if len(faces) != len(np.unique(faces)):
            raise ValueError("All faces should be distinct")

        # Initialize weights to 1.0 for each face
        weights = np.ones_like(faces, dtype=float)

        # Save faces and weights in a private dataframe
        self._data = pd.DataFrame({'weights': weights}, index=faces)

    def change_weight(self, face, new_weight): #allows user to change the weight of given face of die
        # Check if face exists in die
        if face not in self._data.index:
            raise IndexError("Face not found on die")

        # Check if weight is numeric and non-negative
        if not isinstance(new_weight, (int, float)):
            raise TypeError("Weight should be numeric (int or float)")

        if new_weight < 0:
            raise ValueError("Weight should be non-negative")

        # Set new weight for face in _data dataframe
        self._data.at[face, 'weights'] = new_weight

    def roll(self, times=1): #simulates rolling the die
        # Check if 'times' is positive and an integer
        if not isinstance(times, int) or times <= 0:
            raise ValueError("'times' should be a positive integer")

        # Sample with replacement using weights
        results = self._data.sample(n=times, weights='weights', replace=True).index.tolist()
        return results

    def show_state(self):
        # Return a copy of the private dataframe
        return self._data.copy()

# Example Usage
die = Die(np.array([1, 2, 3, 4, 5, 6]))
print(die.show_state())

die.change_weight(3, 2.0)  # Make the side with value 3 more likely to appear
print(die.show_state())

print(die.roll(10))  # Roll the die 10 times



###############################################################################

import numpy as np
#import pandas as pd
from die import Die

# Assuming Die class has been previously defined...

class Game:
    def __init__(self, dice_list): #initializes an instance of the Game class
        # Ideally, one would check if each element in dice_list is an instance of Die and if they all have the same faces.
        self.dice = dice_list
        self._results = None  # This will hold the results DataFrame when dice are rolled

    def play(self, num_rolls):
        # Create a placeholder dataframe to store results of rolls
        results = []

        # Roll each die the specified number of times and save the results
        for roll_num in range(num_rolls):
            roll_results = []
            for die in self.dice:
                roll_results.append(die.roll()[0])  # Since roll returns a list, take the first (and only) element
            results.append(roll_results)
        
        self._results = pd.DataFrame(results, columns=[f"Die_{i+1}" for i in range(len(self.dice))])

    def show_results(self, format="wide"):
        if self._results is None:
            raise ValueError("No game has been played yet!")

        if format == "wide":
            return self._results.copy()
        elif format == "narrow":
            narrow_df = self._results.stack().reset_index()
            narrow_df.columns = ['Roll_Num', 'Die_Num', 'Outcome']
            narrow_df.set_index(['Roll_Num', 'Die_Num'], inplace=True)
            return narrow_df
        else:
            raise ValueError("Invalid option. Choose 'wide' or 'narrow'.")

# Example usage:
die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
die2 = Die(np.array([1, 2, 3, 4, 5, 6]))

game = Game([die1, die2])
game.play(5)

print(game.show_results())
print(game.show_results(format="narrow"))

###############################################################################

import numpy as np
from die import Die
from game import Game

class Analyzer:
    def __init__(self, game):
        if not isinstance(game, Game):
            raise ValueError("Expected a Game object")
        self.game = game

    def jackpot(self):
        if self.game._results is None:
            raise ValueError("No game has been played yet!")

        return (self.game._results.nunique(axis=1) == 1).sum()

    def face_counts_per_roll(self):
        if self.game._results is None:
            raise ValueError("No game has been played yet!")

        all_faces = np.concatenate([die.show_state().index.to_numpy() for die in self.game.dice])
        all_faces = np.unique(all_faces)

        count_df = self.game._results.apply(lambda row: [row.tolist().count(face) for face in all_faces], axis=1, result_type="expand")
        count_df.columns = all_faces
        return count_df

    def combo_count(self):
        if self.game._results is None:
            raise ValueError("No game has been played yet!")

        combos = self.game._results.apply(lambda x: tuple(sorted(x.tolist())), axis=1)
        counts = combos.value_counts()
        df = counts.reset_index()
        df.columns = ['Combo', 'Count']
        return df.set_index('Combo')

    def permutation_count(self):
        if self.game._results is None:
            raise ValueError("No game has been played yet!")

        permutations = self.game._results.apply(tuple, axis=1)
        counts = permutations.value_counts()
        df = counts.reset_index()
        df.columns = ['Permutation', 'Count']
        return df.set_index('Permutation')

# Example usage:
die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
die2 = Die(np.array([1, 2, 3, 4, 5, 6]))

game = Game([die1, die2])
game.play(5)

analyzer = Analyzer(game)
print("The numeber of Jackpots:", analyzer.jackpot())
print(analyzer.face_counts_per_roll())
print(analyzer.combo_count())
print(analyzer.permutation_count())