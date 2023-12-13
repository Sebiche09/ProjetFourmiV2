"""module"""
import random
import pygame
import matplotlib.pyplot as plt
from simulation.ant import hatch
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from simulation.noise_map import generate_noise_map
from simulation.intelligence.simple_ai import (
    move as male_move, action as male_action, check_color_and_adjust as male_check_color_and_adjust)
from simulation.intelligence.advanced_ai import (
    move as soldier_move, action as soldier_action,
    check_color_and_adjust as soldier_check_color_and_adjust)

noise_map = generate_noise_map(3440, 1440, scale=135, octaves=1,
                               persistence=2, lacunarity=0.6, seed=random.randint(0,100))


def run_simulation_gui(ant_colony):
    """
    Exécute une simulation graphique d'une colonie de fourmis.

    PRE:
    - ant_colony est une instance valide de la classe AntColony.

    POST:
    - Lance une simulation graphique de la colonie de fourmis avec une interface utilisateur.
    - Aucune modification permanente de l'état de la colonie n'est effectuée par cette fonction.
    FLO
    """

    def draw_slider(window, position, width, height, value):
        pygame.draw.rect(window, (200, 200, 200), (position[0], position[1], width, height))
        pygame.draw.rect(window, (0, 0, 0), (position[0], position[1], width, height), 2)
        knob_position = (position[0] + int(value * width), position[1] + height // 2)
        pygame.draw.circle(window, (255, 0, 0), knob_position, 10)

    plt.imshow(noise_map, cmap='viridis', interpolation='nearest')
    plt.colorbar()
    plt.show()
    pygame.init()
    # --------------------------------------------- Infos screen
    # ------------------------------------------------------
    screen_info = pygame.display.Info()
    window_width, window_height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((window_width, window_height))
    # --------------------------------------------- Variables globales
    # -----------------------------------------------
    pygame.display.set_caption("Simulation de Colonie de Fourmis")
    background_color = (34, 139, 34)  # Vert Forêt
    ant_colony.queen.position = (window_width // 2, window_height // 2)
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    stop_button_rect = pygame.Rect(10, 10, 100, 30)
    stop_button_color = (255, 0, 0)
    pause_button_rect = pygame.Rect(10, 50, 150, 30)

    clock = pygame.time.Clock()

    digging_list = []
    running = True
    simulation_running = True
    paused = False
    simulation_speed = 1
    last_dig_direction = 0
    # --------------------------------------------- Début simulation
    # ----------------------------------------------
    while running and simulation_running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if stop_button_rect.collidepoint(event.pos):
                    simulation_running = not simulation_running
                if pause_button_rect.collidepoint(event.pos):
                    paused = not paused
                if event.button == 1:
                    # Vérifiez si le clic est sur le curseur
                    slider_rect = pygame.Rect(window_width // 2 - 100,
                                              window_height // 6 - 50, 200, 20)
                    if slider_rect.collidepoint(event.pos):
                        # Mettez à jour la position du curseur en fonction du clic
                        simulation_speed = (event.pos[0] - slider_rect.left) / slider_rect.width
        if not paused:
            screen.fill(background_color)
            pygame.draw.rect(screen, (255, 255, 255),
                             (window_width // 2 - 100, window_height // 2 - 100, 200, 200))
            pygame.draw.rect(screen, (255, 255, 255),
                             (window_width // 2 - 50, window_height // 2 + 100, 100,
                              window_height // 2 - 100))
            pygame.draw.rect(screen, (255, 255, 255),
                             (0, 0, window_width, window_height // 6))
            pygame.draw.rect(screen, (0, 0, 0),
                             (0, 0, window_width, window_height // 6), 5)
            pygame.draw.rect(screen, (0, 0, 0),
                             (0, 0, window_width, window_height), 10)
            pygame.draw.circle(screen, (139, 0, 0),
                               ant_colony.queen.position, 10)
            # --------------------------------------------- bouton stop
            # -------------------------------------------------
            pygame.draw.rect(screen, stop_button_color, stop_button_rect)
            stop_button_text = font.render("STOP", True, (255, 255, 255))
            screen.blit(stop_button_text, (10, 10))
            if not running:
                pygame.draw.rect(screen, (0, 0, 0), stop_button_rect, 5)
            # --------------------------------------------- button pause
            # -------------------------------------------------
            pygame.draw.rect(screen, (0, 0, 255) if not paused else (255, 0, 0),
                             pause_button_rect)  # Toggle color based on paused state
            pause_button_text = font.render("Pause" if not paused else "Resume",
                                            True, (255, 255, 255))
            screen.blit(pause_button_text, (20, 55))
            for x, y in digging_list:
                pygame.draw.rect(screen, (255, 255, 255),
                                 (x - 10, y - 10, 20, 20))
            # --------------------------------------------- slider
            # -------------------------------------------------
            draw_slider(screen, (window_width // 2 - 100,
                                 window_height // 6 - 50), 200, 20, simulation_speed)
            # --------------------------------------------- Légende
            # ------------------------------------------------------
            pygame.draw.circle(screen, (139, 0, 0),
                               [window_width - 140, 50], 10)
            pygame.draw.circle(screen, (165, 42, 42),
                               [window_width - 140, 75], 10)
            pygame.draw.circle(screen, (255, 105, 180),
                               [window_width - 140, 100], 10)
            pygame.draw.circle(screen, (0, 0, 0),
                               [window_width - 140, 125], 10)
            pygame.draw.circle(screen, (255, 255, 0), [window_width - 140, 150], 10)
            pygame.draw.circle(screen, (0, 0, 255), [window_width - 140, 175], 10)
            text_reine = font.render("= Reine", True, (0, 0, 0))
            screen.blit(text_reine, (window_width - 120, 35))
            text_male = font.render("= Mâle", True, (0, 0, 0))
            screen.blit(text_male, (window_width - 120, 60))
            text_nurse = font.render("= Nourrice", True, (0, 0, 0))
            screen.blit(text_nurse, (window_width - 120, 85))
            text_slaver = font.render("= Esclavagiste", True, (0, 0, 0))
            screen.blit(text_slaver, (window_width - 120, 110))
            text_slave = font.render("= Esclave", True, (0, 0, 0))
            screen.blit(text_slave, (window_width - 120, 135))
            text_soldier = font.render("= Soldat", True, (0, 0, 0))
            screen.blit(text_soldier, (window_width - 120, 160))
            # ---------------------------------------------- Larves
            # --------------------------------------------------------
            new_larva = ant_colony.queen.lay_eggs()
            if new_larva:
                collides = False
                new_larva_rect = pygame.Rect(new_larva.position[0], new_larva.position[1], 20, 20)
                for larva in ant_colony.larvae:
                    existing_larva_rect = pygame.Rect(larva.position[0], larva.position[1], 20, 20)
                    if existing_larva_rect.colliderect(new_larva_rect):
                        collides = True
                        break
                # Si aucune collision n'a été trouvée, ajouter la nouvelle larve à la colonie
                if not collides:
                    new_larva.position = (
                        random.randint(window_width // 2 - 50, window_width // 2 + 50),
                        random.randint(window_height // 2 + 10, window_height // 2 + 80)
                    )
                    ant_colony.add_larva(new_larva)

            larvae_to_remove = []
            # Dessiner toutes les larves de la colonie sur l'écran
            for larva in ant_colony.larvae:
                pygame.draw.circle(screen, (0, 0, 0), larva.position, 3)
                larva.ajout_age()
                if larva.age >= larva.time_to_hatch:
                    larvae_to_remove.append(larva)
                    new_ant = hatch()
                    new_ant.id = larva.id
                    ant_key = new_ant.id
                    ant_colony.dicAnt[ant_key] = (new_ant, larva.position[0],
                                                  larva.position[1], 0, 0)
            for larva in larvae_to_remove:
                ant_colony.larvae.remove(larva)
            # ---------------------------------------------- Fourmis
            # ------------------------------------------------
            ants_to_remove = []
            for ant_key, (ant, x, y, count, move) in ant_colony.dicAnt.items():
                ant.age += 1
                if ant.age >= 1000:
                    ant.status_dead = True
                if not ant.status_dead:
                    if ant.ant_type == "Male":
                        new_x, new_y, count, move = male_move(x, y, count, move,
                                                              window_width, window_height)
                        male_action()
                        move, count = male_check_color_and_adjust(new_x, new_y, move,
                                                                  count, window_width,
                                                                  window_height, screen)

                        ant_colony.dicAnt[ant_key] = (ant, new_x, new_y, count, move)
                        pygame.draw.circle(screen, (165, 42, 42),
                                           (int(new_x), int(new_y)), 6)
                    elif ant.ant_type == "Nurse":
                        pygame.draw.circle(screen, (255, 105, 180), (x, y), 6)
                    elif ant.ant_type == "Slaver":
                        pygame.draw.circle(screen, (0, 0, 0), (x, y), 6)
                    elif ant.ant_type == "Slave":
                        pygame.draw.circle(screen, (255, 255, 0), (x, y), 6)
                    if ant.ant_type == "Soldier":
                        new_x, new_y, count, move = soldier_move(x, y, count,move,
                                                                 window_width, window_height)
                        soldier_action()

                        move, count, last_dig_direction = soldier_check_color_and_adjust(new_x, new_y, move, count,
                                                                     screen, noise_map, digging_list, last_dig_direction)

                        ant_colony.dicAnt[ant_key] = (ant, new_x, new_y, count, move)
                        pygame.draw.circle(screen, (0, 0, 255),
                                           (int(new_x), int(new_y)), 8)
                else:
                    # Supprimer la fourmi de la colonie si elle est morte
                    ants_to_remove.append(ant_key)
            for ant_key in ants_to_remove:
                del ant_colony.dicAnt[ant_key]

            pygame.display.flip()
            clock.tick(500 * simulation_speed)  # Limite le nombre d'images par seconde

    pygame.quit()
