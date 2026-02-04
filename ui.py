# ui.py — all drawing and the rects we use for mouse clicks
# clear zones: customer + order at top, build area, ingredients, then serve/trash

import pygame
from ingredients import get_by_id
from order import order_to_string

# soft background so it doesn't feel harsh
BG = (248, 244, 238)

# ----- Serving screen layout -----
# top bar
BAR_LEFT = 24
BAR_TOP = 16
TITLE_TOP = 48

# customer + order (one clear block)
CUSTOMER_RECT = (40, 90, 360, 100)
ORDER_TOP = 200

# drink build area — shows what you've clicked so far
BUILD_LABEL_TOP = 268
BUILD_SLOTS_TOP = 298
BUILD_SLOT_SIZE = 36
BUILD_SLOT_GAP = 6

# ingredient row — only unlocked; centered
ING_SLOT_SIZE = 42
ING_ROW_TOP = 358
ING_ROW_LEFT_FIRST = 40
ING_GAP = 44

# buttons
SERVE_RECT = (40, 418, 120, 48)
TRASH_RECT = (180, 418, 120, 48)

# hint
HINT_TOP = 478

# ----- Summary screen -----
SUM_TITLE_TOP = 100
SUM_MONEY_TOP = 180
SUM_HAPPY_TOP = 230
TO_SHOP_RECT = (200, 300, 200, 52)

# ----- Shop screen -----
SHOP_TITLE_TOP = 70
SHOP_MONEY_TOP = 115
SHOP_FIRST_ITEM_TOP = 155
SHOP_ITEM_H = 48
SHOP_ITEM_GAP = 10
SHOP_ITEM_W = 320
SHOP_ITEM_LEFT = 40
CONTINUE_RECT = (160, 420, 240, 52)


def init_fonts():
    pygame.font.init()
    return {
        "title": pygame.font.Font(None, 52),
        "body": pygame.font.Font(None, 34),
        "small": pygame.font.Font(None, 26),
    }


def _centered_x(surface, width):
    return (surface.get_width() - width) // 2


# ---------- Serving screen ----------

def _ingredient_slot_rects(unlocked_ids):
    """Rects for each ingredient slot; we use these for drawing and for click hit-test."""
    rects = {}
    start_x = ING_ROW_LEFT_FIRST
    for i, ing_id in enumerate(unlocked_ids):
        rects[ing_id] = pygame.Rect(start_x + i * ING_GAP, ING_ROW_TOP, ING_SLOT_SIZE, ING_SLOT_SIZE)
    return rects


def get_serving_rects(unlocked_ids):
    """All clickable rects on the serving screen. Main uses this for mouse."""
    rects = {"serve": pygame.Rect(SERVE_RECT), "trash": pygame.Rect(TRASH_RECT)}
    rects["ingredients"] = _ingredient_slot_rects(unlocked_ids)
    return rects


def draw_serving(
    surface, fonts,
    day, total_money,
    customer, current_drink, unlocked_ids,
    feedback_text=None, feedback_time_left=0,
):
    """Draw the main gameplay screen. One customer, order, build area, ingredients, serve/trash."""
    surface.fill(BG)

    # top bar
    bar = fonts["body"].render(f"Day {day}   |   $ {total_money}", True, (50, 45, 40))
    surface.blit(bar, (BAR_LEFT, BAR_TOP))
    title = fonts["title"].render("Café Rush", True, (60, 52, 44))
    surface.blit(title, (_centered_x(surface, title.get_width()), TITLE_TOP))

    # customer block
    if customer:
        r = pygame.Rect(CUSTOMER_RECT)
        pygame.draw.rect(surface, customer.color, r)
        pygame.draw.rect(surface, (70, 60, 50), r, 2)
        order_text = fonts["body"].render("Order: " + order_to_string(customer.order), True, (40, 35, 30))
        surface.blit(order_text, (40, ORDER_TOP))

    # build area — your current drink as a row of colored boxes
    label = fonts["small"].render("Your drink:", True, (60, 55, 48))
    surface.blit(label, (40, BUILD_LABEL_TOP))
    x = 40
    for ing_id in current_drink:
        ing = get_by_id(ing_id)
        color = ing["color"] if ing else (120, 120, 120)
        rect = pygame.Rect(x, BUILD_SLOTS_TOP, BUILD_SLOT_SIZE, BUILD_SLOT_SIZE)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, (70, 60, 50), rect, 1)
        x += BUILD_SLOT_SIZE + BUILD_SLOT_GAP
    if not current_drink:
        placeholder = fonts["small"].render("(click ingredients below)", True, (130, 120, 110))
        surface.blit(placeholder, (40, BUILD_SLOTS_TOP + 6))

    # ingredient row
    slot_rects = _ingredient_slot_rects(unlocked_ids)
    for ing_id, rect in slot_rects.items():
        ing = get_by_id(ing_id)
        if ing:
            pygame.draw.rect(surface, ing["color"], rect)
            pygame.draw.rect(surface, (70, 60, 50), rect, 2)

    # serve and trash buttons
    serve_r = pygame.Rect(SERVE_RECT)
    pygame.draw.rect(surface, (70, 130, 80), serve_r)
    pygame.draw.rect(surface, (40, 70, 50), serve_r, 2)
    surface.blit(fonts["body"].render("Serve", True, (255, 255, 255)), (serve_r.x + 38, serve_r.y + 12))
    trash_r = pygame.Rect(TRASH_RECT)
    pygame.draw.rect(surface, (150, 90, 90), trash_r)
    pygame.draw.rect(surface, (90, 50, 50), trash_r, 2)
    surface.blit(fonts["body"].render("Trash", True, (255, 255, 255)), (trash_r.x + 38, trash_r.y + 12))

    # brief feedback above buttons
    if feedback_text and feedback_time_left > 0:
        t = fonts["body"].render(feedback_text, True, (50, 45, 40))
        surface.blit(t, (_centered_x(surface, t.get_width()), SERVE_RECT[1] - 28))

    hint = fonts["small"].render("Click ingredients to build, then Serve. Trash to clear. Esc to quit.", True, (100, 92, 85))
    surface.blit(hint, (40, HINT_TOP))


# ---------- Summary screen ----------

def get_summary_rects():
    return {"to_shop": pygame.Rect(TO_SHOP_RECT)}


def draw_summary(surface, fonts, day, money_earned, happy_count, total_customers):
    surface.fill(BG)
    title = fonts["title"].render(f"Day {day} complete", True, (60, 52, 44))
    surface.blit(title, (_centered_x(surface, title.get_width()), SUM_TITLE_TOP))
    money_t = fonts["body"].render(f"Money earned today: $ {money_earned}", True, (50, 45, 40))
    surface.blit(money_t, (_centered_x(surface, money_t.get_width()), SUM_MONEY_TOP))
    happy_t = fonts["body"].render(f"Happy customers: {happy_count} / {total_customers}", True, (50, 45, 40))
    surface.blit(happy_t, (_centered_x(surface, happy_t.get_width()), SUM_HAPPY_TOP))
    r = pygame.Rect(TO_SHOP_RECT)
    pygame.draw.rect(surface, (100, 85, 130), r)
    pygame.draw.rect(surface, (60, 50, 80), r, 2)
    surface.blit(fonts["body"].render("To shop", True, (255, 255, 255)), (r.x + 68, r.y + 14))


# ---------- Shop screen ----------

def get_shop_rects(upgrades_list):
    """upgrades_list is list of (ing_id, name, cost). Returns rects by ing_id and 'continue'."""
    out = {}
    for i, (ing_id, name, cost) in enumerate(upgrades_list):
        y = SHOP_FIRST_ITEM_TOP + i * (SHOP_ITEM_H + SHOP_ITEM_GAP)
        out[ing_id] = pygame.Rect(SHOP_ITEM_LEFT, y, SHOP_ITEM_W, SHOP_ITEM_H)
    out["continue"] = pygame.Rect(CONTINUE_RECT)
    return out


def draw_shop(surface, fonts, total_money, upgrades_list):
    surface.fill(BG)
    title = fonts["title"].render("Shop", True, (60, 52, 44))
    surface.blit(title, (_centered_x(surface, title.get_width()), SHOP_TITLE_TOP))
    money_t = fonts["body"].render(f"Your money: $ {total_money}", True, (50, 45, 40))
    surface.blit(money_t, (SHOP_ITEM_LEFT, SHOP_MONEY_TOP))
    for i, (ing_id, name, cost) in enumerate(upgrades_list):
        y = SHOP_FIRST_ITEM_TOP + i * (SHOP_ITEM_H + SHOP_ITEM_GAP)
        rect = pygame.Rect(SHOP_ITEM_LEFT, y, SHOP_ITEM_W, SHOP_ITEM_H)
        can = total_money >= cost
        bg = (220, 245, 220) if can else (235, 220, 220)
        pygame.draw.rect(surface, bg, rect)
        pygame.draw.rect(surface, (70, 60, 50), rect, 1)
        surface.blit(fonts["body"].render(f"{name}  —  $ {cost}", True, (45, 40, 35)), (rect.x + 12, rect.y + 12))
    r = pygame.Rect(CONTINUE_RECT)
    pygame.draw.rect(surface, (70, 130, 80), r)
    pygame.draw.rect(surface, (40, 70, 50), r, 2)
    surface.blit(fonts["body"].render("Continue to next day", True, (255, 255, 255)), (r.x + 52, r.y + 14))
