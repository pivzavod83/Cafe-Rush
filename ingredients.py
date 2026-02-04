# ingredients.py — every ingredient the café can use
# base set is free; the rest you unlock in the shop so difficulty can ramp naturally

# each entry: id, name, color (RGB), unlock_cost (0 = you start with it)
# add more here anytime and they'll show up in the shop if cost > 0
INGREDIENT_DEFS = [
    {"id": 0, "name": "Coffee", "color": (101, 67, 33), "unlock_cost": 0},
    {"id": 1, "name": "Milk", "color": (248, 248, 255), "unlock_cost": 0},
    {"id": 2, "name": "Sugar", "color": (255, 250, 240), "unlock_cost": 0},
    {"id": 3, "name": "Espresso", "color": (40, 20, 10), "unlock_cost": 0},
    {"id": 4, "name": "Water", "color": (200, 230, 255), "unlock_cost": 0},
    # unlockables — buying these makes orders longer and trickier
    {"id": 5, "name": "Syrup", "color": (139, 69, 19), "unlock_cost": 30},
    {"id": 6, "name": "Oat Milk", "color": (210, 200, 160), "unlock_cost": 35},
    {"id": 7, "name": "Vanilla", "color": (255, 248, 220), "unlock_cost": 40},
    {"id": 8, "name": "Caramel", "color": (255, 200, 124), "unlock_cost": 45},
    {"id": 9, "name": "Cream", "color": (255, 253, 208), "unlock_cost": 50},
    {"id": 10, "name": "Chocolate", "color": (90, 55, 35), "unlock_cost": 55},
    {"id": 11, "name": "Ice", "color": (200, 230, 255), "unlock_cost": 25},
]


def get_by_id(ingredient_id):
    for ing in INGREDIENT_DEFS:
        if ing["id"] == ingredient_id:
            return ing
    return None


def get_name(ingredient_id):
    ing = get_by_id(ingredient_id)
    return ing["name"] if ing else "?"


def get_color(ingredient_id):
    ing = get_by_id(ingredient_id)
    return ing["color"] if ing else (128, 128, 128)


def base_ids():
    """Ids you have from day 1 (unlock_cost == 0)."""
    return [ing["id"] for ing in INGREDIENT_DEFS if ing["unlock_cost"] == 0]


def unlockable():
    """All ingredients that can be bought in the shop."""
    return [ing for ing in INGREDIENT_DEFS if ing["unlock_cost"] > 0]


def all_ids():
    return [ing["id"] for ing in INGREDIENT_DEFS]
