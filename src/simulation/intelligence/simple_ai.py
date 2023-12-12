import random
import math

def move(x, y, count, move, window_width, window_height):
    """
    Fonction de mouvement pour les fourmis mâles.

    PRE:
    - x et y sont les coordonnées actuelles de la fourmi.
    - count est un entier représentant le compteur de mouvement.
    - move est un flottant représentant la direction actuelle de la fourmi.
    - window_width et window_height sont les dimensions de la fenêtre de simulation.

    POST:
    - Retourne les nouvelles coordonnées, le nouveau compteur de mouvement et la nouvelle direction.
    - La logique de mouvement spécifique aux mâles est gérée dans cette fonction.
    - Les nouvelles coordonnées sont calculées en fonction de la direction actuelle et du compteur de mouvement.
    - Si la fourmi atteint les bords de la fenêtre, elle change de direction de manière aléatoire.
    MAX
    """
    # Logique de mouvement pour les mâles
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

    if not (30 <= new_x <= window_width-30 and window_height/6+30 <= new_y <= window_height-30):
        # Inverser la direction en ajoutant ou soustrayant π (pi)
        angle += math.pi
        # Recalculer les nouvelles coordonnées avec la direction inversée
        new_x = x + distance * math.cos(angle)
        new_y = y + distance * math.sin(angle)

    return new_x, new_y, count, move
def action():
    """
    Fonction d'action pour les fourmis mâles.

    POST:
    - La logique d'action spécifique aux mâles est gérée dans cette fonction.
    - Pour les fourmis mâles, il peut s'agir de interactions spécifiques ou de comportements particuliers.
    - Cette fonction peut être appelée à chaque itération de la simulation pour mettre à jour l'état des fourmis mâles.
    FLO
    """
    pass
def check_color_and_adjust(x, y, move, count, window_width, window_heigth, screen):
    """
    Fonction pour vérifier la couleur sous la fourmi et ajuster le mouvement en conséquence.

    PRE:
    - new_x et new_y sont les nouvelles coordonnées de la fourmi.
    - angle est un flottant représentant la direction actuelle de la fourmi.
    - distance est un flottant représentant la distance à parcourir.
    - window est la surface de la fenêtre de simulation.
    - digging_list est une liste contenant les coordonnées des zones de creusage.

    POST:
    - Vérifie la couleur sous la fourmi sur la surface de la fenêtre.
    - Si la couleur correspond à une zone de creusage, ajuste le mouvement en conséquence.
    - Si la couleur est différente, la fourmi continue dans la direction actuelle.
    - Les nouvelles coordonnées et le nouvel angle sont renvoyés après ajustement.
    SEB
    """
    color_under_ant = screen.get_at((int(x + 6), int(y + 6)))
    if color_under_ant == (34, 139, 34):
        move = move - math.pi  # Inverser la direction si la couleur sous la fourmi est verte
        count = random.randint(7, 12)
    return move, count
