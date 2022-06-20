from abc import ABC, abstractclassmethod
from tile import Tile

class Piece(ABC):
    '''
    Abstract class for a game piece. Pieces can be moveable or fixed in place, can
    provide different levels of protection for surrounding tiles, or can be moved
    to overtake neighboring tiles.
    '''

    def __init__(self, tile: 'Tile'=None):
        self.tile = tile

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

    #TODO: fill in other descriptors and rules as necessary, make this as general as possible
    #      so that other pieces can be made in the future

class Hut(Piece):
    power = 1
    name = "Hut"
    moveable = False
    turn_cost = 0
    initial_cost = 0
    purchasable = False

class Fort(Piece):
    power = 2
    name = "Fort"
    moveable = False
    turn_cost = 0
    initial_cost = 15
    purchasable = True

class SoldierOne(Piece):
    power = 1
    name = "Soldier"
    moveable = True
    turn_cost = 2
    initial_cost = 10
    purchasable = True

class SoldierTwo(Piece):
    power = 2
    name = "Spearman"
    moveable = True
    turn_cost = 6
    initial_cost = 20
    purchasable = True
