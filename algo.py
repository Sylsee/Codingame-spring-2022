import sys
from math import hypot

MAP_X_LIMIT = 17630
MAP_Y_LIMIT = 9000

BASE_RADIUS = 5000

PLAYER_VISIBILITY = 2200
BASE_VISIBILITY = 6000

TYPE_MONSTER = 0
TYPE_MY_HERO = 1
TYPE_OP_HERO = 2

def wind(x: int, y: int):
    print(f'SPELL WIND {x} {y}')


def control(entityId: int, x: int, y: int):
    print(f'SPELL CONTROL {entityId} {x} {y}')


def shield(entity):
    print(f'SPELL SHIELD {entity._id}')


class Hero:
    def __init__(self, id, x, y, shield_life, is_controlled):
        self._id = id
        self.id = (id if id <= 2 else id - 3)
        self.x = x
        self.y = y
        self.shield_life = shield_life
        self.is_controlled = is_controlled

    def __str__(self):
        return 'id:[{}] x[{}] y[{}] shield_life[{}] is_controlled[{}]'.format(
            self.id, self.x, self.y, self.shield_life, self.is_controlled
        )


class Defender(Hero):
    def routine(self, monsters):
        targets = None
        if monsters:
            targets = self.choose_target(monsters)

        if targets:
            if hypot(base_x - self.x, base_y - self.y) > 8500:
                wait_pos(self.id)

            elif my_mana > 9 and targets[0][2].shield_life == 0:
                if targets[0][1] < 2200 and distHeroMonster(targets[0][2], self) <= 1280:
                    print(f'SPELL WIND {op_base_x} {op_base_y}')
                elif 4599 < targets[0][1] < 5200 and distHeroMonster(targets[0][2], self) <= 2200:
                    print(f'SPELL CONTROL {targets[0][2].id} {op_base_x} {op_base_y}')
                else:
                    print(f'MOVE {targets[0][2].x} {targets[0][2].y}')
    
            else:
                print(f'MOVE {targets[0][2].x} {targets[0][2].y}')

        else:
            wait_pos(self.id)


    def choose_target(self, monsters):
        spiders_ranked = []
        for monster in monsters:
            threat_level = 0
            if monster.near_base == 1 and monster.threat_for == 1:
                threat_level = 1000
            elif monster.threat_for == 1:
                threat_level = 500
    
            dist = hypot(base_x - monster.x, base_y - monster.y)
            threat_level += 500 * (1 / (dist + 1))
            spiders_ranked.append((threat_level, dist, monster))
    
        spiders_ranked.sort(reverse=True)
    
        return spiders_ranked


    def wait_pos(self):
        pass


class Attacker(Hero):
    def routine(self, monsters):
        targets = None
        if monsters:
            targets = self.choose_target(monsters)
        if targets:
            if hypot(base_x - self.x, base_y - self.y) > 8500:
                wait_pos(self.id)
            elif my_mana > 9 and targets[0][2].shield_life == 0:
                if targets[0][1] < 2200 and distHeroMonster(targets[0][2], self) <= 1280:
                    print(f'SPELL WIND {op_base_x} {op_base_y}')
                elif 4599 < targets[0][1] < 5200 and distHeroMonster(targets[0][2], self) <= 2200:
                    print(f'SPELL CONTROL {targets[0][2].id} {op_base_x} {op_base_y}')
                else:
                    print(f'MOVE {targets[0][2].x} {targets[0][2].y}')
            else:
                print(f'MOVE {targets[0][2].x} {targets[0][2].y}')
        else:
            self.wait_pos()


    def choose_target(self, monsters):
        spiders_ranked = []
        for monster in monsters:
            dist = hypot(self.x - monster.x, self.y - monster.y)
            threat_level = 500 * (1 / (dist + 1))
            spiders_ranked.append((threat_level, dist, monster))
    
        spiders_ranked.sort(reverse=True)
    
        return spiders_ranked


    def wait_pos(self):
        if base_x == 0:
            print(f'WAIT ')
        else:
            print(f'WAIT ')

class Monster:
    def __init__(self, id, x, y, vx, vy, health, shield_life, is_controlled, near_base, threat_for):
        self._id = id
        self.id = id
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.health = health
        self.shield_life = shield_life
        self.is_controlled = is_controlled
        self.near_base = near_base
        self.threat_for = threat_for

    def __str__(self):
        return 'id:[{}] x[{}] y[{}] vx[{}] vy[{}] health[{}] shield_life[{}] is_controlled[{}] near_base[{}] threat_for[{}]'.format(
            self.id, self.x, self.y, self.vx, self.vy, self.health, self.shield_life, self.is_controlled, self.near_base, self.threat_for
        )


def wait_pos(id : int):
    if base_x == 0:
        if id == 0:
            print('MOVE 5800 450')
        elif id == 1:
            print('MOVE 4100 3500')
        elif id == 2:
            print('MOVE 450 5800')
    else:
        if id ==  0:
            print('MOVE 16000 3300')
        elif id == 1:
            print('MOVE 12300 7800')
        elif id == 2:
            print('MOVE 13800 5000')


def distHeroMonster(monster: Monster, hero: Hero) -> float:
    return hypot(monster.x - hero.x, monster.y - hero.y)


# def intersecMonster(monster: Monster, hero: Hero):
    




""" MAIN LOOP """


# base_x,base_y: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
heroes_per_player = int(input())

op_base_x = MAP_X_LIMIT if base_x == 0 else 0
op_base_y = MAP_Y_LIMIT if base_y == 0 else 0


# game loop
while True:
    my_health, my_mana = [int(j) for j in input().split()]
    enemy_health, enemy_mana = [int(j) for j in input().split()]
    entity_count = int(input())  # Amount of heros and monsters you can see

    monsters = []
    my_heroes = []
    enemy_heroes = []

    nb_hero = 0
    for i in range(entity_count):
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
        # _id: Unique identifier
        # _type: 0=monster, 1=your hero, 2=opponent hero
        # x,y: Position of this entity
        # shield_life: Ignore for this league; Count down until shield spell fades
        # is_controlled: Ignore for this league; Equals 1 when this entity is under a control spell
        # health: Remaining health of this monster
        # vx,vy: Trajectory of this monster
        # near_base: 0=monster with no target yet, 1=monster targeting a base
        # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither

        if _type == TYPE_MONSTER:
            monsters.append(Monster(_id, x, y, vx, vy, health, shield_life, is_controlled, near_base, threat_for))
        elif _type == TYPE_MY_HERO:
            if nb_hero == 0:
                my_heroes.append(Attacker(_id, x, y, shield_life, is_controlled))
            else:
                my_heroes.append(Defender(_id, x, y, shield_life, is_controlled))
            nb_hero += 1
        elif _type == TYPE_OP_HERO:
            enemy_heroes.append(Hero(_id, x, y, shield_life, is_controlled))

    my_heroes[0].routine(monsters)
    my_heroes[1].routine(monsters)
    my_heroes[2].routine(monsters)

# To debug: print("Debug messages...", file=sys.stderr, flush=True)

# In the first league: MOVE <x> <y> | WAIT; In later leagues: | SPELL <spellParams>;

"""
    - definir une position initiale
    - faire un systeme de comptage des ennemis qui risque de niquer la base
    - si c'est la merde a la base, tout le mana est reserve pour les defenseurs pour defendre
    - faire un systeme pour ne pas taper un ennemi si il parts dans une direction apres un sort control
    - intercepter un ennemi avec le chemin le plus court
    - prioriser le spell wind si plusieurs ennemis devant, en fonction de leur distance avec la base, utiliser deux spell au lieu d'un pour bien les eloigner
    - faire revenir l'attaquant vers la base si c'est la merde et si il est assez proche
    - mettre une place une ronde en arc de cercle pour l'attaquant et une position initiale
    - attaquant pousse les ennemis vers la base adverse mais il faut qu'il farme le mana aussi, donc il faut qu'il tape des araignees quand meme, a voir si il les tue, etc...
"""