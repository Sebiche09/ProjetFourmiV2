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
                               persistence=2, lacunarity=0.6, seed=random.randint(0, 100))


def handle_events(running, simulation_running, paused, simulation_speed, egg_speed, spawn_speed, stop_button_rect, pause_button_rect,
                  window_width, window_height):
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if stop_button_rect.collidepoint(event.pos):
                simulation_running = not simulation_running
            if pause_button_rect.collidepoint(event.pos):
                paused = not paused
        elif event.type == pygame.MOUSEMOTION:  # Ajout pour détecter les mouvements de la souris
            if event.buttons[0]:  # Vérifie si le bouton gauche de la souris est enfoncé
                slider_rect = pygame.Rect(window_width // 2 - 100, window_height // 6 - 50, 200, 20)
                slider_rect1 = pygame.Rect(window_width // 2 - 100, window_height // 6 - 75, 200, 20)
                slider_rect2 = pygame.Rect(window_width // 2 - 100, window_height // 6 - 100, 200, 20)
                if slider_rect.collidepoint(event.pos):
                    simulation_speed = (event.pos[0] - slider_rect.left) / slider_rect.width
                if slider_rect1.collidepoint(event.pos):
                    egg_speed = (event.pos[0] - slider_rect1.left) / slider_rect1.width
                if slider_rect2.collidepoint(event.pos):
                    spawn_speed = (event.pos[0] - slider_rect2.left) / slider_rect2.width

    return running, simulation_running, paused, simulation_speed, egg_speed, spawn_speed


def draw_initial_environment(screen, window_width, window_height, ant_colony):
    background_image = pygame.image.load("img/background.jpg").convert()
    background_image = pygame.transform.scale(background_image, (window_width, window_height))
    screen.blit(background_image, (0, 0))
    # Dessiner les éléments de l'environnement initial
    pygame.draw.rect(screen, (255, 255, 255), (window_width // 2 - 100, window_height // 2 - 100, 200, 200))
    pygame.draw.rect(screen, (255, 255, 255),
                     (window_width // 2 - 50, window_height // 2 + 100, 100, window_height // 2 - 100))
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, window_width, window_height // 6))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, window_width, window_height // 6), 5)
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, window_width, window_height), 10)
    pygame.draw.circle(screen, (139, 0, 0), ant_colony.queen.position, 10)


def draw_slider(window, position, width, height, value):
    pygame.draw.rect(window, (200, 200, 200), (position[0], position[1], width, height))
    pygame.draw.rect(window, (0, 0, 0), (position[0], position[1], width, height), 2)
    knob_position = (position[0] + int(value * width), position[1] + height // 2)
    pygame.draw.circle(window, (255, 0, 0), knob_position, 10)


def draw_legend(screen, font, window_width):
    legend_positions = [(window_width - 140, 50 + i * 25) for i in range(6)]
    legend_colors = [(139, 0, 0), (165, 42, 42), (255, 105, 180), (0, 0, 0), (255, 255, 0), (0, 0, 255)]
    ant_types = ["Reine", "Mâle", "Nourrice", "Esclavagiste", "Esclave", "Soldat"]

    for position, color, ant_type in zip(legend_positions, legend_colors, ant_types):
        pygame.draw.circle(screen, color, position, 10)
        text = font.render(f"= {ant_type}", True, (0, 0, 0))
        screen.blit(text, (window_width - 120, 35 + 25 * ant_types.index(ant_type)))


def draw_buttons(screen, font, paused, running):
    # Dessine les boutons de pause et stop
    stop_button_rect = pygame.Rect(10, 10, 100, 30)
    stop_button_color = (255, 0, 0)
    pygame.draw.rect(screen, stop_button_color, stop_button_rect)
    stop_button_text = font.render("STOP", True, (255, 255, 255))
    screen.blit(stop_button_text, (10, 10))

    pause_button_rect = pygame.Rect(10, 50, 150, 30)
    pause_button_color = (0, 0, 255) if not paused else (255, 0, 0)
    pygame.draw.rect(screen, pause_button_color, pause_button_rect)
    pause_button_text = font.render("Pause" if not paused else "Resume", True, (255, 255, 255))
    screen.blit(pause_button_text, (20, 55))


def lay_and_position_larva(ant_colony, window_width, window_height, spawn_speed):
    spawn_speed = 0.001 + (0.01 - 0.001) * spawn_speed
    ant_colony.queen.laying_rate = spawn_speed
    new_larva = ant_colony.queen.lay_eggs()
    if new_larva:
        collides = any(
            pygame.Rect(larva.position[0], larva.position[1], 20, 20).colliderect(
                pygame.Rect(new_larva.position[0], new_larva.position[1], 20, 20)
            )
            for larva in ant_colony.larvae
        )

        if not collides:
            new_larva.position = (
                random.randint(window_width // 2 - 50, window_width // 2 + 50),
                random.randint(window_height // 2 + 10, window_height // 2 + 80)
            )
            ant_colony.add_larva(new_larva)


def draw_larvae(screen, ant_colony, egg_speed):
    larvae_to_remove = []

    for larva in ant_colony.larvae:
        pygame.draw.circle(screen, (0, 0, 0), larva.position, 3)
        larva.time_to_hatch = 1 + (1000 - 1) * egg_speed
        larva.ajout_age()

        if larva.age >= larva.time_to_hatch:
            larvae_to_remove.append(larva)
            new_ant = hatch()
            new_ant.id = larva.id
            ant_key = new_ant.id
            ant_colony.dicAnt[ant_key] = (new_ant, larva.position[0], larva.position[1], 0, 0)

    for larva in larvae_to_remove:
        ant_colony.larvae.remove(larva)


def draw_male_ants(screen, ant_colony, window_width, window_height):
    ants_to_remove = []

    for ant_key, (ant, x, y, count, move) in ant_colony.dicAnt.items():
        ant.age += 1

        if ant.age >= 2000:
            ant.status_dead = True

        if not ant.status_dead and ant.ant_type == "Male":
            new_x, new_y, count, move = male_move(x, y, count, move, window_width, window_height)
            male_action()
            move, count = male_check_color_and_adjust(new_x, new_y, move, count, window_width, window_height, screen)

            ant_colony.dicAnt[ant_key] = (ant, new_x, new_y, count, move)
            pygame.draw.circle(screen, (165, 42, 42), (int(new_x), int(new_y)), 6)

        elif ant.status_dead and ant.ant_type == "Male":
            # Supprimer la fourmi de la colonie si elle est morte ou n'est pas un mâle
            ants_to_remove.append(ant_key)

    for ant_key in ants_to_remove:
        del ant_colony.dicAnt[ant_key]


def draw_ants(screen, ant_colony, ant_type, color):
    ants_to_remove = []

    for ant_key, (ant, x, y, _, _) in ant_colony.dicAnt.items():
        if ant.ant_type == ant_type and not ant.status_dead:
            pygame.draw.circle(screen, color, (int(x), int(y)), 6)
        elif ant.status_dead and ant.ant_type == ant_type:
            ants_to_remove.append(ant_key)

    for ant_key in ants_to_remove:
        del ant_colony.dicAnt[ant_key]


def draw_nurse_ants(screen, ant_colony):
    draw_ants(screen, ant_colony, "Nurse", (255, 105, 180))


def draw_slaver_ants(screen, ant_colony):
    draw_ants(screen, ant_colony, "Slaver", (0, 0, 0))


def draw_slave_ants(screen, ant_colony):
    draw_ants(screen, ant_colony, "Slave", (255, 255, 0))


def draw_soldier_ants(screen, ant_colony, window_width, window_height, last_dig_direction, digging_list):
    ants_to_remove = []
    for ant_key, (ant, x, y, count, move) in ant_colony.dicAnt.items():
        ant.age += 1
        if ant.age >= 2000:
            ant.status_dead = True
        if not ant.status_dead and ant.ant_type == "Soldier":
            new_x, new_y, count, move = soldier_move(x, y, count, move,
                                                     window_width, window_height)
            soldier_action()

            move, count, last_dig_direction = soldier_check_color_and_adjust(new_x, new_y, move, count,
                                                                             screen, noise_map,
                                                                             digging_list,
                                                                             last_dig_direction)

            ant_colony.dicAnt[ant_key] = (ant, new_x, new_y, count, move)
            pygame.draw.circle(screen, (0, 0, 255),
                               (int(new_x), int(new_y)), 8)
        elif ant.status_dead and ant.ant_type == "Soldier":
            ants_to_remove.append(ant_key)

    for ant_key in ants_to_remove:
        del ant_colony.dicAnt[ant_key]
    return digging_list


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

    plt.imshow(noise_map, cmap='viridis', interpolation='nearest')
    plt.colorbar()
    plt.show()
    pygame.init()
    # --------------------------------------------- Infos screen ------------------------------------------------------
    screen_info = pygame.display.Info()
    window_width, window_height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((window_width, window_height))
    # --------------------------------------------- Variables globales -----------------------------------------
    pygame.display.set_caption("Simulation de Colonie de Fourmis")

    ant_colony.queen.position = (window_width // 2, window_height // 2)
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    stop_button_rect = pygame.Rect(10, 10, 100, 30)
    pause_button_rect = pygame.Rect(10, 50, 150, 30)

    clock = pygame.time.Clock()

    digging_list = []
    running = True
    simulation_running = True
    paused = False
    simulation_speed = 1
    egg_speed = 1
    spawn_speed = 1
    last_dig_direction = 0
    # ------------------------------------- Début simulation ------------------------------------
    while running and simulation_running:
        running, simulation_running, paused, simulation_speed, egg_speed, spawn_speed = handle_events(
            running, simulation_running, paused, simulation_speed, egg_speed, spawn_speed,
            stop_button_rect, pause_button_rect, window_width, window_height)
        if not paused:
            draw_initial_environment(screen, window_width, window_height, ant_colony)
            draw_buttons(screen, font, paused, running)
            draw_slider(screen, (window_width // 2 - 100, window_height // 6 - 50),
                        200, 20, simulation_speed)
            draw_slider(screen, (window_width // 2 - 100, window_height // 6 - 75),
                        200, 20, egg_speed)
            draw_slider(screen, (window_width // 2 - 100, window_height // 6 - 100),
                        200, 20, spawn_speed)

            draw_legend(screen, font, window_width)

            for x, y in digging_list:
                pygame.draw.rect(screen, (255, 255, 255),
                                 (x - 10, y - 10, 20, 20))
            lay_and_position_larva(ant_colony, window_width, window_height, spawn_speed)
            draw_larvae(screen, ant_colony, egg_speed)
            draw_male_ants(screen, ant_colony, window_width, window_height)
            draw_nurse_ants(screen, ant_colony)
            draw_slaver_ants(screen, ant_colony)
            draw_slave_ants(screen, ant_colony)
            digging_list = draw_soldier_ants(screen, ant_colony, window_width, window_height, last_dig_direction,
                                             digging_list)

            pygame.display.flip()
            clock.tick(100 * simulation_speed)  # Limite le nombre d'images par seconde
    pygame.quit()
