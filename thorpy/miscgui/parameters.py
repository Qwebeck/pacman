"""This module defines miscellaneous parameters for ThorPy. These parameters may
change during execution, so don't forget to import this module and then use its
attributes, instead of importing them directly or to use them as default args.
"""

from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYDOWN, KEYUP, K_UP, K_DOWN

CHILDREN_SHIFT = (0, 10)
HELP_WAIT_TIME = 500
WHEEL_LIFT_SHIFT = 10
WHEEL_SLIDER_SHIFT = 5
CLICK_LIFT_SHIFT = 1
CLICK_LIFT_REPEAT = 4
LIMVALS = (0., 100.)
DOUBLE_CLICK_DELAY = 400 #unit: ms

LEFT_CLICK_BUTTON = 1
RIGHT_CLICK_BUTTON = 3
MIDDLE_CLICK_BUTTON = 2  # may be WHEEL_CLICK_BUTTON
WHEELUP_BUTTON = 4
WHEELDOWN_BUTTON = 5

BUTTON_PRESS_EVENT = MOUSEBUTTONDOWN
BUTTON_UNPRESS_EVENT = MOUSEBUTTONUP

KEY_PRESS_EVENT = KEYDOWN
KEY_UNPRESS_EVENT = KEYUP

SLIDER_UP = K_UP
SLIDER_DOWN = K_DOWN

KEY_DELAY = 500
KEY_INTERVAL = 30

CURSOR_INTERVAL = 500

FILL_SCREEN_AT_SUBMENUS = False
SCREEN_FILL = (255,255,255)