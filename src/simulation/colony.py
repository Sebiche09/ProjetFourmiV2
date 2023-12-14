import random
import time
from .ant import Queen, Larva, Ant, SlaverAnt, NurseAnt, SlaveAnt, MaleAnt, SoldierAnt
from collections import defaultdict
from random import choice


class AntColony:
    def __init__(self):
        self.queen = Queen()
        self.larvae = []
        self.__time = 0
        self.generated_ant_types = []
        self.dicAnt = {}
        self.killed_ant_types = []
        self.max_larvae_spawn = 10
        self.max_ants_spawn = 10

    @property
    def time(self):
        return self.__time

    def simulate_time_passing(self, time_units):
        for _ in range(time_units):
            self.__time += 1
            print(f"Temps passé: {self.__time} unité(s)")

            # Spawn multiple larvae
            num_larvae = random.randint(1, self.max_larvae_spawn)
            for _ in range(num_larvae):
                new_larva = self.queen.lay_eggs()
                if new_larva:
                    print("La reine a pondu un œuf.")
                    self.larvae.append(new_larva)

            # Éclosion des larves en fourmis
            for larva in self.larvae:
                larva.age += 1
                if larva.age >= larva.time_to_hatch:
                    num_ants = random.randint(1, self.max_ants_spawn)
                    for _ in range(num_ants):
                        new_ant = larva.hatch()
                        print(f"Une nouvelle fourmi ({new_ant.ant_type}) est née!")
                        self.queen.accept_new_ant(new_ant)
                        self.generated_ant_types.append(new_ant.ant_type)

            # Ajoutez le code pour créer une nouvelle fourmi à chaque unité de temps
            num_new_ants = random.randint(1, self.max_ants_spawn)
            for _ in range(num_new_ants):
                new_ant_type = random.choice(["Male", "Nurse", "Slaver", "Slave", "Soldier"])
                new_ant = Ant(new_ant_type)
                print(f"Une nouvelle fourmi ({new_ant_type}) est née !")
                self.queen.accept_new_ant(new_ant)
                self.generated_ant_types.append(new_ant_type)

            print(f"Nombre de larves : {len(self.larvae)}")
            print(f"Nombre de fourmis : {len(self.queen.accepted_ants)}")
            print(f"Types de fourmis générés : {self.generated_ant_types}")

    def show_generated_ant_types(self):
        print("\nTypes de fourmis générés pendant la simulation:")
        # Exclure les types de fourmis tuées de la liste des types générés
        remaining_ant_types = [ant_type for ant_type in self.generated_ant_types if
                               ant_type.lower() not in self.killed_ant_types]
        ant_type_counts = defaultdict(int)

        for ant_type in remaining_ant_types:
            ant_type_counts[ant_type] += 1

        if not ant_type_counts:
            print("Aucune fourmi générée.")
        else:
            for ant_type, count in ant_type_counts.items():
                print(f"{ant_type}: {count}")

    def get_larva_count(self):
        return len(self.larvae)

    def get_ant_count(self):
        return (sum(1 for larva in self.larvae if larva.age >= larva.time_to_hatch) +
                len(self.queen.accepted_ants))

    def add_larva(self, larva):
        self.larvae.append(larva)

    def remove_larva(self, larva):
        self.larvae.remove(larva)

    def kill_ant_by_type(self, ant_type):
        if self.queen.accepted_ants:
            # Filtrer les fourmis du type spécifié
            ant_type_lower = ant_type.lower()
            ants_to_kill = [ant for ant in self.queen.accepted_ants if ant.ant_type.lower() == ant_type_lower]

            if ants_to_kill:
                # Choisir une fourmi du type spécifié au hasard et la tuer
                ant_to_kill = random.choice(ants_to_kill)
                self.queen.accepted_ants.remove(ant_to_kill)
                print(f"{ant_to_kill.ant_type} a été tuée.")

                # Mettre à jour la liste des types générés
                self.generated_ant_types = [ant_type for ant_type in self.generated_ant_types if
                                            ant_type.lower() != ant_type_lower]
            else:
                print(f"Aucune fourmi du type {ant_type} n'est disponible à tuer.")
        else:
            print("Aucune fourmi n'est disponible à tuer.")
