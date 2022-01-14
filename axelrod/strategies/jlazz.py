"""Memory One strategies. Note that there are Memory One strategies in other
files, including titfortat.py and zero_determinant.py"""
'''
import warnings
from typing import Tuple

from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D

from .memoryone import MemoryOnePlayer


class jlazz(MemoryOnePlayer):

    name = "jlazz"

    def __init__(self) -> None:
        four_vector = (1, 0, 1, 0)
        super().__init__(four_vector)
        self.set_four_vector(four_vector)
'''
from axelrod.action import Action
C, D = Action.C, Action.D

from .zero_determinant import LRPlayer
from axelrod import Player

import numpy as np
'''
class jlazz(Player):
    """ A player starts by cooperating and then mimics previous move by opponent. """
    def strategy(self, opponent):
        """ Begins by playing 'C': This is affected by the history of the opponent: the strategy simply repeats the last action of the opponent """
        try:
            return opponent.history[-1]
        except IndexError:
            return C

    def __repr__(self):
        """ The string method for the strategy. """
        return 'jlazz'
'''


class jlazz(LRPlayer, Player):
    """
    An Extortionate Zero Determinant Strategy with l=P.

    Names:

    - Extort-2: [Stewart2012]_
    """

    def __init__(self, phi: float = 1 / 9, s: float = 1) -> None:
        # l = P will be set by receive_match_attributes
        super().__init__(phi, s, None)

    def receive_match_attributes(self):
        (R, P, S, T) = self.match_attributes["game"].RPST()
        self.l = P
        super().receive_match_attributes()

    def strategy(self, opponent: Player) -> Action:
        time = len(opponent.history)
        nrounnds = self.match_attributes["length"]
        if time == 0:
            return self._initial
        #set the new four vector to change extortion
        R, P, S, T = self.match_attributes["game"].RPST()
        #scores for each pair
        combscores = {
            (C, C): np.array([R, R]),
            (D, D): np.array([P, P]),
            (C, D): np.array([S, T]),
            (D, C): np.array([T, S]),
        }
        #find current average score
        a_score = np.array([0,0])
        for i in range(time):
            a_score += combscores[(self.history[i], opponent.history[i])]
        a_score = a_score/time
        #update s based on average
        if time> 100 and time%50==0:
            if a_score[0] < S+0.5:
                self.s =(self.s+1)/2#less extortionate
                print([self.s,time,'up'])
            elif a_score[0] < P+0.05 and a_score[0]> P-0.05:
            #elif a_score[0] < a_score[1]+0.05 and a_score[0]> a_score[1]-0.05:
                self.s =self.s*0.9#more extortionate
                print([self.s,time,'down'])
                
        
        l = self.l
        s = self.s
        phi = self.phi

        # Check parameters
        s_min = -min((T - l) / (l - S), (l - S) / (T - l))
        if (l < P) or (l > R) or (s > 1) or (s < s_min):
            raise ValueError

        p1 = 1 - phi * (1 - s) * (R - l)
        p2 = 1 - phi * (s * (l - S) + (T - l))
        p3 = phi * ((l - S) + s * (T - l))
        p4 = phi * (1 - s) * (l - P)

        four_vector = [p1, p2, p3, p4]
        self.set_four_vector(four_vector)
        # Determine which probability to use
        p = self._four_vector[(self.history[-1], opponent.history[-1])]
        # Draw a random number in [0, 1] to decide
        try:
            return self._random.random_choice(p)
        except AttributeError:
            return D if p == 0 else C
        

    def __repr__(self):
        """ The string method for the strategy. """
        return 'jlazz'

