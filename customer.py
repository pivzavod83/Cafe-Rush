# customer.py — one customer at a time: their order and a face (colored rect)
# no timer; they wait until you serve them

from order import make_random_order

# different rectangle colors so customers feel a bit different
CUSTOMER_COLORS = [
    (180, 160, 140),
    (160, 140, 180),
    (140, 180, 160),
    (200, 170, 150),
    (170, 150, 200),
    (190, 175, 155),
]


class Customer:
    """Single customer at the counter. They have an order and a color. That's it."""

    def __init__(self, unlocked_ids, order=None, color_index=0):
        self.order = order if order is not None else make_random_order(unlocked_ids)
        self.color = CUSTOMER_COLORS[color_index % len(CUSTOMER_COLORS)]
