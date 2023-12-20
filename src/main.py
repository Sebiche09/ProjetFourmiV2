"""Modules"""
import time
from simulation.colony import AntColony
from gui import run_simulation_gui
from colorama import Fore, Style
from simulation.noise_map import generate_noise_map


# ------------------------------------------------------------------------
def show_welcome():
    welcome_message = "Bienvenue dans le simulateur de colonie de fourmis!"
    colored_welcome = f"{Fore.CYAN}{Style.BRIGHT}{welcome_message}{Style.RESET_ALL}"
    frame_width = max(len(welcome_message) + 4, 40)
    print(f"{Fore.BLUE}+{'-' * (frame_width - 2)}+{Style.RESET_ALL}")
    print(f"{Fore.GREEN}|{' ' * (frame_width - 2)}|{Style.RESET_ALL}")
    print(f"{Fore.GREEN}|{colored_welcome.center(frame_width - 2)}|{Style.RESET_ALL}")
    print(f"{Fore.GREEN}|{' ' * (frame_width - 2)}|{Style.RESET_ALL}")
    print(f"{Fore.BLUE}+{'-' * (frame_width - 2)}+{Style.RESET_ALL}\n")


def show_help():
    print(f"{Fore.BLUE}Liste des commandes disponibles:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}help{Style.RESET_ALL} - Afficher cette aide")
    print(f"{Fore.RED}exit{Style.RESET_ALL} - Quitter le programme")
    print(f"{Fore.YELLOW}simulate-cli{Style.RESET_ALL} - Lancer la simulation en ligne de commande")
    print(f"{Fore.YELLOW}simulate-gui{Style.RESET_ALL} - Lancer la simulation en interface graphique")


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
    print(f"Nombre d'oeufs: {larva_count}")
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
    show_welcome()
    show_help()

    while True:
        try:
            user_input = input(f"{Fore.CYAN}Entrez une commande (help pour afficher l'aide): {Style.RESET_ALL}").lower()
            if user_input == "help":
                show_help()
            elif user_input == "exit":
                print("Au revoir!")
                break
            elif user_input == "simulate-cli":
                temps_simulation = input("Combien de temps voulez-vous faire "
                                         "avancer la simulation? ")
                temps_simulation = int(temps_simulation)
                if not isinstance(temps_simulation, int) and temps_simulation <= 0:
                    raise ValueError("La durée de simulation doit être un nombre entier.")
                else:
                    run_simulation_cli(ant_colony, temps_simulation)
            elif user_input == "simulate-gui":
                run_simulation_gui(ant_colony)
            elif user_input.startswith('kill'):

                parts = user_input.split()
                if len(parts) == 3 and parts[1].isdigit():
                    ant_type_to_kill = parts[2].capitalize()
                    num_to_kill = int(parts[1])
                    ant_colony.kill_ant_by_type(ant_type_to_kill, num_to_kill)
                    ant_colony.show_generated_ant_types()
                else:
                    print("Commande kill incorrecte. Utilisation correcte: kill [nombre] [type]")

            else:
                print("Commande non reconnue. Utilisez help pour "
                      "afficher les commandes disponibles.")

            print("kill nbr type - Tuer une fourmi")
            afficher_types_fourmis = input(
                "Afficher les types de fourmis générés pendant la simulation ? (Oui/Non): ").lower()
            if afficher_types_fourmis == "oui":
                ant_colony.show_generated_ant_types()

            continuer_simulation = input("Voulez-vous continuer la simulation? (Oui/Non): ").lower()
            if continuer_simulation != "oui":
                break
        except KeyboardInterrupt as e:
            print(f"\n{Fore.RED}Simulation interrompue par l'utilisateur.{Style.RESET_ALL}")
            break


if __name__ == "__main__":
    try:
        ant_colony = AntColony()
        generate_noise_map(100, 100, 10, 5, 0.5, 2, 0)
        main(ant_colony)
    except ValueError as e:
        print(f"erreur valeur : {e}")
    except TypeError as e:
        print(f"erreur type : {e}")
