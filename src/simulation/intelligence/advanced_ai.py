import math
import random
global angle, distance

def move(x, y, count, move, window_width, window_height):
    """
    Logique de mouvement pour les fourmis soldats.

    PRE:
    - x et y sont les coordonnées actuelles de la fourmi.
    - count est un entier représentant le compteur de mouvement.
    - move est un flottant représentant la direction du mouvement.
    - window_width est la largeur de la fenêtre de simulation.
    - window_height est la hauteur de la fenêtre de simulation.

    POST:
    - Effectue le mouvement de la fourmi soldat en fonction de la logique définie.
    - Les nouvelles coordonnées, le nouveau compteur de mouvement et la nouvelle
    direction sont renvoyés.
    FLO
    """
    # Choisir un mouvement aléatoire
    global angle, distance
    if count == 0:
        random_move = random.randint(0, 3)
        if random_move == 0:
            angle = 0  # vers la droite
        elif random_move == 1:
            angle = math.pi / 2  # vers le haut
        elif random_move == 2:
            angle = math.pi  # vers la gauche
        elif random_move == 3:
            angle = 3 * math.pi / 2  # vers le bas
        distance = 1
        move = angle
        count = random.randint(50, 60)

    if count != 0:
        angle = move
        distance = 1
        count -= 1

    # Calculer les nouvelles coordonnées en fonction de la direction
    new_x = x + distance * math.cos(angle)
    new_y = y + distance * math.sin(angle)

    if not (30 <= new_x <= window_width -
            30 and window_height / 6 + 30 <= new_y <= window_height - 30):
        # Inverser la direction en ajoutant ou soustrayant π (pi)
        angle += math.pi
        # Recalculer les nouvelles coordonnées avec la direction inversée
        new_x = x + distance * math.cos(angle)
        new_y = y + distance * math.sin(angle)

    return new_x, new_y, count, move


def action():
    """
    Logique d'action pour les fourmis soldats.

    POST:
    - Gère la logique d'action spécifique aux soldats.
    - Cela peut inclure des comportements offensifs, défensifs ou d'autres interactions.
    - Cette fonction peut être appelée à chaque itération de la simulation
    pour mettre à jour l'état des soldats.
    MAX
    """
    pass


def check_color_and_adjust(x, y, move, count, screen, noise_map, digging_list, last_dig_direction):
    """
    Fonction pour vérifier la couleur sous la fourmi et ajuster le mouvement en conséquence.

    PRE:
    - new_x et new_y sont les nouvelles coordonnées de la fourmi.
    - angle est un flottant représentant la direction actuelle de la fourmi.
    - distance est un flottant représentant la distance à parcourir.
    - window est la surface de la fenêtre de simulation.
    - digging_list est une liste contenant les coordonnées des zones de creusage.
    - last_dig_direction est la direction dans laquelle la fourmi a creusé récemment.

    POST:
    - Vérifie la couleur sous la fourmi sur la surface de la fenêtre.
    - Si la couleur correspond à une zone de creusage, ajuste le mouvement en conséquence.
    - Si la couleur est différente, la fourmi continue dans la direction actuelle.
    - Les nouvelles coordonnées, le nouvel angle et la nouvelle direction de creusage sont renvoyés après ajustement.
    """
    color_under_ant = screen.get_at((int(x + 8), int(y + 8)))

    # Utiliser la carte de bruit pour déterminer si la fourmi doit creuser
    noise_value = noise_map[int(x)][int(y)]
    digging_threshold = 0.5  # Ajustez ce seuil selon vos besoins

    # Vérifier si la fourmi est déjà dans une situation de blocage
    blocked = (int(x), int(y)) in digging_list and count == 0

    if color_under_ant == (34, 139, 34) and noise_value < digging_threshold and not blocked:
        digging_list.append((int(x), int(y)))
        # Ajustement progressif en fonction de la proximité du seuil
        adjustment_factor = min(1.0, (digging_threshold - noise_value) * 10)
        move += math.pi * adjustment_factor

        # Interpolation pour rendre le mouvement plus doux
        move = move + (math.pi - move) * adjustment_factor

        # Enregistrez la nouvelle direction de creusage
        last_dig_direction = move

        count = random.randint(7, 12)

    elif color_under_ant == (34, 139, 34) and noise_value >= digging_threshold:
        if blocked:
            # La fourmi est bloquée, elle peut choisir un nouveau mouvement aléatoire
            move = random.uniform(0, 2 * math.pi)
            last_dig_direction = None  # Réinitialiser la direction de creusage
            count = random.randint(7, 12)
        else:
            # Faire demi-tour si proche de la couleur verte
            move = move + math.pi
            count = random.randint(7, 12)

    return move, count, last_dig_direction