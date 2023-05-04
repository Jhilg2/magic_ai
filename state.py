from typing import Union
from player import Player
from constants import Phase

class State(object):

    def __init__(self):
        super(State, self).__init__()
        self.player1 = Player()
        self.player2 = Player()
        self.phase = Phase.PLAY

    def peform_action(action: Union[])