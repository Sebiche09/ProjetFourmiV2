import argparse
import time
#from colorama import Fore, Style, init
from simulation.colony import AntColony
from gui import run_simulation_gui

def show_help():
    print("Liste des commandes disponibles:")
    print("help - Afficher cette aide")
    print("exit - Quitter le programme")
    print("simulate - Lancer la simulation")

def run_simulation_cli(ant_colony, simulation_time):
    """
    Exécute une simulation en mode ligne de commande d'une colonie
     de fourmis pendant une période donnée.

    PRE:
    - ant_colony est une instance valide de la classe AntColony.
    - simulation_time est un nombre entier ou flottant
    représentant la durée de la simulation en secondes.

    POST:
    - La simulation de la colonie de fourmis est exécutée pendant la durée spécifiée.
    - Aucune modification permanente de l'état de la colonie n'est effectuée par cette fonction.
    - Affiche le nombre de larves et de fourmis à la fin de la simulation.
    SEB
    """
    try:
        for _ in range(int(simulation_time)):
            ant_colony.simulate_time_passing(1)
            time.sleep(1)

        larva_count = ant_colony.get_larva_count()
        ant_count = ant_colony.get_ant_count()
        print(f"Nombre d'oeufs: {larva_count}")
        print(f"Nombre de fourmis: {ant_count}")
    except AttributeError as e:
        raise RuntimeError(
            "La classe AntColony doit implémenter les méthodes simulate_time_passing,"
            " get_larva_count et get_ant_count.") from e
    except ValueError as e:
        # Si simulation_time n'est pas convertible en entier
        raise ValueError("La durée de simulation doit être un nombre entier.") from e


def main(ant_colony):
    """
    Fonction principale pour lancer la simulation de gestion d'une colonie de fourmis.

    PRE:
    - ant_colony est une instance valide de la classe AntColony.

    POST:
    - La fonction permet à l'utilisateur de choisir entre
    lancer une simulation en mode GUI ou en mode CLI.
    - Affiche les types de fourmis générés pendant la simulation si l'utilisateur le demande.
    - La simulation continue tant que l'utilisateur souhaite poursuivre.
    MAX
    """
    print("Bienvenue dans le simulateur de colonie de fourmis!")
    show_help()

    while True:
        try:
            user_input = input("Entrez une commande (help pour afficher l'aide): ").lower()

            if user_input == "help":
                show_help()
            elif user_input == "exit":
                print("Au revoir!")
                break
            elif user_input == "simulate":
                temps_simulation = input("Combien de temps voulez-vous faire avancer la simulation? ")
                if not temps_simulation.isdigit():
                    print("Erreur: La durée de simulation doit être un nombre entier.")
                else:
                    temps_simulation = int(temps_simulation)
                    if temps_simulation <= 0:
                        print("Erreur: La durée de simulation doit être un nombre positif.")
                    else:
                        run_simulation_cli(ant_colony, temps_simulation)
            elif user_input.startswith('kill'):
                # Récupérez le type de fourmi à tuer à partir de la commande
                ant_type_to_kill = user_input[len('kill'):].strip().capitalize()
                ant_colony.kill_ant_by_type(ant_type_to_kill)
                ant_colony.show_generated_ant_types()

            else:
                print("Commande non reconnue. Utilisez help pour afficher les commandes disponibles.")

            print("killFourmi - Tuer une fourmi")
            afficher_types_fourmis = input(
                "Afficher les types de fourmis générés pendant la simulation ? (Oui/Non): ").lower()
            if afficher_types_fourmis == "oui":
                ant_colony.show_generated_ant_types()

            continuer_simulation = input("Voulez-vous continuer la simulation? (Oui/Non): ").lower()
            if continuer_simulation != "oui":
                break
        except KeyboardInterrupt:
            print("\nSimulation interrompue par l'utilisateur.")
            break


if __name__ == "__main__":
    ant_colony = AntColony()
    main(ant_colony)
