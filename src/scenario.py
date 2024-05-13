__author__ = 'Felix A. Goebel'

import glob
from enum import Enum

# Enumeration of scenario names for 'better' code readability
class Scenarios(Enum):
    
    WARMING = 1
    FLOODING = 4
    SPACE = 5
    MOBILITY = 2
    ANIMALS = 3
    POLLUTION = 7
    NATURE = 6
    ENERGIES = 8

# Scenario based folders for AI images
# Keep track of images that were already displayed
class Scenario:
    
    def __init__(self, scenario) -> None:
        self.name = f"{scenario}"
        self.index = 0
        self.image_list = glob.glob(f"**/{scenario}/*")
    
    def __repr__(self) -> str:
        return f'\tScenario --- {self.name}\n\tPath --- {self.image_list[self.index]}'
    
    # Function: return the corresponding scenario of the selected combination set
    def select(selected_set:set[int]) -> object:
        # transform the given selected set into a string, a list of sorted numbers (key of the dictionary below)
        selection_string = ','.join(map(lambda s: str(s), sorted(selected_set)))
        scenarios = {
            f"{Scenarios.WARMING.value},{Scenarios.FLOODING.value}": warming_flood,
            f"{Scenarios.WARMING.value},{Scenarios.SPACE.value}": warming_space,
            f"{Scenarios.WARMING.value},{Scenarios.MOBILITY.value}": warming_mobility,
            f"{Scenarios.WARMING.value},{Scenarios.ANIMALS.value}": warming_animals,
            f"{Scenarios.WARMING.value},{Scenarios.POLLUTION.value}": warming_pollution,
            f"{Scenarios.WARMING.value},{Scenarios.ENERGIES.value}": warming_energies,
            f"{Scenarios.WARMING.value},{Scenarios.NATURE.value}": warming_nature,
            f"{Scenarios.FLOODING.value},{Scenarios.SPACE.value}": flood_space,
            f"{Scenarios.FLOODING.value},{Scenarios.MOBILITY.value}": flood_mobility,
            f"{Scenarios.FLOODING.value},{Scenarios.ANIMALS.value}": flood_animals,
            f"{Scenarios.FLOODING.value},{Scenarios.POLLUTION.value}": flood_pollution,
            f"{Scenarios.FLOODING.value},{Scenarios.ENERGIES.value}": flood_energies,
            f"{Scenarios.FLOODING.value},{Scenarios.NATURE.value}": flood_nature,
            f"{Scenarios.SPACE.value},{Scenarios.MOBILITY.value}": space_mobility,
            f"{Scenarios.SPACE.value},{Scenarios.ANIMALS.value}": space_animals,
            f"{Scenarios.SPACE.value},{Scenarios.POLLUTION.value}": space_pollution,
            f"{Scenarios.SPACE.value},{Scenarios.ENERGIES.value}": space_energies,
            f"{Scenarios.SPACE.value},{Scenarios.NATURE.value}": space_nature,
            f"{Scenarios.MOBILITY.value},{Scenarios.ANIMALS.value}": mobility_animals,
            f"{Scenarios.MOBILITY.value},{Scenarios.POLLUTION.value}": mobility_pollution,
            f"{Scenarios.MOBILITY.value},{Scenarios.ENERGIES.value}": mobility_energies,
            f"{Scenarios.MOBILITY.value},{Scenarios.NATURE.value}": mobility_nature,
            f"{Scenarios.ANIMALS.value},{Scenarios.POLLUTION.value}": animals_pollution,
            f"{Scenarios.ANIMALS.value},{Scenarios.ENERGIES.value}": animals_energies,
            f"{Scenarios.ANIMALS.value},{Scenarios.NATURE.value}": animals_nature,
            f"{Scenarios.POLLUTION.value},{Scenarios.ENERGIES.value}": pollution_energies,
            f"{Scenarios.POLLUTION.value},{Scenarios.NATURE.value}": pollution_nature,
            f"{Scenarios.ENERGIES.value},{Scenarios.NATURE.value}": energies_nature
        }
        return scenarios.get(selection_string, None)
        

# 28 Categories (Scenarios)
warming_flood = Scenario('warming_flood')
warming_space = Scenario('warming_space')
warming_mobility = Scenario('warming_mobility')
warming_animals = Scenario('warming_animals')
warming_pollution = Scenario('warming_pollution')
warming_energies = Scenario('warming_energies')
warming_nature = Scenario('warming_nature')
flood_space = Scenario('flood_space')
flood_mobility = Scenario('flood_mobility')
flood_animals = Scenario('flood_animals')
flood_pollution = Scenario('flood_pollution')
flood_energies = Scenario('flood_energies')
flood_nature = Scenario('flood_nature')
space_mobility = Scenario('space_mobility')
space_animals = Scenario('space_animals')
space_pollution = Scenario('space_pollution')
space_energies = Scenario('space_energies')
space_nature = Scenario('space_nature')
mobility_animals = Scenario('mobility_animals')
mobility_pollution = Scenario('mobility_pollution')
mobility_energies = Scenario('mobility_energies')
mobility_nature = Scenario('mobility_nature')
animals_pollution = Scenario('animals_pollution')
animals_energies = Scenario('animals_energies')
animals_nature = Scenario('animals_nature')
pollution_energies = Scenario('pollution_energies')
pollution_nature = Scenario('pollution_nature')
energies_nature = Scenario('energies_nature') 