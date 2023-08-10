import numpy as np
import pandas as pd

class Die:
    def __init__(self, faces):
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

    def change_weight(self, face, new_weight):
        # Check if face exists in die
        if face not in self._data.index:
            raise IndexError("Face not found in die")

        # Check if weight is numeric and non-negative
        if not isinstance(new_weight, (int, float)):
            raise TypeError("Weight should be numeric (int or float)")

        if new_weight < 0:
            raise ValueError("Weight should be non-negative")

        # Set new weight
        self._data.at[face, 'weights'] = new_weight

    def roll(self, times=1):
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
