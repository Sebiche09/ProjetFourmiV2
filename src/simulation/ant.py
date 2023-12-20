import random

LARVA_ID_COUNT = 0


def hatch():
    ant_type = random.choice(["Male", "Nurse", "Slaver", "Slave", "Soldier"])
    return Ant(ant_type, 400, 400, 0)


class Larva:
    def __init__(self, x: float = 0, y: float = 0, id_larva=0):
        self.time_to_hatch = 7
        self.age = 0
        self.position = x, y
        self.id = id_larva

    def ajout_age(self):
        self.age += 1


class Ant:
    def __init__(self, ant_type="Male", x: float = 10, y: float = 10, id_ant=0):
        self.ant_type = ant_type
        self.id = id_ant
        self.food = 100
        self.status_dead = False
        self.position = x, y
        self.age = 0

    def hungry(self, value):
        self.food -= value

    def eat(self, value):
        self.food += value

    def dead(self):
        self.status_dead = True

    def __str__(self):
        return f"je suis une fourmi et mon id est {self.id}"


class Queen(Ant):
    def __init__(self):
        super().__init__("Queen", 10, 0, 0)
        self.__laying_rate = 0.05
        self.accepted_ants = []
        self.generated_ant_types = []

    @property
    def laying_rate(self):
        return self.__laying_rate

    @laying_rate.setter
    def laying_rate(self, new_laying_rate):
        if 0.001 < new_laying_rate <= 0.1:
            self.__laying_rate = new_laying_rate

    def lay_eggs(self):
        global LARVA_ID_COUNT
        """
        Simule la ponte d'œufs par la reine.

        PRE:
        - La reine existe.

        POST:
        - Si le nombre aléatoire généré est inférieur au taux de ponte (laying_rate),
          une nouvelle larve est créée avec un identifiant unique et renvoyée.
        - Si aucune nouvelle larve n'est créée, la méthode renvoie None.
        SEB
        """
        if random.random() < self.laying_rate:
            LARVA_ID_COUNT += 1
            return Larva(0, 0, LARVA_ID_COUNT)
        return None

    def accept_new_ant(self, ant):
        self.accepted_ants.append(ant)

    def __str__(self):
        return super().__str__() + f", je suis une reine"


class MaleAnt(Ant):
    def __init__(self):
        super().__init__("Male")
        # Add any specific attributes or methods for MaleAnt

    def __str__(self):
        return super().__str__() + f", je suis un male"


class NurseAnt(Ant):
    def __init__(self):
        super().__init__("Nurse")
        self.__nurse_augment = 0.1
        # Add any specific attributes or methods for NurseAnt

    @property
    def nurse_augment(self):
        return self.__nurse_augment

    @nurse_augment.setter
    def nurse_augment(self, new_nurse_augment):
        if 0.05 < new_nurse_augment <= 0.5:
            self.__nurse_augment = new_nurse_augment

    def __str__(self):
        return super().__str__() + f", je suis une infirmière"


class SlaverAnt(Ant):
    def __init__(self):
        super().__init__("Slaver")
        # Add any specific attributes or methods for ForagerAnt
        self.add_slave = random.randint(1, 5)
        self.__survive_rate = 0.2

    @property
    def survive_rate(self):
        return self.__survive_rate

    @survive_rate.setter
    def survive_rate(self, new_survive_rate):
        if 0.1 < new_survive_rate <= 0.5:
            self.__survive_rate = new_survive_rate

    def go_outside_slaver(self):
        pass

    def come_back_slaver(self):
        pass

    def __str__(self):
        return super().__str__() + f", je suis un esclavagiste"


class SlaveAnt(Ant):
    def __init__(self):
        super().__init__("Slave")
        # Add any specific attributes or methods for SlaveAnt
        self.revolt_rate = 0.05

    def set_revolt_rate(self, value):
        self.revolt_rate = value

    def revolt(self):
        if random.random() < self.revolt_rate:
            pass

    def __str__(self):
        return super().__str__() + f", je suis un esclave"


class SoldierAnt(Ant):
    def __init__(self):
        super().__init__("Soldier")
        # Add any specific attributes or methods for SlaveAnt
        self.defense = 0.1
        self.exit = False
        self.survive_rate = 0.4
        self.dig_speed = 0.5

    def defense_modify(self, value):
        self.defense = value

    def survive_rate_modify(self, value):
        self.survive_rate = value

    def dig_speed_modify(self, value):
        self.dig_speed = value

    def __str__(self):
        return super().__str__() + f", je suis un soldat"
