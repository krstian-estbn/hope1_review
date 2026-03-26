from typing import Optional, Callable
from common_types import Player
from abc import ABC, abstractmethod

class Crop:
    def __init__(self, cost: int, days_to_grow: int, harvest_value: int, growing_sprite: str, harvesting_sprite: str):
        self.cost = cost
        self.days_to_grow = days_to_grow
        self.harvest_value = harvest_value
        self.growing_sprite = growing_sprite
        self.harvesting_sprite = harvesting_sprite
        
        self.current_day: int = 0
        self.watered: bool = False
    
    def water(self):
        self.watered = True
    
    def next_day(self):
        if self.watered:
            self.current_day += 1
        self.watered = False

    def is_harvestable(self) -> bool:
       return self.current_day >= self.days_to_grow
   
    def get_sprite(self):
        return self.harvesting_sprite if self.is_harvestable() else self.growing_sprite

class Turnip(Crop):
    def __init__(self):
        super().__init__(300, 2, 500, "t", "T")

class Sunflower(Crop):
    def __init__(self):
        super().__init__(25, 1, 50, "s", "S")
        
class Marigold(Crop):
    def __init__(self):
        super().__init__(50, 2, 150, "m", "M")


class WateringCan(ABC):
    @abstractmethod
    def get_cells(self, i: int, j: int, rows: int, cols: int) -> list[tuple[int, int]]:
        raise NotImplemented
    
class BasicCan(WateringCan):
    def get_cells(self, i: int, j: int, rows: int, cols: int) -> list[tuple[int, int]]:
        return [(i, j)]

class SteelCan(WateringCan):
    def get_cells(self, i: int, j: int, rows: int, cols: int) -> list[tuple[int, int]]:
        cells: list[tuple[int, int]] = []
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                ni, nj = i + di , j + dj
                if 0 <= ni < rows and 0 <= nj < cols:
                    cells.append((ni, nj))
        return cells

class Farm:
    def __init__(self, m: int, n: int):
        self.m = m
        self.n = n
        self.grid: list[list[Optional[Crop]]] = [[None for _ in range(self.n)] for _ in range(self.m)]

    def in_bounds(self, i: int, j: int) -> bool:
        return 0 <= i < self.m and 0 <= j < self.n

    def plant(self, crop: Crop, i: int, j: int, player: Player) -> bool:
        if not self.in_bounds(i, j):
            return False
        if self.grid[i][j] is not None:
            return False
        if player.pesos < crop.cost:
            return False
    
        self.grid[i][j] = crop
        player.pesos -= crop.cost
        return True
    
    def water(self, i: int, j: int, watering_can: WateringCan) -> bool:
        if not self.in_bounds(i, j):
            return False
        
        cells = watering_can.get_cells(i, j, self.m, self.n)
        
        for r, c in cells:
            if self.grid[r][c] is not None:
                crop: Crop = self.grid[r][c]
                crop.water()
        
        return True
    
    def harvest(self, player: Player) -> bool:
        total = 0
        for i in range(self.m):
            for j in range(self.n):
                crop: Optional[Crop] = self.grid[i][j]
                if crop and crop.is_harvestable():
                    total += crop.harvest_value
                    self.grid[i][j] = None
        
        if total == 0:
            return False
        
        player.pesos += total
        return True
    
    def next_day(self, player: Player):
        for i in range(self.m):
            for j in range(self.n):
                crop: Optional[Crop] = self.grid[i][j]
                if crop:
                    crop.next_day()
                    
        player.day += 1
    

class Seed(ABC):
    @abstractmethod
    def get_starting_pesos(self) -> int:
        pass
        
    @abstractmethod
    def get_grid_size(self) -> tuple[int, int]:
        pass
        
    @abstractmethod
    def get_crop(self) -> dict[str, Callable[[], Crop]]:
        pass

class AnimalCrossing(Seed):
    def get_starting_pesos(self):
        return 1000
    
    def get_grid_size(self) -> tuple[int, int]:
        return (5, 5)
    
    def get_crop(self) -> dict[str, Callable[[], Crop]]:
        return {"turnip": Turnip}

class PVZ(Seed):
    def get_starting_pesos(self):
        return 100
    
    def get_grid_size(self) -> tuple[int, int]:
        return (5, 9)
    
    def get_crop(self) -> dict[str, Callable[[], Crop]]:
        return {"sunflower": Sunflower,
                "marigold": Marigold}