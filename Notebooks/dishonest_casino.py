"""
python implementation of the dishonest casino example.
"""

import random
import bisect
import numpy as np


class Dice:
    """
    A dice with arbitrary probability (not necessary a fair dice)
    """
    def __init__(self, prob_vector):
        """
        :type prob_vector: list
        """
        if (min(prob_vector) < 0) | (not np.isclose(sum(prob_vector), 1)):
            raise ValueError('Invalid probability vector')
        self.prob_vector = [sum(prob_vector[:i+1])
                            for i in range(len(prob_vector))]

    def roll(self, n):
        """
        Roll the dice
        :type n: int
        """
        rand_values = [random.random() for _ in range(n)]
        dice_values = [bisect.bisect_right(self.prob_vector, i) + 1
                       for i in rand_values]
        return dice_values


def dishonest_casino_play(n, fair_prob=(1./6, 1./6, 1./6, 1./6, 1./6, 1./6),
                          unfair_prob=(0.1, 0.1, 0.1, 0.1, 0.1, 0.5),
                          prob_switch_to_unfair=0.05,
                          prob_switch_to_fair=0.1,
                          initial_dice=0):
    """
    Simulate n rolls of dice
    :param n: the number of rolls
    :param fair_prob: list, the probabilities for the fair dice
    :param unfair_prob: list, the probabilities for the loaded dice
    :param prob_switch_to_unfair: float, probability of switch from
                                  fair to loaded
    :param prob_switch_to_fair: float, probability of switch from
                                loaded to fair
    :param initial_dice: the first dice used (0 for fair dice)
    :return: a tuple with two list
            (i.e. the sequence of dices used, hidden states and
            the values obtained, observations)
    """
    fair_dice = Dice(fair_prob)
    loaded_dice = Dice(unfair_prob)
    available_dices = (fair_dice, loaded_dice)
    used_dices = [initial_dice]
    values = []
    for _ in range(n):
        current_dice = available_dices[used_dices[-1]]
        values.append(current_dice.roll(1)[0])
        # Switch dices with some probability
        if used_dices[-1] == 0:
            # Switch to unfair dice with probability equal
            # to prob_switch_to_unfair
            used_dices.append(int(random.random() < prob_switch_to_unfair))
        else:
            # Switch to fair dice with probability equal
            # to prob_switch_to_fair
            used_dices.append(int(random.random() >= prob_switch_to_fair))
    return used_dices[:-1], values
 
