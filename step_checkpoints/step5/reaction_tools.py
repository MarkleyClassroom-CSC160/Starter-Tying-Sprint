# reaction_tools.py
# The Typing Sprint's parts and helper functions, plus play_round().
# reaction_timer.py imports what it needs from this file.

from random import uniform, choice
from time import sleep, perf_counter
from gpiozero import LED, Buzzer

try:
    import termios
except ImportError:
    termios = None

# ----- parts -----
red = LED(17)
green = LED(22)
buzzer = Buzzer(18, active_high=False, initial_value=False)

TIME_LIMIT = 5.0   # a word that takes longer than 5 seconds does not count
WORDS = ["pixel", "cursor", "python", "server", "debug", "loop", "array", "float",
         "input", "print", "class", "tuple", "queue", "stack", "table", "query"]

# ----- helper functions (given) -----

def show_wait():
    green.off()
    red.on()


def show_go():
    red.off()
    green.on()


def lights_off():
    red.off()
    green.off()


def buzz(times):
    for beep in range(times):
        buzzer.on()
        sleep(0.1)
        buzzer.off()
        sleep(0.1)


def show_early():
    # round not counted: red blinks twice with one buzz
    for blink in range(2):
        red.on()
        sleep(0.15)
        red.off()
        sleep(0.15)
    buzz(1)


def show_best():
    # new personal best: green blinks three times with two buzzes
    for blink in range(3):
        green.on()
        sleep(0.15)
        green.off()
        sleep(0.15)
    buzz(2)


def clear_keyboard():
    # throw away keys typed ahead of time
    # works in a terminal; in other editors it quietly does nothing
    if termios is None:
        return
    try:
        termios.tcflush(0, termios.TCIFLUSH)
    except (termios.error, OSError, ValueError):
        pass


def play_round():
    word = choice(WORDS)
    show_wait()
    clear_keyboard()
    sleep(uniform(2, 4))
    clear_keyboard()
    buzz(1)
    show_go()
    print(f"    Type this word, then press Enter:  {word}")
    start = perf_counter()
    typed = input().strip()
    seconds = perf_counter() - start
    lights_off()
    if typed != word:
        print("    Not the same word.")
        return None
    if seconds > TIME_LIMIT:
        print("    Too slow.")
        return None
    return seconds
