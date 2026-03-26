import argparse
from controller import Controller
from view import View
from model_part1 import AnimalCrossing, PVZ, BasicCan, SteelCan, Seed, WateringCan
from model_part2 import StardewValley, KoyukiAndCans, WaterBucket
from typing import Callable
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True)
    parser.add_argument("--water", required=True)
    
    args = parser.parse_args()
    mode_mapping: dict[str, Callable[[], Seed]] = {
        "ac": AnimalCrossing,
        "pvz": PVZ,
        "svd": StardewValley
    }
    
    watering_can_mapping: dict[str, Callable[[], WateringCan]] = {
        "basic": BasicCan,
        "steel": SteelCan,
        "koyuki": KoyukiAndCans,
        "bucket": WaterBucket
    }
    
    mode = mode_mapping[args.mode]()
    watering_can = watering_can_mapping[args.water]()
    
    view = View()
    game = Controller(view, mode, watering_can)
    game.run()

if __name__ == "__main__":
    main()