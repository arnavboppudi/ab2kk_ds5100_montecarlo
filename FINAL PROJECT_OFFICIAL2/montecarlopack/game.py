import numpy as np
import pandas as pd
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
