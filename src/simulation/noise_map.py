import noise


def generate_noise_map(width, height, scale, octaves, persistence, lacunarity, seed):
    """
    Génère une carte de bruit en 2D.

    PRE:
    - width et height sont des entiers positifs représentant les dimensions de la carte.
    - scale est un flottant positif, octaves, persistence et lacunarity sont des entiers positifs.
    - seed est un entier, utilisé comme base pour la génération pseudo-aléatoire.

    POST:
    - Retourne une carte de bruit 2D normalisée entre 0 et 1.
    - La carte de bruit est représentée sous la forme d'une liste de listes avec les
    dimensions width x height.
    SEB
    """
    world = [[0] * height for _ in range(width)]
    for i in range(width):
        for j in range(height):
            world[i][j] = noise.pnoise2(i / scale,
                                        j / scale,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        repeatx=1024,
                                        repeaty=1024,
                                        base=seed)

    # Normalisation des valeurs pour les ramener entre 0 et 1
    min_noise = min(map(min, world))
    max_noise = max(map(max, world))
    for i in range(width):
        for j in range(height):
            world[i][j] = (world[i][j] - min_noise) / (max_noise - min_noise)

    return world
