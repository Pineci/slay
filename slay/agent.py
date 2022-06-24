from abc import ABC, abstractmethod
from typing import Tuple
from piece import Piece

class Agent(ABC):

    def __init__(self):
        pass

    def select_piece(self, tile_coord: Tuple[int, int]) -> Piece:
        pass
    
    def place_piece(self, tile_coord: Tuple[int, int], piece: Piece) -> None:
        pass