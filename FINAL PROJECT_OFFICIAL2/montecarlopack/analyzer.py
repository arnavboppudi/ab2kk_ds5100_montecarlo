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
print(analyzer.jackpot())
print(analyzer.face_counts_per_roll())
print(analyzer.combo_count())
print(analyzer.permutation_count())
