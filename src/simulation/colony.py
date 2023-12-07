import random
import time
from .ant import Queen, Larva, Ant, SlaverAnt, NurseAnt, SlaveAnt, MaleAnt, SoldierAnt
from collections import defaultdict


class AntColony:
    def __init__(self):
        self.queen = Queen()
        self.larvae = []
        self.__time = 0
        self.generated_ant_types = []
        self.dicAnt = {}

    @property
    def time(self):
        return self.__time

    def simulate_time_passing(self, time_units):
        for _ in range(time_units):
            self.__time += 1
            print(f"Temps passé: {self.__time} unité(s)")

            new_larva = self.queen
            if new_larva:
                print("La reine a pondu un œuf.")
                self.add_larva(new_larva)
                new_ant = new_larva.hatch()
                print(f"Une nouvelle fourmi ({new_ant.ant_type}) est née!")
                self.queen.accept_new_ant(new_ant)
                self.remove_larva(new_larva)
                self.generated_ant_types.append(new_ant.ant_type)
            else:
                print("La reine n'a pas pondu d'œuf.")
        print(f"Nombre de larves : {len(self.larvae)}")
        print(f"Nombre de fourmis : {len(self.queen.accepted_ants)}")
        print(f"Types de fourmis générés : {self.generated_ant_types}")

    def show_generated_ant_types(self):
        print("\nTypes de fourmis générés pendant la simulation:")

        ant_type_counts = defaultdict(int)

        for ant_type in self.generated_ant_types:
            ant_type_counts[ant_type] += 1

        if not ant_type_counts:
            print("Aucune fourmi générée.")
        else:
            for ant_type, count in ant_type_counts.items():
                print(f"{ant_type}: {count}")

    def get_larva_count(self):
        return len(self.larvae)

    def get_ant_count(self):
        return sum(1 for larva in self.larvae if larva.age >= larva.time_to_hatch) + len(self.queen.accepted_ants)

    def add_larva(self, larva):
        self.larvae.append(larva)

    def remove_larva(self, larva):
        self.larvae.remove(larva)
