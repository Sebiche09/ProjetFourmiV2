import argparse
import time
from simulation.colony import AntColony
from gui import run_simulation_gui


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
    for _ in range(int(simulation_time)):
        ant_colony.simulate_time_passing(1)
        time.sleep(1)

    larva_count = ant_colony.get_larva_count()
    ant_count = ant_colony.get_ant_count()
    print(f"Nombre de larves: {larva_count}")
    print(f"Nombre de fourmis: {ant_count}")


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
    while True:
        parser = argparse.ArgumentParser(description='Simulation de gestion de colonie de fourmis')
        parser.add_argument('--gui', action='store_true', help='Lancer l\'interface graphique')

        args = parser.parse_args()

        if args.gui:
            run_simulation_gui(ant_colony)
        else:
            temps_simulation = input("Combien de temps voulez-vous faire avancer la simulation? ")
            run_simulation_cli(ant_colony, temps_simulation)

        afficher_types_fourmis = input(
            "Afficher les types de fourmis générés pendant la simulation ? (Oui/Non): ").lower()
        if afficher_types_fourmis == "oui":
            ant_colony.show_generated_ant_types()

        continuer_simulation = input("Voulez-vous continuer la simulation? (Oui/Non): ").lower()
        if continuer_simulation != "oui":
            break


if __name__ == "__main__":
    colony = AntColony()
    main(colony)
