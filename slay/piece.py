from abc import ABC, abstractclassmethod
from tile import Tile
from typing import Tuple

class Piece(ABC):
    '''
    Abstract class for a game piece. Pieces can be moveable or fixed in place, can
    provide different levels of protection for surrounding tiles, or can be moved
    to overtake neighboring tiles.
    '''

    MAX_SOLDIER_LEVEL = 4

    def __init__(self):
        pass

    @property
    @abstractclassmethod
    def power(self) -> int:
        ...

    @property
    @abstractclassmethod
    def name(self) -> str:
        ...

    @property
    @abstractclassmethod
    def moveable(self) -> bool:
        ...

    @property
    @abstractclassmethod
    def turn_cost(self) -> int:
        ...

    @property
    @abstractclassmethod
    def initial_cost(self) -> int:
        ...

    @property
    @abstractclassmethod
    def purchasable(self) -> bool:
        ...

    @property
    @abstractclassmethod
    def upgradeable(self) -> bool:
        ...

    #TODO: fill in other descriptors and rules as necessary, make this as general as possible
    #      so that other pieces can be made in the future

class Hut(Piece):
    power = 1
    name = "hut"
    moveable = False
    turn_cost = 0
    initial_cost = 0
    purchasable = False
    upgradeable = False

class Fort(Piece):
    power = 2
    name = "fort"
    moveable = False
    turn_cost = 0
    initial_cost = 15
    purchasable = True
    upgradeable = False

class Soldier1(Piece):
    power = 1
    name = "soldier1"
    moveable = True
    turn_cost = 2
    initial_cost = 10
    purchasable = True
    upgradeable = True

class Soldier2(Piece):
    power = 2
    name = "soldier2"
    moveable = True
    turn_cost = 6
    initial_cost = 20
    purchasable = True
    upgradeable = True

class PalmTree(Piece):
    power = 0
    name = "palmtree"
    moveable = False
    turn_cost = 1
    initial_cost = 0
    purchasable = False
    upgradeable = False