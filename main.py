# main.py — game loop and phase handling
# day-based flow only; mouse for ingredients and buttons

import pygame
import sys
from ingredients import base_ids
from order import score_drink
from day_manager import DayManager
from shop import upgrades_for_sale, buy as shop_buy
from ui import (
    init_fonts,
    draw_serving,
    draw_summary,
    draw_shop,
    get_serving_rects,
    get_summary_rects,
    get_shop_rects,
)

FEEDBACK_DURATION = 1.2


def run():
    pygame.init()
    # fullscreen; (0, 0) lets pygame use the display's native resolution
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Café Rush")
    clock = pygame.time.Clock()

    fonts = init_fonts()

    # these persist across the whole run
    total_money = 0
    unlocked_ids = list(base_ids()) # base ingredients are unlocked

    # day flow: serving -> summary -> shop -> next day
    day_mgr = DayManager(unlocked_ids)
    day_mgr.start_day()

    # only used during serving phase
    current_drink = []
    feedback_text = None
    feedback_timer = 0.0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        # --- events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                phase = day_mgr.phase

                if phase == DayManager.PHASE_SERVING:
                    rects = get_serving_rects(unlocked_ids)
                    customer = day_mgr.current_customer()

                    if rects["serve"].collidepoint(pos):
                        if customer:
                            payment, got_tip, msg = score_drink(customer.order, current_drink)
                            day_mgr.serve_current(payment, left_early=False)
                            total_money += payment
                            feedback_text = msg
                            feedback_timer = FEEDBACK_DURATION
                            current_drink = []
                    elif rects["trash"].collidepoint(pos):
                        current_drink = []
                    else:
                        for ing_id, r in rects["ingredients"].items():
                            if r.collidepoint(pos) and customer:
                                current_drink.append(ing_id)
                                break

                elif phase == DayManager.PHASE_SUMMARY:
                    if get_summary_rects()["to_shop"].collidepoint(pos):
                        day_mgr.go_to_shop()

                elif phase == DayManager.PHASE_SHOP:
                    upgrades = upgrades_for_sale(unlocked_ids)
                    shop_rects = get_shop_rects(upgrades)
                    if shop_rects.get("continue") and shop_rects["continue"].collidepoint(pos): # go to next day
                        day_mgr.next_day(unlocked_ids)
                        current_drink = []
                        feedback_text = None
                        feedback_timer = 0.0
                    else:
                        for ing_id, r in shop_rects.items():
                            if ing_id == "continue":
                                continue
                            if r.collidepoint(pos):
                                result = shop_buy(unlocked_ids, ing_id, total_money)
                                if result:
                                    unlocked_ids, total_money = result
                                break

        if not running:
            break

        # --- update: fade out feedback message
        if feedback_timer > 0:
            feedback_timer -= dt
            if feedback_timer <= 0:
                feedback_text = None

        # --- draw
        phase = day_mgr.phase
        if phase == DayManager.PHASE_SERVING:
            draw_serving(
                screen, fonts,
                day_mgr.day, total_money,
                day_mgr.current_customer(), current_drink, unlocked_ids,
                feedback_text=feedback_text, feedback_time_left=feedback_timer,
            )
        elif phase == DayManager.PHASE_SUMMARY:
            draw_summary(
                screen, fonts,
                day_mgr.day, day_mgr.money_earned_today,
                day_mgr.happy_count(), day_mgr.total_customers_today(),
            )
        elif phase == DayManager.PHASE_SHOP:
            draw_shop(screen, fonts, total_money, upgrades_for_sale(unlocked_ids))

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    run()
