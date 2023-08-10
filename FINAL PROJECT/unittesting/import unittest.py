import unittest
import numpy as np
from montecarlo import Die, Game, Analyzer

class TestDie(unittest.TestCase):
    def test_init(self):
        # Test valid init
        die = Die(np.array([1, 2, 3, 4, 5, 6]))
        self.assertIsInstance(die, Die)
        
        # Test invalid dtype
        with self.assertRaises(TypeError):
            die = Die(np.array([1, 2, "a", 4, 5, 6]))

        # Test repeated face values
        with self.assertRaises(ValueError):
            die = Die(np.array([1, 2, 3, 3, 5, 6]))

    def test_show_state(self):
        die = Die(np.array([1, 2, 3, 4, 5, 6]))
        self.assertIsInstance(die.show_state(), pd.DataFrame)
        
    def test_change_weight(self):
        die = Die(np.array([1, 2, 3, 4, 5, 6]))
        die.change_weight(3, 2.0)
        self.assertEqual(die.show_state().loc[3, 'weights'], 2.0)

    def test_roll(self):
        die = Die(np.array([1, 2, 3, 4, 5, 6]))
        rolls = die.roll(10)
        self.assertEqual(len(rolls), 10)

class TestGame(unittest.TestCase):
    
    def test_init(self):
        # Test valid init
        game = Game([self.die1, self.die2])
        self.assertIsInstance(game, Game)
        
        # Test with non-Die objects
        with self.assertRaises(TypeError):
            game = Game(["invalid", self.die2])

    def setUp(self):
        print("Setting up for a test...")
        self.die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        self.die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        self.game = Game([self.die1, self.die2])

    def test_play(self):
        self.game.play(5)
        self.assertIsNotNone(self.game._results)
        
    def test_show_results(self):
        self.game.play(5)
        self.assertIsInstance(self.game.show_results(), pd.DataFrame)


class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        self.die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        self.game = Game([self.die1, self.die2])
        self.analyzer = Analyzer(self.game)
    
    def test_init(self):
        # Test valid init
        analyzer = Analyzer(self.game)
        self.assertIsInstance(analyzer, Analyzer)
        
        # Test with non-Game object
        with self.assertRaises(ValueError):
            analyzer = Analyzer("invalid game object")

    def test_jackpot(self):
        self.game.play(5)
        result = self.analyzer.jackpot()
        print(type(result))
        self.assertTrue(isinstance(result, (int, np.integer)))
 
    def test_face_counts_per_roll(self):
        self.game.play(5)
        self.assertIsInstance(self.analyzer.face_counts_per_roll(), pd.DataFrame)
        
    def test_combo_count(self):
        self.game.play(5)
        self.assertIsInstance(self.analyzer.combo_count(), pd.DataFrame)
        
    def test_permutation_count(self):
        self.game.play(5)
        self.assertIsInstance(self.analyzer.permutation_count(), pd.DataFrame)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
