import argparse
from controller import Controller
from view import View
from model_part1 import AnimalCrossing, PVZ, BasicCan, SteelCan

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True)
    parser.add_argument("--water", required=True)
    
    args = parser.parse_args()
    
    if args.mode == "ac":
        mode = AnimalCrossing()
    elif args.mode == "pvz":
        mode = PVZ()
    else:
        print("Invalid mode")
        return
    
    if args.water == "basic":
        watering_can = BasicCan()
    elif args.water == "steel":
        watering_can = SteelCan()
    else:
        print("Invalid watering can")
        return
    view = View()
    game = Controller(view, mode, watering_can)
    game.run()

if __name__ == "__main__":
    main()