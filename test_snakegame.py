import random
import unittest

from snakegame import change_direction, hits_wall, place_food, random_cell, step

UP, DOWN, LEFT, RIGHT = (0, -20), (0, 20), (-20, 0), (20, 0)
FAR_FOOD = (0, 0)


class ChangeDirectionTests(unittest.TestCase):
    def test_can_start_moving_any_direction(self):
        for d in (UP, DOWN, LEFT, RIGHT):
            self.assertEqual(change_direction((0, 0), d), d)

    def test_can_turn(self):
        self.assertEqual(change_direction(RIGHT, UP), UP)
        self.assertEqual(change_direction(UP, LEFT), LEFT)

    def test_cannot_reverse(self):
        self.assertEqual(change_direction(RIGHT, LEFT), RIGHT)
        self.assertEqual(change_direction(UP, DOWN), UP)


class StepTests(unittest.TestCase):
    def test_no_movement_before_first_key(self):
        snake = [(200, 200)]
        self.assertEqual(step(snake, (0, 0), FAR_FOOD, 0), (snake, FAR_FOOD, 0, False))

    def test_moves_without_growing(self):
        snake, food, score, died = step([(200, 200), (180, 200)], RIGHT, FAR_FOOD, 0)
        self.assertEqual(snake, [(220, 200), (200, 200)])
        self.assertEqual((food, score, died), (FAR_FOOD, 0, False))

    def test_eating_food_grows_snake_and_scores(self):
        snake, food, score, died = step([(200, 200)], RIGHT, (220, 200), 3, random.Random(1))
        self.assertEqual(snake, [(220, 200), (200, 200)])
        self.assertEqual(score, 4)
        self.assertFalse(died)
        self.assertNotIn(food, snake)

    def test_dies_at_each_wall(self):
        cases = [((380, 200), RIGHT), ((0, 200), LEFT), ((200, 0), UP), ((200, 380), DOWN)]
        for head, d in cases:
            with self.subTest(head=head, direction=d):
                self.assertTrue(step([head], d, FAR_FOOD, 0)[3])

    def test_dies_running_into_itself(self):
        # Head at (200,200) moving up into a body cell that won't move away this tick.
        snake = [(200, 200), (220, 200), (220, 180), (200, 180), (180, 180)]
        self.assertTrue(step(snake, UP, FAR_FOOD, 0)[3])

    def test_can_follow_own_tail(self):
        # The tail moves out of the way on the same tick, so this is safe.
        snake = [(200, 200), (220, 200), (220, 180), (200, 180)]
        self.assertFalse(step(snake, UP, FAR_FOOD, 0)[3])

    def test_does_not_modify_input_list(self):
        snake = [(200, 200)]
        step(snake, RIGHT, FAR_FOOD, 0)
        self.assertEqual(snake, [(200, 200)])


ALL_CELLS = [(x, y) for x in range(0, 400, 20) for y in range(0, 400, 20)]


class FoodTests(unittest.TestCase):
    def test_food_never_lands_on_snake(self):
        rng = random.Random(0)
        snake = ALL_CELLS[:-1]
        free = set(ALL_CELLS) - set(snake)
        for _ in range(20):
            self.assertIn(place_food(snake, rng), free)

    def test_food_can_reach_every_cell(self):
        rng = random.Random(0)
        seen = {random_cell(rng) for _ in range(10000)}
        self.assertEqual(seen, set(ALL_CELLS))

    def test_wall_edges(self):
        self.assertFalse(hits_wall((0, 0)))
        self.assertFalse(hits_wall((380, 380)))
        self.assertTrue(hits_wall((400, 0)))
        self.assertTrue(hits_wall((0, -20)))


if __name__ == "__main__":
    unittest.main()
