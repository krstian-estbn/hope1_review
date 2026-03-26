from typing import Callable

from model_part1 import *
from rev.model_part1 import Crop
class Parsnip(Crop):
    def __init__(self):
        super().__init__(100, 1, 200, "p", "P")
        
class SweetGemBerry(Crop):
    def __init__(self):
        super().__init__(300, 3, 1000, "g", "G")
        self.watered_yesterday: bool = False
        
    def next_day(self):
        if self.watered and self.watered_yesterday:
            self.current_day += 1
        self.watered_yesterday = self.watered
        self.watered = False

class AncientFruit(Crop):
    def __init__(self):
        super().__init__(1000, 14, 6700, "a", "A")
        self.watered_consecutively: int = 0
    
    def next_day(self):
        if self.watered:
            self.watered_consecutively += 1
            self.current_day += self.watered_consecutively
        else:
            self.watered_consecutively = 0
        self.watered = False
       
       
class StardewValley(Seed):
    def get_starting_pesos(self) -> int:
        return 400
    
    def get_grid_size(self) -> tuple[int, int]:
        return (9, 9)

    def get_crop(self) -> dict[str, Callable[[], Crop]]:
        return {"parsnip": Parsnip,
                "sweet_gem_berry": SweetGemBerry,
                "ancient_fruit": AncientFruit}

class KoyukiAndCans(WateringCan):
    def get_cells(self, i: int, j: int, rows: int, cols: int) -> list[tuple[int, int]]:
        cells: list[tuple[int, int]] = []
        
        for di in range(rows):
            for dj in range(cols):
                if abs(i - di) + abs(j - dj) <= 3:
                    cells.append((di, dj))
        return cells
    
class WaterBucket(WateringCan):
    def get_cells(self, i: int, j: int, rows: int, cols: int) -> list[tuple[int, int]]:
        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = [(i, j)]
        while stack:
            ci, cj = stack.pop()
            if (ci, cj) in visited:
                continue
            
            visited.add((ci, cj))
            if 0 <= ci < rows and 0 <= cj < cols:
                for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    ni, nj = ci + di, cj + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        stack.append((ni, nj))
        
        return list(visited)