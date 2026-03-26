from model_part1 import *
from typing import Literal, Mapping, Callable
class View:
    def print_grid(self, farm: Farm, player: Player):
        print("====\n")
        print(f"Day {player.day}")
        print(f"Pesos: {player.pesos}")
        
        for row in farm.grid:
            print(' '.join(crop.get_sprite() if crop else '.' for crop in row))
        print()

    def ask_for_action(self) -> Literal["p", "w", "h", "n", "g"]:
        while True:
            action = input("Action:\n- ").strip().lower()
            if action not in ("p", "w", "h", "n", "g"):
                continue
            return action
    
    def ask_for_crop(self, crops: Mapping[str, Callable[[], Crop]]):
        print(f"Crops: {', '.join(crops.keys())}")
        crop = input("- ").strip().lower()
        
        if crop not in crops:
            self.failed()
            return

        return crop
        
    def ask_for_location(self):
        try:
            i, j = map(int, input("Location (i, j): \n- ").split())
        except Exception:
            self.failed()
            return
        return (i, j)
    
    def success(self):
        print("Success!")
    
    def failed(self):
        print("Failed.")
        
