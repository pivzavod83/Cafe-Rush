# day_manager.py — one day at a time: fixed number of customers, then summary, then shop
# no endless spawning; clear start and end of each day so pacing feels intentional
# customer count scales with day number so later days feel harder

from customer import Customer

# how many customers per day: start gentle, ramp up over time
CUSTOMERS_MIN = 5
CUSTOMERS_MAX = 10
CUSTOMERS_GROWTH_PER_DAY = 0.4


def _customer_count(day):
    n = CUSTOMERS_MIN + int(day * CUSTOMERS_GROWTH_PER_DAY)
    return min(max(n, CUSTOMERS_MIN), CUSTOMERS_MAX)


class DayManager:
    """
    Tracks the current day and the exact flow: serving -> summary -> shop -> next day.
    One customer at a time; when the queue is empty we move to summary.
    """

    PHASE_SERVING = "serving"
    PHASE_SUMMARY = "summary"
    PHASE_SHOP = "shop"

    def __init__(self, unlocked_ids):
        self.unlocked_ids = list(unlocked_ids)
        self.day = 1
        self.phase = self.PHASE_SERVING
        self.customers = []
        self.current_index = 0
        self.money_earned_today = 0
        self.results_today = []  # list of (payment, left_early) for summary; left_early always False now

    def start_day(self):
        """Build today's customer queue and set phase to serving."""
        n = _customer_count(self.day)
        self.customers = [
            Customer(self.unlocked_ids, color_index=self.day + i)
            for i in range(n)
        ]
        self.current_index = 0
        self.money_earned_today = 0
        self.results_today = []
        self.phase = self.PHASE_SERVING

    def current_customer(self):
        """The customer at the counter right now, or None if the day is over."""
        if self.current_index >= len(self.customers):
            return None
        return self.customers[self.current_index]

    def total_customers_today(self):
        return len(self.customers)

    def happy_count(self):
        """How many customers paid something."""
        return sum(1 for pay, left in self.results_today if not left and pay > 0)

    def serve_current(self, payment, left_early=False):
        """Called after we serve the current customer. Records result and moves to next."""
        self.results_today.append((payment, left_early))
        if not left_early:
            self.money_earned_today += payment
        self.current_index += 1
        if self.current_index >= len(self.customers):
            self.phase = self.PHASE_SUMMARY

    def go_to_shop(self):
        """Player clicked through summary; show the shop."""
        self.phase = self.PHASE_SHOP

    def next_day(self, new_unlocked_ids):
        """Leave shop, save unlocked list, advance day and start the next one."""
        self.unlocked_ids = list(new_unlocked_ids)
        self.day += 1
        self.phase = self.PHASE_SERVING
        self.start_day()
