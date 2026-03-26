from view import *
from model_part1 import *

class Controller:
    def __init__(self, view: View, mode: Seed, watering_can: WateringCan):
        self.view = view
        self.mode = mode
        self.watering_can = watering_can
        
        self.player = Player(self.mode.get_starting_pesos())
        rows, cols = self.mode.get_grid_size()
        self.farm = Farm(rows, cols)
        
        self.crops = self.mode.get_crop()
    
    def run(self):
        self.view.print_grid(self.farm, self.player)
        
        while True:
            action: str = self.view.ask_for_action()
            
            if action == "p":
                self.plant_action()
            elif action == "w":
                self.water_action()
            elif action == "h":
                self.harvest_action()
            elif action == "n":
                self.next_day_action()
            elif action == "g":
                self.view.print_grid(self.farm, self.player)

    def plant_action(self):
        crop_name = self.view.ask_for_crop(self.crops)
        if not crop_name:
            return
        
        coords = self.view.ask_for_location()
        if not coords:
            return
        
        i, j = coords
        if self.farm.plant(self.crops[crop_name](), i, j, self.player):
            self.view.success()
        else:
            self.view.failed()
            
    def water_action(self):
        coords = self.view.ask_for_location()
        if not coords:
            return
        
        i, j = coords
        if self.farm.water(i, j, self.watering_can):
            self.view.success()
        else:
            self.view.failed()
    
    def harvest_action(self):
        if self.farm.harvest(self.player):
            self.view.success()
        else:
            self.view.failed()
    
    def next_day_action(self):
        self.farm.next_day(self.player)
        print("Day ended.")
        self.view.print_grid(self.farm, self.player)