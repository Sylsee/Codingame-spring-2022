import sys
from collections import namedtuple
from math import hypot

Entity = namedtuple('Entity', [
    'id', 'type', 'x', 'y', 'shield_life', 'is_controlled', 'health', 'vx', 'vy', 'near_base', 'threat_for'
])

TYPE_MONSTER = 0
TYPE_MY_HERO = 1
TYPE_OP_HERO = 2

# base_x,base_y: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
heroes_per_player = int(input())

def wait_pos(id : int):
    if base_x == 0:
        if id == 0 or 3:
            print(f'MOVE 5800 450')
        elif id == 1 or 4:
            print(f'MOVE 4100 3500')
        elif id == 2 or 5:
            print(f'MOVE 450 5800')
    else:
        if id == 0 or 3:
            print(f'MOVE 16000 3300')
        elif id == 1 or 4:
            print(f'MOVE 12300 7800')
        elif id == 2 or 5:
            print(f'MOVE 13800 5000')


def join_target(entity1, entity2):
    monster = None
    hero = None    
    if entity1.type == TYPE_MONSTER:
        monster = entity1
        hero = entity2
    else:
        monster = entity2
        hero = entity1

    


def choose_target(monsters):
    spiders_ranked = []
    for monster in monsters:
        threat_level = 0
        if monster.near_base == 1 and monster.threat_for == 1:
            threat_level = 1000
        elif monster.threat_for == 1:
            threat_level = 500

        dist = hypot(base_x - monster.x, base_y - monster.y)
        threat_level += 500 * (1 / (dist + 1))

        spiders_ranked.append((threat_level, monster))

    spiders_ranked.sort(reverse=True)

    return spiders_ranked


# game loop
while True:
    my_health, my_mana = [int(j) for j in input().split()]
    enemy_health, enemy_mana = [int(j) for j in input().split()]
    entity_count = int(input())  # Amount of heros and monsters you can see

    monsters = []
    my_heroes = []
    enemy_heroes = []

    for i in range(entity_count):
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
        entity = Entity(
            _id,            # _id: Unique identifier
            _type,          # _type: 0=monster, 1=your hero, 2=opponent hero
            x, y,           # x,y: Position of this entity
            shield_life,    # shield_life: Ignore for this league; Count down until shield spell fades
            is_controlled,  # is_controlled: Ignore for this league; Equals 1 when this entity is under a control spell
            health,         # health: Remaining health of this monster
            vx, vy,         # vx,vy: Trajectory of this monster
            near_base,      # near_base: 0=monster with no target yet, 1=monster targeting a base
            threat_for      # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
        )

        if _type == TYPE_MONSTER:
            monsters.append(entity)
        elif _type == TYPE_MY_HERO:
            my_heroes.append(entity)
        elif _type == TYPE_OP_HERO:
            enemy_heroes.append(entity)

    for hero in my_heroes:
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)

        targets = None
        if monsters:
            targets = choose_target(monsters)

        # In the first league: MOVE <x> <y> | WAIT; In later leagues: | SPELL <spellParams>;
        if targets:
            if hypot(base_x - hero.x, base_y - hero.y) > 7500:
                wait_pos(hero.id)
            else:
                print(f'MOVE {targets[0][1].x} {targets[0][1].y}')
        else:
            wait_pos(hero.id)