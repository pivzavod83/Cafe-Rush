# shop.py — end-of-day upgrades: spend money to unlock new ingredients
# everything here is permanent; new ingredients make orders harder but more varied

from ingredients import get_by_id, unlockable


def upgrades_for_sale(unlocked_ids):
    """List of (ingredient_id, name, cost) that the player doesn't own yet."""
    unlocked_set = set(unlocked_ids)
    return [
        (ing["id"], ing["name"], ing["unlock_cost"])
        for ing in unlockable()
        if ing["id"] not in unlocked_set
    ]


def buy(unlocked_ids, ingredient_id, money):
    """
    If we can afford it and don't already have it, return (new_unlocked_list, money_left).
    Otherwise return None.
    """
    ing = get_by_id(ingredient_id)
    if not ing or ing["unlock_cost"] == 0:
        return None
    if ingredient_id in unlocked_ids:
        return None
    if money < ing["unlock_cost"]:
        return None
    new_unlocked = list(unlocked_ids) + [ingredient_id]
    new_unlocked.sort()
    return (new_unlocked, money - ing["unlock_cost"])
