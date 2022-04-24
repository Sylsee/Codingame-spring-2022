import sys
from math import hypot


""" DEFINE """

ROUND = 0
ROUND_ATTACK = 130

MAP_X_LIMIT = 17630
MAP_Y_LIMIT = 9000

BASE_RADIUS = 5000

MONSTER_SPEED = 400
HERO_DAMAGE = 2

SPELL_COST = 10

PLAYER_VISIBILITY = 2200
BASE_VISIBILITY = 6000

TYPE_MONSTER = 0
TYPE_MY_HERO = 1
TYPE_OP_HERO = 2

TARGET_POS_ONE = 0
TARGET_POS_TWO = 0

HERO_CONTROLED = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)

# The generic monster class
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

    def nextLocation(self) -> Point:
        return Point(self.x + self.vx, self.y + self.vy)

""" ACTIONS """

# Move to x, y direction (800 per round per hero)
def move(x: int, y: int):
    print(f'MOVE {x} {y} move')

# Throw wind spell (1280 range and push 2200 in zone)
def wind(x: int, y: int):
    global gmana
    gmana -= SPELL_COST
    print(f'SPELL WIND {x} {y} wind')

# Throw control spell (one movement to this pos (800 for hero and 400 for monsters))
def control(entity: Monster, x: int, y: int):
    global gmana
    gmana -= SPELL_COST
    entity.is_controlled = True
    print(f'SPELL CONTROL {entity._id} {x} {y} control')

# Throw shield spell (the entity isn't affected by spells for 12 rounds)
def shield(entity):
    global gmana
    gmana -= SPELL_COST
    entity.shield_life = 12
    print(f'SPELL SHIELD {entity._id} shield')

# Returns true if the target probably reach the base with 1 hero on him
# else returns false
def canReachBase(target, base) -> bool:
    return distance(target, base) / MONSTER_SPEED > target.health / HERO_DAMAGE

# Get the distance between two targets
def distance(target1, target2) -> float:
    return hypot(target1.x - target2.x, target1.y - target2.y)

""" CLASSES """

# Generic hero class
class Hero:
    def __init__(self, id, x, y, shield_life, is_controlled):
        self._id = id
        self.id = (id if id < 3 else id - 3)
        self.x = x
        self.y = y
        self.shield_life = shield_life
        self.is_controlled = is_controlled

    def __str__(self):
        return 'id:[{}] x[{}] y[{}] shield_life[{}] is_controlled[{}]'.format(
            self.id, self.x, self.y, self.shield_life, self.is_controlled
        )

# The hero who defend our base
class Defender(Hero):

    used_spell = False
    positions = [[], [], []]
    target_pos = 0

    def __init__(self, id, x, y, shield_life, is_controlled):
        super().__init__(id, x, y, shield_life, is_controlled)
        if is_controlled != 0:
            global HERO_CONTROLED
            HERO_CONTROLED = True
        if self.id == 1:
            global TARGET_POS_ONE
            self.target_pos = TARGET_POS_ONE
            self.positions = [[4700, 4000], [1900, 5300], [5900, 5900]] if base_x == 0 else [[0,0],[0,0],[0,0]]
        else:
            global TARGET_POS_TWO
            self.target_pos = TARGET_POS_ONE
            self.positions = [[5500, 2400], [7600, 420], [7900, 3300]] if base_x == 0 else [[0,0],[0,0],[0,0]]

    def routine(self, monsters, targets = None):
        if monsters and targets == None:
            targets = self.choose_target_near_base(monsters)

        if targets:
            target = targets[0]

            if distance(self, my_base) > 8500:
                self.patrol(0 if ROUND < 30 else 0)

            if my_mana > 9 and targets[0][2].shield_life == 0 : #and Defender.used_spell == False:
                if target[1] < 2200 and distance(target[2], self) <= 1280:
                    wind(op_base.x, op_base.y)
                    Defender.used_spell = True
                elif 4599 < target[1] < 5200 and distance(target[2], self) <= 2200 and (target[2].is_controlled == 0 or target[2].threat_for == 1):
                    control(target[2], op_base.x, op_base.y)
                    Defender.used_spell = True
                else:
                    move(target[2].x, target[2].y)
            else:
                Defender.used_spell = False
                move(target[2].x, target[2].y)
        else:
            targets = self.choose_target_near_self(monsters)
            if targets:
                target = targets[0]
                #if hypot(target[2].x - self.positions[TARGET_POS_ONE if self.id == 1 else TARGET_POS_TWO][0], target[2].y - self.positions[TARGET_POS_ONE if self.id == 1 else TARGET_POS_TWO][1]) > 500:
                #    self.patrol(1 if ROUND < 30 else 1)
                #if hypot(self.positions[TARGET_POS_ONE if self.id == 1 else TARGET_POS_TWO][0] - target[2].x, target[2].y - self.positions[TARGET_POS_ONE if self.id == 1 else TARGET_POS_TWO][1]) > 1000:
                #  self.patrol(1 if ROUND < 30 else 1)
                #if my_mana > 9 and target[1] < 2200 and target[2].is_controlled == 0 and (target[2].is_controlled == 0 or target[2].threat_for == 1):
                #   control(target[2].id, op_base_x, op_base_y)
                #else:
                move(target[2].x, target[2].y)
            else:
                if my_mana > 9 and self.shield_life == 0:
                    self.patrol(2 if ROUND < 30 else 1)
#                   shield(self)
                else:
                    self.patrol(2 if ROUND < 30 else 1)
        return targets

    def choose_target_near_self(self, monsters):
        monsters_ranked = []
        for monster in monsters:
            if hypot(self.x - monster.x, self.y - monster.y) < 3000 and hypot(base_x - monster.x, base_y - monster.y) < 8000:
                dist = hypot(self.x - monster.x, self.y - monster.y)
                threat_level = 500 * (1 / (dist + 1))
                monsters_ranked.append((threat_level, dist, monster))
        monsters_ranked.sort(reverse=True)
        return monsters_ranked

    def choose_target_near_base(self, monsters):
        monsters_ranked = []
        for monster in monsters:
            if hypot(base_x - monster.x, base_y - monster.y) < 6000:
                threat_level = 0
                if monster.near_base == 1 and monster.threat_for == 1:
                    threat_level = 1000
                elif monster.threat_for == 1:
                    threat_level = 500
                dist = hypot(base_x - monster.x, base_y - monster.y)
                threat_level += 500 * (1 / (dist + 1))
                monsters_ranked.append((threat_level, dist, monster))
        monsters_ranked.sort(reverse=True)
        return monsters_ranked


    def patrol(self, limits):
        global defender_current_pos
        current = defender_pos[ROUND > ROUND_ATTACK][defender_current_pos]
        if distance(self, current) < 800:
            defender_current_pos += 1
            if defender_current_pos >= defender_max_pos[ROUND > ROUND_ATTACK]:
                defender_current_pos = 0
        if my_base.x == 0:
            move(current.x, current.y)
        else:
            move(MAP_X_LIMIT - current.x, MAP_Y_LIMIT - current.y)


defender_current_pos = 0
defender_pos = [
                {
                    0: Point(4700, 4000),
                    1: Point(1900, 5300),
                    2: Point(5900, 5900),
                },
                {
                    0: Point(0, 0),
                    1: Point(0, 0),
                    2: Point(0, 0),
                },
               ]
defender_max_pos = []
for i in defender_pos:
    defender_max_pos.append(len(i))


# The hero who attack the ennemy base
class Attacker(Hero):
    def __init__(self, id, x, y, shield_life, is_controlled):
        super().__init__(id, x, y, shield_life, is_controlled)
        if is_controlled != 0:
            global HERO_CONTROLED
            HERO_CONTROLED = True

    def routine(self, monsters):
        if ROUND < ROUND_ATTACK or gmana < 40:
            self.farming(monsters)
        else:
            self.attacking(monsters)

    # FARM
    def farming(self, monsters):
        targets = None
        if monsters:
            targets = self.choose_target(monsters)
        if targets:
            target = targets[0][1]
            move(target.x, target.y)
        else:
            self.wait()

    # ATTACK
    def attacking(self, monsters):
        targets = None
        if monsters:
            targets = self.choose_target(monsters)

        if targets:
            target = targets[0][1]
            canReachBase(target, op_base)
            dist = distance(target, self)

            if dist > 2200:
                self.move(target.x, target.y)
            elif target.shield_life == 0:
                self.useSpell(target, dist)
            else:
                self.wait()

        else:
            self.wait()

    def dontTouch(self, target: Monster):
        if distance(self, target.nextLocation()) < 800:
            move(target.x, target.y)
        else:
            move(target.x, target.y)

    def useSpell(self, target, dist: float):
        if target.near_base == 1 and target.threat_for == 2 and canReachBase(target, op_base):
            shield(target)
        elif target.near_base == 0 and target.threat_for != 2:
            control(target, op_base.x, op_base.y)
        elif dist < 1280:
            wind(op_base.x, op_base.y)
        else:
            self.wait()

    def choose_target(self, monsters):
        spiders_ranked = []
        for monster in monsters:
            # FARMING
            if ROUND < ROUND_ATTACK:
                if distance(monster.nextLocation(), op_base) < 12000:
                    dist = distance(self, monster.nextLocation())
                    spiders_ranked.append((dist, monster))
            # ATTACK
            else:
                dist = distance(monster.nextLocation(), op_base)
                if dist < 6000:
                    spiders_ranked.append((dist, monster))

        spiders_ranked.sort(reverse=True)

        return spiders_ranked


    def wait(self):
        global attacker_current_pos
        current = attacker_pos[ROUND > ROUND_ATTACK][attacker_current_pos]
        if distance(self, current) < 800:
            attacker_current_pos += 1
            if attacker_current_pos >= attacker_max_pos[ROUND > ROUND_ATTACK]:
                attacker_current_pos = 0
        print(f'current {current.x} {current.y}', file=sys.stderr, flush=True)
        if my_base.x == 0:
            move(current.x, current.y)
        else:
            move(MAP_X_LIMIT - current.x, MAP_Y_LIMIT - current.y)


attacker_current_pos = 0
attacker_pos = [
                {
                    0: Point(15000, 2000),
                    1: Point(11000, 3500),
                    2: Point(10000, 7000),
                    3: Point(14000, 5500),
                },
                {
                    0: Point(16000, 4300),
                    1: Point(14000, 5500),
                    2: Point(13000, 7500),
                    3: Point(16000, 7500)
                },
               ]
attacker_max_pos = []
for i in attacker_pos:
    attacker_max_pos.append(len(i))


""" MAIN LOOP """

# base_x,base_y: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
my_base = Point(base_x, base_y)
heroes_per_player = int(input())

op_base = Point(MAP_X_LIMIT if base_x == 0 else 0, MAP_Y_LIMIT if base_y == 0 else 0)

gmana = 0

# game loop
while True:
    my_health, my_mana = [int(j) for j in input().split()]
    gmana = my_mana
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
    targets = my_heroes[1].routine(monsters)
    my_heroes[2].routine(monsters, targets)

    ROUND += 1

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