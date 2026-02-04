# order.py — drink orders, validation, and how much the customer pays
# keeps all "is this drink right?" and "how much do we earn?" logic in one place
# scoring is accuracy + order only (no time factor)

import random
from ingredients import get_name

# base payment when the drink is perfect; we scale down from here
BASE_PAYMENT = 14
TIP_BONUS = 4  # extra if perfect


def make_random_order(unlocked_ids, min_len=2, max_len=4):
    """Build a random drink from only unlocked ingredients. Order matters."""
    if not unlocked_ids:
        return []
    length = random.randint(min_len, max_len)
    return [random.choice(unlocked_ids) for _ in range(length)]


def order_to_string(order):
    if not order:
        return "(nothing)"
    return ", ".join(get_name(i) for i in order)


def is_perfect_match(expected, actual):
    """Exact match: same ingredients in same order."""
    if len(expected) != len(actual):
        return False
    return all(a == b for a, b in zip(expected, actual))


def score_drink(expected, actual):
    """
    Returns (money_earned, got_tip, feedback_string).
    Based only on ingredient correctness and order; no timer.
    """
    if not expected:
        return (0, False, "Empty order?")

    # ingredient correctness: how many slots are correct
    correct_slots = sum(1 for a, b in zip(expected, actual) if a == b) if actual else 0
    accuracy = correct_slots / len(expected)
    order_ok = is_perfect_match(expected, actual)

    # payment from accuracy and order only
    combined = accuracy * 0.6 + (1.0 if order_ok else 0.0) * 0.4
    payment = int(BASE_PAYMENT * combined)
    payment = max(0, payment)

    got_tip = order_ok
    if got_tip:
        payment += TIP_BONUS

    if order_ok:
        feedback = f"Perfect! +${payment}"
    elif accuracy >= 0.5:
        feedback = f"Close. +${payment}"
    else:
        feedback = f"Wrong order. +${payment}" if payment > 0 else "Wrong order. No pay."

    return (payment, got_tip, feedback)
